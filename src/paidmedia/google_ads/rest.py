"""Direct REST client for the Google Ads API (stdlib only, no google-ads library).

Built for the cloud environment, where the egress proxy injects secrets per host:
  - oauth2.googleapis.com     -> HTTP Basic auth = client ID / client secret
  - googleads.googleapis.com  -> header `developer-token`
So the code only needs GOOGLE_ADS_REFRESH_TOKEN, GOOGLE_ADS_LOGIN_CUSTOMER_ID and
GOOGLE_ADS_CUSTOMER_IDS. If GOOGLE_ADS_CLIENT_ID/SECRET or GOOGLE_ADS_DEVELOPER_TOKEN
are set (e.g. on the laptop), they are sent explicitly instead.
"""
import base64
import json
import os
import time
import urllib.error
import urllib.parse
import urllib.request

TOKEN_URL = "https://oauth2.googleapis.com/token"
API_ROOT = "https://googleads.googleapis.com"
# Newest first; the first version that answers is used. Update as Google releases versions.
CANDIDATE_VERSIONS = [f"v{n}" for n in range(26, 18, -1)]


class GoogleAdsError(RuntimeError):
    pass


def _post(url, body: bytes, headers: dict):
    req = urllib.request.Request(url, data=body, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            return r.status, r.read()
    except urllib.error.HTTPError as e:
        return e.code, e.read()


class AdsClient:
    def __init__(self):
        self.refresh_token = os.environ.get("GOOGLE_ADS_REFRESH_TOKEN")
        if not self.refresh_token:
            raise GoogleAdsError("GOOGLE_ADS_REFRESH_TOKEN is not set")
        self.login_customer_id = os.environ.get("GOOGLE_ADS_LOGIN_CUSTOMER_ID", "").replace("-", "")
        self.customer_ids = [c.strip().replace("-", "") for c in
                             os.environ.get("GOOGLE_ADS_CUSTOMER_IDS", "").split(",") if c.strip()]
        self._token, self._expires, self.version = None, 0.0, None

    # --- auth -------------------------------------------------------------
    def access_token(self) -> str:
        if self._token and time.time() < self._expires - 60:
            return self._token
        form = {"grant_type": "refresh_token", "refresh_token": self.refresh_token}
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        cid, secret = os.environ.get("GOOGLE_ADS_CLIENT_ID"), os.environ.get("GOOGLE_ADS_CLIENT_SECRET")
        if cid and secret:  # laptop mode; in the cloud the proxy adds Basic auth
            headers["Authorization"] = "Basic " + base64.b64encode(f"{cid}:{secret}".encode()).decode()
        status, body = _post(TOKEN_URL, urllib.parse.urlencode(form).encode(), headers)
        if status != 200:
            raise GoogleAdsError(f"Token refresh failed ({status}): {body[:300]!r}")
        data = json.loads(body)
        self._token, self._expires = data["access_token"], time.time() + data.get("expires_in", 3600)
        return self._token

    def _headers(self):
        h = {"Authorization": f"Bearer {self.access_token()}", "Content-Type": "application/json"}
        if self.login_customer_id:
            h["login-customer-id"] = self.login_customer_id
        dev = os.environ.get("GOOGLE_ADS_DEVELOPER_TOKEN")
        if dev:  # laptop mode; in the cloud the proxy adds it
            h["developer-token"] = dev
        return h

    # --- queries ----------------------------------------------------------
    def _search_once(self, version, customer_id, query):
        url = f"{API_ROOT}/{version}/customers/{customer_id}/googleAds:searchStream"
        return _post(url, json.dumps({"query": query}).encode(), self._headers())

    def search(self, customer_id: str, query: str):
        """Yield result rows as dicts (REST JSON, camelCase field names)."""
        versions = [self.version] if self.version else CANDIDATE_VERSIONS
        last = None
        for v in versions:
            status, body = self._search_once(v, customer_id, query)
            if status == 404 and not self.version:
                last = (v, status, body)
                continue  # version not available, try older
            if status != 200:
                raise GoogleAdsError(f"{v} search failed ({status}): {body[:1500].decode(errors='replace')}")
            self.version = v
            for batch in json.loads(body):
                yield from batch.get("results", [])
            return
        raise GoogleAdsError(f"No API version answered; last: {last}")

    def accessible_customers(self):
        """List accounts the signed-in user can reach (smoke test, no customer ID needed)."""
        for v in [self.version] if self.version else CANDIDATE_VERSIONS:
            url = f"{API_ROOT}/{v}/customers:listAccessibleCustomers"
            req = urllib.request.Request(url, headers=self._headers())
            try:
                with urllib.request.urlopen(req, timeout=60) as r:
                    self.version = v
                    return json.loads(r.read()).get("resourceNames", [])
            except urllib.error.HTTPError as e:
                if e.code == 404 and not self.version:
                    continue
                raise GoogleAdsError(f"{v} listAccessibleCustomers failed ({e.code}): "
                                     f"{e.read()[:1500].decode(errors='replace')}")
        raise GoogleAdsError("No API version answered")


def get_field(row: dict, path: str):
    """'campaign.target_cpa.target_cpa_micros' -> row['campaign']['targetCpa']['targetCpaMicros']."""
    obj = row
    for part in path.split("."):
        head, *rest = part.split("_")
        key = head + "".join(w.capitalize() for w in rest)
        if not isinstance(obj, dict) or key not in obj:
            return ""
        obj = obj[key]
    return obj
