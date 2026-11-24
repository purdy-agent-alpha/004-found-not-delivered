"""The runtime test's counts for every scene, read once from experiment/runs.jsonl through experiment/table.py, and
the other figures the video shows, each with where it comes from (report/report.md). test_data.py checks them."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "experiment"))
from table import counts, load  # noqa: E402

RUNS = counts(load())
OLD, NEW = RUNS["old"], RUNS["new"]
TOTAL_RUNS = OLD["runs"] + NEW["runs"]
COST = "$0.42"                 # the 72 runs on OpenRouter, summed unrounded (report, "The test through the real runtime")
REQUESTS = 12                  # experiment/prompts.json
SAMPLES = 3                    # runs per request and layout

# The skill-read limit, measured through the runtime (report, "The finding").
SERVED_CHARS, REFUSED_CHARS, BUDGET_CHARS = 15_822, 16_062, 16_000
BUDGET_AT_100K = 32_000        # the budget from a 100,000-token window up (runtime source)
WINDOW_SET, WINDOW_LISTED = 90_000, 1_000_000   # Alpha's config; OpenRouter's listing, 2026-11-24
OLD_SKILL_BYTES, NEW_CORE_BYTES, PIN_BYTES = 17_438, 7_577, 4_818
SIZE_CAP_BYTES = 9_400         # skills/test_skill_size.py in Alpha's repository
INDEX_SKILLS, INDEX_CHARS = 15, 5_500
OWN_SKILLS = 12               # Alpha's own skills, each SKILL.md under the size test; the other 3 come with the runtime

# Production, from Alpha's session log (private; report, "The finding").
SEARCHED = ("10-12", "11-24")  # the first and last day of the log searched
CROSSED = "10-19"
REFUSED_READS = ("10-23", "10-23", "11-03", "11-23")
SKILL_READS = 52
DAYS_OVER = 35

# Voyager, Table 1 (iterations to iron tools, mean; diamond tools reached, of 3 runs), without and with the library.
VOYAGER_IRON = (29, 21)
VOYAGER_DIAMOND = (0, 1)
