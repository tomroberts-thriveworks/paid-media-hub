"""Pull raw Google Ads data to local CSVs (one set per customer). Run once, then
analyze offline so repeat analysis costs no API quota (Explorer ~2,880 ops/day)."""
import csv
from pathlib import Path

from ..config import load_google_ads_settings
from ..google_ads.client import get_client, run_query
from ..google_ads.queries import QUERIES


def _get(row, path):
    obj = row
    for part in path.split("."):
        obj = getattr(obj, part)
    return obj.name if hasattr(obj, "name") and not isinstance(obj, str) else obj


def pull(start: str, end: str, out_dir: str = "data/raw", only=None) -> int:
    settings = load_google_ads_settings()
    client = get_client()
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    requests = 0
    for cid in settings.customer_ids:
        for name, (gaql, cols) in QUERIES.items():
            if only and name not in only:
                continue
            q = gaql.format(start=start, end=end) if "{start}" in gaql else gaql
            path = out / f"{cid}_{name}.csv"
            n = 0
            with path.open("w", newline="") as f:
                w = csv.writer(f)
                w.writerow(["customer_id", *cols])
                for row in run_query(client, cid, q):
                    w.writerow([cid, *[_get(row, c) for c in cols]])
                    n += 1
            requests += 1
            print(f"{cid} {name}: {n} rows -> {path}")
    print(f"API requests used: {requests}")
    return requests
