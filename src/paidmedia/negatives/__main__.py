"""python -m paidmedia.negatives [--campaign NAME] [--days 30] [--apply]

Dry run by default: prints the plan and writes data/negatives/plan_<date>.csv.
--apply validates with Google first, then adds the negatives.
"""
import argparse
import csv
import datetime as dt
import os
import time
from collections import Counter, defaultdict

from ..google_ads.rest import AdsClient
from .sculpt import Group, norm, plan
from .themes import CAMPAIGNS


def load(client, cid, campaign, theme_of):
    q = lambda s: list(client.search(cid, s))
    groups = {}
    for r in q(f"SELECT ad_group.resource_name, ad_group.name FROM ad_group "
               f"WHERE campaign.name = '{campaign}' AND ad_group.status = 'ENABLED'"):
        name = r["adGroup"]["name"]
        theme = theme_of(name)
        if theme:
            groups[name] = Group(name, theme, [], set(), r["adGroup"]["resourceName"])
    for r in q(f"SELECT ad_group.name, ad_group_criterion.keyword.text, ad_group_criterion.keyword.match_type, "
               f"ad_group_criterion.negative, ad_group_criterion.status FROM ad_group_criterion "
               f"WHERE campaign.name = '{campaign}' AND ad_group_criterion.type = 'KEYWORD' "
               f"AND ad_group_criterion.status != 'REMOVED'"):
        g = groups.get(r["adGroup"]["name"])
        if not g:
            continue
        kw = r["adGroupCriterion"]
        text, match = kw["keyword"]["text"], kw["keyword"]["matchType"]
        if kw.get("negative"):
            g.negatives.add((norm(text), match))
        elif kw.get("status") == "ENABLED":
            g.keywords.append((text, match))
    return list(groups.values())


def search_terms(client, cid, campaign, days, names):
    end = dt.date.today() - dt.timedelta(days=1)
    start = end - dt.timedelta(days=days - 1)
    rows = defaultdict(lambda: [0, 0.0])
    for r in client.search(cid, f"SELECT ad_group.name, search_term_view.search_term, metrics.clicks, "
                                f"metrics.cost_micros FROM search_term_view WHERE campaign.name = '{campaign}' "
                                f"AND segments.date BETWEEN '{start}' AND '{end}' AND metrics.impressions > 0"):
        name = r["adGroup"]["name"]
        if name in names:
            k = (name, r["searchTermView"]["searchTerm"])
            rows[k][0] += int(r["metrics"].get("clicks", 0))
            rows[k][1] += int(r["metrics"].get("costMicros", 0)) / 1e6
    return [(n, t, c, cost) for (n, t), (c, cost) in rows.items()]


def main():
    p = argparse.ArgumentParser(prog="python -m paidmedia.negatives")
    p.add_argument("--campaign", action="append", choices=sorted(CAMPAIGNS))
    p.add_argument("--days", type=int, default=30, help="search-term lookback")
    p.add_argument("--apply", action="store_true", help="add the negatives (default: dry run)")
    a = p.parse_args()
    client = AdsClient()
    cid = client.customer_ids[0]
    out_rows = []
    for campaign in a.campaign or sorted(CAMPAIGNS):
        cfg = CAMPAIGNS[campaign]
        groups = load(client, cid, campaign, cfg["theme_of"])
        st = search_terms(client, cid, campaign, a.days, {g.name for g in groups})
        adds, skipped = plan(groups, cfg["tiers"], st)
        res = {g.name: g.resource for g in groups}
        by_reason = Counter(n.reason.split(" (")[0] if n.reason.startswith("search term") else
                            ("funnel" if n.reason.startswith("funnel") else n.reason) for n in adds)
        print(f"\n{campaign}: {len(groups)} managed ad groups, {len(st)} search terms ({a.days}d)")
        print(f"  negatives to add: {len(adds)}  {dict(by_reason)}  skipped: {len(skipped)}")
        for g, n in sorted(Counter(n.group for n in adds).items(), key=lambda x: -x[1])[:8]:
            print(f"    {g}: {n}")
        for n in [n for n in adds if n.reason.startswith("search term")][:15]:
            print(f"    exact -> {n.group}: [{n.text}]  {n.reason}")
        for n in adds + skipped:
            out_rows.append([campaign, n.group, n.text, n.match, n.reason, "skip" if n in skipped else "add"])
        if a.apply and adds:
            ops = [{"create": {"adGroup": res[n.group], "negative": True,
                               "keyword": {"text": n.text, "matchType": n.match}}} for n in adds]
            batches = [ops[i:i + 250] for i in range(0, len(ops), 250)]
            for b in batches:                       # validate everything before changing anything
                client.mutate(cid, "adGroupCriteria", b, validate_only=True)
                time.sleep(10)
            for b in batches:
                client.mutate(cid, "adGroupCriteria", b, validate_only=False)
                time.sleep(20)
            print(f"  APPLIED {len(ops)} negatives")
    os.makedirs("data/negatives", exist_ok=True)
    path = f"data/negatives/plan_{dt.date.today()}.csv"
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["campaign", "ad_group", "negative", "match", "reason", "action"])
        w.writerows(out_rows)
    print(f"\nPlan written to {path}" + ("" if a.apply else "  (dry run: nothing changed; add --apply)"))


main()
