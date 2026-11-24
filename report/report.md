# Found, chosen, refused: why an AI agent lost a skill it had

Read, measured and written 2026-11-23 and 2026-11-24 (Mountain
time; log times in UTC where marked). Guesses are marked GUESS. Nothing was published, sent or bought for it.

## Summary

On 2026-11-23 at 21:29 Levi Purdy asked Alpha to get its phone to the PIN screen, and a minute later asked whether it
could not type the PIN over the Bluetooth keyboard. The route existed, written up in Alpha's phone skill, and Alpha
reached for that file at 21:29. The knowledge was not lost from the store, and the model did not misjudge it: **the
runtime refused to hand the file over.** The phone skill had grown past the runtime's 16,000-character budget for one
skill read, a budget set by a 90,000-token setting in Alpha's configuration. Every production read of that skill in
the 35 days it was over the line was refused, 4 of 4; no other skill was refused in 52 skill reads over six weeks.
The fix (a split file, the route named in the index line, a size test) was tested through the real runtime in 72
runs: the first read of the phone skill was served in 0 of 34 runs before and 34 of 34 after, and the brief Alpha
wrote for a worker carried the route in 6 of 19 runs before and 17 of 17 after. It has not yet met production.

## The finding

- OpenClaw, the runtime Alpha runs (version 2026.9.8), serves a skill file whole or not at all. It drops `offset` and
  `limit` on a skill file and refuses the read when the file is over the per-result budget. The refusal reads: "Skill
  instructions cannot be partially served: the whole document exceeds this call's read or model-context budget. Ask
  the operator to reduce the document or increase the model context."
- The budget comes from the model's context window, as `contextTokens` in the configuration sets it. Alpha's chat
  model (Claude Haiku 5.5) is set to 90,000 tokens, which gives 16,000 characters. Below 100,000 tokens the budget is
  16,000 characters; from 100,000 it is 32,000, and from 200,000, 64,000.
- The 90,000 is a local setting, not the model's limit: OpenRouter lists Claude Haiku 5.5 at 1,000,000 tokens (its
  model list, 2026-11-24). Why 90,000 was chosen is not recorded where I looked, and a larger window costs more on
  every turn, so this report does not call it a mistake.
- Source: the installed package, `dist/tool-result-limits-*.mjs` and `dist/agent-tools.read-*.mjs`. Measured through
  the runtime: a 15,822-character file served, a 16,062-character file refused. Two 9.4 KB skills are served.
- The phone skill (17,438 bytes) passed 16,000 characters on 2026-10-19 and stayed over until it was split on
  2026-11-23. In those 35 days Alpha read it 4 times in production and was refused 4 times:
    - 2026-10-24 03:46 UTC, twice (2026-10-23 in Mountain time). Another person had asked Alpha to use the phone,
      and it told them the phone instructions were too long.
    - 2026-11-03 22:45 UTC, and 2026-11-24 04:29 UTC (21:29 on 2026-11-23, Mountain time: the PIN night).
- No other skill was refused in 52 skill reads from 2026-10-12 to 2026-11-24.

Alpha's own catalogue of failures had filed the 10-23 turn as the model asserting something it had not observed. The
log shows a real refusal, reported in the model's own words, so the runtime rule behind it went unseen for a month.
Only the model sees a refusal.

Three kinds of loss, of which the first was the cause here:

1. **Delivery (the context budget).** Knowledge in a skill file over the budget cannot be got by the normal read. The
   model can still get pieces through the shell if it thinks to (19 of 36 old runs below did).
2. **Routing (the index).** Before the fix, the phone skill's index line did not mention a PIN, unlocking or
   Bluetooth. A model that did not think of the phone skill had no hint that the route was in it.
3. **Not looking.** Alpha reads skills rarely (52 reads in six weeks of chats) and mostly hands a job to a worker with
   a brief in its own words. The worker can read the skills, but it starts from that brief.

## The test through the real runtime

OpenClaw's own embedded agent, on Alpha's model route, prompt files and skills, in a sandbox with no network and no
Python, so nothing could reach the phone (`../experiment/README.md`). Twelve requests, Levi's two of 2026-11-23 and ten
written by the author, three runs each per layout: 72 runs, $0.42.

| 36 runs each | old: one 17.4 KB SKILL.md | new: 7.6 KB core and side files |
|---|---|---|
| read a phone skill file before acting | 34 | 34 |
| that first read was served | **0** | **34** |
| told the user the instructions were too long or could not be read | 8 | 0 |
| read the SKILL.md through the shell, anywhere in the run | 19 | 2 |
| named `unlock.py` in what it did or said | **14** | **35** |
| tried to hand the job to a worker | 19 | 17 |
| ... and the brief named `unlock.py` | **6 of 19** | **17 of 17** |
| tool calls before deciding (median) | 4 | 6 |
| cost (OpenRouter) | $0.21 | $0.21 |

What it shows: the refusal, the "too long" reply and the lucky way round it through the shell all appear through the
real runtime, as in production; the split removes the first two and makes the third unneeded. The plainest number is
the brief (counted from the same transcripts after the scored runs, not one of the fields fixed before them). The new
layout costs two more tool calls before deciding: reading the side file. The new layout's one miss was a sandbox
artefact (it read the side file, then got stuck on the missing Python).

What it does not show: messages came bare, without a Telegram envelope or the day's chat; exec calls after the first
ones failed in the sandbox, so scoring stops at the first spawn; only Haiku was tested; these are rates on twelve
requests, ten of them the author's, not production rates; and as of 2026-11-24 the phone skill had not been read in
production since the split.

## Three published designs

All three papers were read in full on 2026-11-23.

- **Voyager** (Wang et al., arXiv 2305.16291). Each verified skill is stored as a program, keyed by the embedding of a
  description the model wrote when it saved it. The harness, not the model, queries the library with the current task
  and puts the top 5 programs in the prompt. Without the library, iron tools took 29 ± 11 iterations against 21 ± 7
  with it, and diamond tools were reached in 0 of 3 runs against 1 of 3 (Table 1).
- **MemGPT** (Packer et al., arXiv 2310.08560). Memory in tiers, with an archival store searched by embeddings; the
  model pages through results itself. Its own reported weakness is the nearest to Alpha's: the agent "will often stop
  paging through retriever results before exhausting the retriever database".
- **Reflexion** (Shinn et al., arXiv 2303.11366). Short written reflections on failed attempts, kept to "usually ...
  1-3" and put whole into every attempt; the authors name the sliding window as a limit and suggest vector or SQL
  stores as future work.
- Anthropic's Agent Skills post (2025-10-16) describes the design Alpha's runtime uses: each skill's name and
  description in the system prompt, the file read when the model judges it relevant.

My reading, not a claim about the field (no wider search was done): none of the three measures a store that holds the
knowledge while the path that delivers it drops it. Alpha works like MemGPT, a model that decides when to look.

**A vector database.** In Voyager and MemGPT, retrieval does the choosing because the library is too big to list in
the prompt. Alpha's index lists 15 skills in about 5,500 characters, and the model saw the phone skill's line. A
vector store would not have fixed 2026-11-23: the skill was found, chosen and refused. It would be the next step if
the index stopped fitting, or for knowledge in notes and memory files that no index lists, which is untested here.

GUESS: an agent's store of knowledge needs a check that each piece can still be delivered whole, and this is likely
true of other runtimes with skill files. Only OpenClaw was checked.

## Sources

- S1 this report and its runs: report/report.md, experiment/runs.jsonl, experiment/prompts.json, experiment/table.py
- S2 OpenClaw 2026.9.8, https://www.npmjs.com/package/openclaw/v/2026.9.8
- S3 OpenRouter, Claude Haiku 5.5, https://openrouter.ai/anthropic/claude-haiku-5.5
- S4 Voyager, https://arxiv.org/abs/2305.16291
- S5 MemGPT, https://arxiv.org/abs/2310.08560
- S6 Reflexion, https://arxiv.org/abs/2303.11366
- S7 Anthropic, Equipping agents for the real world with Agent Skills, https://www.anthropic.com/research/equipping-agents-for-the-real-world-with-agent-skills
