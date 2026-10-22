"""Flatten the report into two CSV files, ready for any warehouse loader.

    OPSEN_SHARE_TOKEN=... python to_warehouse.py
    # findings.csv: one row per finding
    # items.csv:    one row per person, invitation or workflow behind a finding
"""
import csv
import json
import os
import urllib.request

report = json.load(urllib.request.urlopen(f"https://opsen.dev/r/{os.environ['OPSEN_SHARE_TOKEN']}.json"))
taken = report["taken_at"]

with open("findings.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["org", "taken_at", "finding_id", "category", "title", "monthly_usd", "basis"])
    for x in report["findings"]:
        w.writerow([report["org"], taken, x["id"], x["category"], x["title"], x["monthly_usd"], x["basis"]])

with open("items.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["org", "taken_at", "finding_id", "subject", "monthly_usd", "detail"])
    for x in report["findings"]:
        for it in x["items"]:
            subject = it.get("login") or it.get("email") or f"{it.get('repo', '')}/{it.get('path', '')}"
            w.writerow([report["org"], taken, x["id"], subject, it.get("monthly_usd"), json.dumps(it)])
print(f"Wrote findings.csv and items.csv for {report['org']}")
