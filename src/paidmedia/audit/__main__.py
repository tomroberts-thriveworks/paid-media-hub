import argparse

p = argparse.ArgumentParser(prog="python -m paidmedia.audit")
sub = p.add_subparsers(dest="cmd", required=True)
pu = sub.add_parser("pull", help="download raw data to data/raw (uses API quota)")
pu.add_argument("--start", default="2026-01-01")
pu.add_argument("--end", required=True, help="YYYY-MM-DD")
pu.add_argument("--only", nargs="*", help="query names, e.g. campaigns conversion_actions")
sub.add_parser("check", help="verify auth and list accessible accounts")
sub.add_parser("report", help="build markdown findings from data/raw (offline)")
a = p.parse_args()
if a.cmd == "pull":
    from .pull import pull
    pull(a.start, a.end, only=a.only)
elif a.cmd == "check":
    from .pull import smoke_test
    smoke_test()
else:
    from .report import run
    run()
