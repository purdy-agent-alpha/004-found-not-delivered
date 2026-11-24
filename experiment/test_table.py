"""The counts table.py gives for the saved runs are the ones the report and the video state."""
from table import counts, load


def test_counts_match_the_report():
    c = counts(load())
    assert c["old"] == {"read_phone": 34, "first_served": 0, "too_long": 8, "shell_read": 19, "route": 14,
                        "delegated": 19, "error": 0, "brief_route": 6, "runs": 36, "median_calls": 4, "cost": 0.21}
    assert c["new"] == {"read_phone": 34, "first_served": 34, "too_long": 0, "shell_read": 2, "route": 35,
                        "delegated": 17, "error": 0, "brief_route": 17, "runs": 36, "median_calls": 6, "cost": 0.21}


def test_brief_counts_only_runs_that_delegated():
    rows = [{"layout": "old", "brief_route": True, "delegated": False, "read_phone": 0, "first_served": 0,
             "too_long": 0, "shell_read": 0, "route": 0, "error": None, "calls": 1, "cost": 0.0}]
    assert counts(rows)["old"]["brief_route"] == 0
