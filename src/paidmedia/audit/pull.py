"""Pull raw Google Ads data to local CSVs (one set per customer). Run once, then
analyze offline so repeat analysis costs no API quota (Explorer ~2,880 ops/day)."""
import csv
from pathlib import Path

from ..google_ads.queries import QUERIES
from ..google_ads.rest import AdsClient, get_field


def smoke_test():
    c = AdsClient()
    names = c.accessible_customers()
    print(f"Auth OK (API {c.version}). Accessible customers: {names}")
    print(f"Configured login customer: {c.login_customer_id or '-'}; customers: {c.customer_ids}")
    return c


def pull(start: str, end: str, out_dir: str = "data/raw", only=None) -> int:
    client = AdsClient()
    if not client.customer_ids:
        raise SystemExit("GOOGLE_ADS_CUSTOMER_IDS is not set")
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    requests = 0
    for cid in client.customer_ids:
        for name, (gaql, cols) in QUERIES.items():
            if only and name not in only:
                continue
            q = gaql.format(start=start, end=end) if "{start}" in gaql else gaql
            path = out / f"{cid}_{name}.csv"
            n = 0
            with path.open("w", newline="") as f:
                w = csv.writer(f)
                w.writerow(["customer_id", *cols])
                for row in client.search(cid, q):
                    w.writerow([cid, *[get_field(row, c) for c in cols]])
                    n += 1
            requests += 1
            print(f"{cid} {name}: {n} rows -> {path}")
    print(f"API requests used: {requests} (API {client.version})")
    return requests
