"""Post the week's biggest findings to Slack.

    OPSEN_SHARE_TOKEN=... SLACK_WEBHOOK_URL=... python slack_digest.py
"""
import json
import os
import urllib.request

report = json.load(urllib.request.urlopen(f"https://opsen.dev/r/{os.environ['OPSEN_SHARE_TOKEN']}.json"))
top = sorted(report["findings"], key=lambda f: -f["monthly_usd"])[:5]
lines = [f"*{report['org']}*: ${report['monthly_waste']:,.0f} a month paid for and not used."]
lines += [f"• {f['title']}: ${f['monthly_usd']:,.0f}/mo" for f in top]
urllib.request.urlopen(urllib.request.Request(
    os.environ["SLACK_WEBHOOK_URL"], method="POST",
    data=json.dumps({"text": "\n".join(lines)}).encode(), headers={"content-type": "application/json"}))
