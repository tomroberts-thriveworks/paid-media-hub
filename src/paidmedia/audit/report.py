"""Offline analysis of pulled CSVs -> markdown findings. No API calls."""
import csv
from collections import defaultdict
from pathlib import Path

from ..metrics import cpb, is_booking_action
from ..naming import parse_campaign, BOOKINGS, PROXY

CONSENT_LAUNCH = "2026-05-27"  # Osano banner


def read(path):
    with open(path, newline="") as f:
        return list(csv.DictReader(f))


def load(raw_dir="data/raw"):
    d = Path(raw_dir)
    def cat(kind):
        rows = []
        for p in sorted(d.glob(f"*_{kind}.csv")):
            rows += read(p)
        return rows
    return {k: cat(k) for k in ("campaigns", "conversion_actions", "campaign_daily",
                                "campaign_conversions")}


def _f(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return 0.0


def _money(micros):
    return _f(micros) / 1e6


def _table(headers, rows):
    out = ["| " + " | ".join(headers) + " |", "|" + "---|" * len(headers)]
    out += ["| " + " | ".join(str(c) for c in r) + " |" for r in rows]
    return "\n".join(out)


def account_map(campaigns):
    lines = ["# Account map", f"{len(campaigns)} non-removed campaigns.\n"]
    rows, flags = [], []
    for c in sorted(campaigns, key=lambda r: r["campaign.name"]):
        info = parse_campaign(c["campaign.name"])
        tcpa = _money(c["campaign.target_cpa.target_cpa_micros"]
                      or c["campaign.maximize_conversions.target_cpa_micros"])
        rows.append([c["campaign.name"], c["campaign.status"],
                     c["campaign.advertising_channel_type"], c["campaign.bidding_strategy_type"],
                     f"${_money(c['campaign_budget.amount_micros']):,.0f}/day",
                     f"${tcpa:,.0f}" if tcpa else "-", info.goal_type,
                     ",".join(info.states) or ("USA" if info.nationwide else "-")])
        if info.brand is None or info.channel is None:
            flags.append(f"Name not fully parsed: `{c['campaign.name']}`")
        if c["campaign.status"] == "ENABLED" and info.goal_type == BOOKINGS and tcpa and tcpa < 100:
            flags.append(f"`{c['campaign.name']}` is bookings-goaled but tCPA ${tcpa:,.0f} looks like a proxy target")
        if c["campaign.status"] == "ENABLED" and info.goal_type == PROXY and tcpa and tcpa > 100:
            flags.append(f"`{c['campaign.name']}` is proxy-goaled by name but tCPA ${tcpa:,.0f} looks like a booking target")
    lines.append(_table(["Campaign", "Status", "Type", "Bid strategy", "Budget", "tCPA",
                         "Goal (from name)", "States"], rows))
    lines.append("\n## Flags\n" + ("\n".join(f"- {x}" for x in flags) or "None"))
    lines.append("\nGoal type is inferred from the name; verify against actual conversion goals.")
    return "\n".join(lines)


def conversion_setup(actions):
    rows = [[a["conversion_action.name"], a["conversion_action.type"],
             a["conversion_action.status"], a["conversion_action.category"],
             a["conversion_action.primary_for_goal"],
             a["conversion_action.include_in_conversions_metric"],
             "YES" if is_booking_action(a["conversion_action.name"]) else ""]
            for a in sorted(actions, key=lambda r: r["conversion_action.name"])]
    hits = [r for r in rows if r[-1]]
    lines = ["# Conversion setup", _table(["Action", "Type", "Status", "Category", "Primary",
                                           "In 'Conversions'", "Counts as Bookings*"], rows)]
    lines.append(f"\n{len(hits)} action(s) matched as Event 1 / Event 4 by name."
                 + ("" if len(hits) >= 2 else
                    " **Fewer than 2 matched: fix BOOKING_EVENT_NAMES in metrics.py before trusting any CPB.**"))
    return "\n".join(lines)


def _build(data):
    camp = {c["campaign.id"]: c for c in data["campaigns"]}
    spend, bookings = defaultdict(float), defaultdict(float)  # key (campaign, date)
    for r in data["campaign_daily"]:
        spend[(r["campaign.id"], r["segments.date"])] += _money(r["metrics.cost_micros"])
    for r in data["campaign_conversions"]:
        if is_booking_action(r["segments.conversion_action_name"]):
            bookings[(r["campaign.id"], r["segments.date"])] += _f(r["metrics.conversions"])
    return camp, spend, bookings


def _group(spend, bookings, keyfn):
    s, b = defaultdict(float), defaultdict(float)
    for k, v in spend.items():
        s[keyfn(*k)] += v
    for k, v in bookings.items():
        b[keyfn(*k)] += v
    return s, b


def _rows(s, b):
    out = []
    for k in sorted(s, key=lambda k: -s[k]):
        v = cpb(s[k], b.get(k, 0))
        out.append([k, f"${s[k]:,.0f}", f"{b.get(k, 0):,.0f}", f"${v:,.0f}" if v else "n/a"])
    return out


def efficiency(data):
    camp, spend, bookings = _build(data)
    if not bookings:
        return ("# Efficiency\nNo Event 1 / Event 4 conversions matched. "
                "Check the Conversion setup report first.")
    H = ["", "Spend", "Bookings*", "CPB"]
    def info(cid):
        return parse_campaign(camp[cid]["campaign.name"]) if cid in camp else None
    def name(cid): return camp[cid]["campaign.name"] if cid in camp else cid
    L = ["# Efficiency (Bookings* = Event 1 + Event 4; CPB = spend / Bookings*)",
         "Proxy-goaled campaigns are shown with their Event 1/4 bookings only, never their own 'conversions'."]
    s, b = _group(spend, bookings, lambda c, d: name(c))
    L += ["\n## By campaign", _table(["Campaign"] + H[1:], _rows(s, b))]
    s, b = _group(spend, bookings, lambda c, d: info(c).goal_type if info(c) else "unknown")
    L += ["\n## By goal type (from name)", _table(["Goal type"] + H[1:], _rows(s, b))]
    s, b = _group(spend, bookings, lambda c, d: d[:7])
    rows = sorted(_rows(s, b))
    L += ["\n## By month", _table(["Month"] + H[1:], rows)]
    def stl(c, d):
        i = info(c)
        return ",".join(i.states) if i and i.states else ("USA" if i and i.nationwide else "other")
    s, b = _group(spend, bookings, stl)
    L += ["\n## By state (single/multi-state campaigns as named)", _table(["State"] + H[1:], _rows(s, b))]
    s, b = _group(spend, bookings, lambda c, d: "declining 10" if info(c) and info(c).declining_market else "other")
    L += ["\n## Declining-market campaigns vs rest", _table([""] + H[1:], _rows(s, b))]
    def consent(c, d):
        i = info(c)
        return f"{i.regulation if i else 'unknown'} / {'after' if d >= CONSENT_LAUNCH else 'before'} {CONSENT_LAUNCH}"
    s, b = _group(spend, bookings, consent)
    L += ["\n## Consent banner (opt-in 'high' vs opt-out 'low' states)",
          _table(["Regulation / period"] + H[1:], sorted(_rows(s, b))),
          "Before/after periods have different lengths; compare CPB and daily rates, not totals."]
    return "\n".join(L)


def run(raw_dir="data/raw", out_dir="data/reports"):
    data = load(raw_dir)
    out = Path(out_dir); out.mkdir(parents=True, exist_ok=True)
    reports = {"1_account_map.md": account_map(data["campaigns"]),
               "2_conversion_setup.md": conversion_setup(data["conversion_actions"]),
               "3_efficiency.md": efficiency(data)}
    for fn, text in reports.items():
        (out / fn).write_text(text + "\n")
        print("wrote", out / fn)
