"""Exit non-zero when a source's monthly spend is over the limit you pass.
Use it in CI, cron or anywhere a failed command raises an alarm.

    OPSEN_SHARE_TOKEN=... python budget_gate.py --copilot 7000 --actions 8000
"""
import argparse
import json
import os
import sys
import urllib.request

p = argparse.ArgumentParser()
for k in ("seats", "copilot", "actions", "agents"):
    p.add_argument(f"--{k}", type=float)
a = p.parse_args()

r = json.load(urllib.request.urlopen(f"https://opsen.dev/r/{os.environ['OPSEN_SHARE_TOKEN']}.json"))
sp, ag = r["spend"], r.get("agents") or {}
spend = {
    "seats": sp.get("seats_monthly") or 0,
    "copilot": (sp.get("copilot_monthly") or 0) + (sp.get("copilot_credits_last_month") or 0),
    "actions": sp.get("actions_last_month") or 0,
    "agents": ((r.get("attribution") or {}).get("total_usd") or 0)
    + (ag.get("cursor") or {}).get("total_usd", 0) + (ag.get("openai") or {}).get("total_usd", 0),
}
over = [(k, spend[k], lim) for k, lim in vars(a).items() if lim is not None and spend[k] > lim]
for k, v, lim in over:
    print(f"{k}: ${v:,.0f} is over ${lim:,.0f}")
sys.exit(1 if over else 0)
