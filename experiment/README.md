# The runtime test

The test of 2026-11-24: Alpha's phone-skill requests through OpenClaw's own embedded agent, with the old layout of
the phone skill and the new.

- **What was real:** OpenClaw 2026.9.8 (`openclaw agent --local`), Alpha's prompt files (AGENTS.md, SOUL.md, USER.md,
  IDENTITY.md), all 12 of its skills in the index beside three bundled ones, its model route (Claude Haiku 5.5 on
  OpenRouter, contextTokens 90,000) and its `coding` tool profile, with the read tool's skill budget.
- **What differed, so nothing could reach the phone, Levi or a worker:** tools ran in a Podman sandbox with no network,
  on a Debian image without Python (so the unlock script could not run); the workspace was a copy without secrets;
  message, web, cron, browser and spawn tools were denied, and a spawn attempt was recorded with its brief. Messages
  arrived bare, not in a Telegram envelope.
- **Layouts:** old, the phone skill as one 17,438-byte SKILL.md; new, a 7,577-byte core with `pin.md`, `updates.md`
  and `flows.md` beside it, and an index line naming the PIN, screen unlock, the Bluetooth keyboard and `unlock.py`.
- **Requests:** `prompts.json`, twelve: Levi's two of 2026-11-23 verbatim and ten written by the author. Three runs of
  each per layout, each a fresh session: 72 runs, $0.42 on OpenRouter.

## Scoring (fixed after one trial run, before the scored runs)

A successful spawn ends Alpha's turn in production; here it failed and the model went on. So a run is scored up to
its first spawn attempt, or in full if it has none.

| field | meaning |
|---|---|
| `delegated` | it tried to start a worker |
| `read_phone` | before that point, it tried to read a phone skill file |
| `first_served` | that first read was served, not refused |
| `route` | `unlock.py` appears in what it did or said before that point |
| `route_any` | the same over the whole run (reference only) |
| `brief_route` | the first spawn's brief names `unlock.py` (counted after the scored runs) |
| `too_long` | a reply before that point tells the user the file was too long or could not be read |
| `shell_read` | anywhere in the run, a shell command reads the phone SKILL.md |
| `calls` | tool calls before that point |
| `cost` | the run's cost on OpenRouter, dollars |
| `tools` | the name of each tool call, in order |

`table.py` counts them; `test_table.py` holds the counts the report gives.
