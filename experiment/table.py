#!/usr/bin/env python3
"""The runtime test's table, counted from runs.jsonl (one scored run per line).

    python3 table.py            prints the counts per layout

Each run's fields are described in README.md. Every count the video and report/report.md give for the 72 runs comes
from counts() below.
"""
import json
import statistics
from pathlib import Path

RUNS = Path(__file__).with_name("runs.jsonl")
LAYOUTS = ("old", "new")


def load(path: Path = RUNS) -> list[dict]:
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def counts(rows: list[dict]) -> dict[str, dict]:
    """Per layout: runs, the run counts of each scored field, the briefs that named the route among the runs that
    delegated, the median tool calls before deciding, and the cost in dollars."""
    out = {}
    for layout in LAYOUTS:
        rs = [r for r in rows if r["layout"] == layout]
        if not rs:
            continue
        c = {k: sum(bool(r[k]) for r in rs) for k in
             ("read_phone", "first_served", "too_long", "shell_read", "route", "delegated", "error")}
        c["brief_route"] = sum(bool(r["brief_route"]) for r in rs if r["delegated"])
        c["runs"] = len(rs)
        c["median_calls"] = statistics.median(r["calls"] for r in rs)
        c["cost"] = round(sum(r["cost"] or 0 for r in rs), 2)
        out[layout] = c
    return out


if __name__ == "__main__":
    for layout, c in counts(load()).items():
        print(layout, " ".join(f"{k}={v}" for k, v in c.items()))
