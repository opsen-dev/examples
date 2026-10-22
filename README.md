# examples

Runnable examples that use the opsen report JSON. Each reads the report from a read-only link: set `OPSEN_SHARE_TOKEN` to the token from **opsen → Settings → Read-only links**.

| Example | What it does |
| --- | --- |
| [`python/slack_digest.py`](python/slack_digest.py) | Posts the biggest findings to a Slack channel |
| [`python/to_warehouse.py`](python/to_warehouse.py) | Flattens the report into CSV files for any warehouse loader |
| [`python/budget_gate.py`](python/budget_gate.py) | Exits non-zero when a source is over the limit you pass |

Standard library only; Python 3.9 or later. For the job summary in GitHub Actions, see [report-action](https://github.com/opsen-dev/report-action).
