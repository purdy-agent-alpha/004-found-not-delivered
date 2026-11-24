# Method

- How the question became sub-questions: (1) Where did the knowledge go: was it missing from the store, missing from
  the index, not looked for, or not delivered? (2) How often did it happen: was the night of 2026-11-23 a one-off?
  (3) Where does the limit come from: the model, or a setting? (4) What do published agent designs do to keep
  operational knowledge retrievable, and do they measure this loss? (5) Does a small fix work through the real
  runtime, and what does it cost?
- Searched, where and when: Alpha's own session log, every skill read from 2026-10-12 to 2026-11-24 (private; the
  counts are in report/report.md); the installed runtime's code, OpenClaw 2026.9.8 (`dist/tool-result-limits-*.mjs`,
  `dist/agent-tools.read-*.mjs`), read 2026-11-23 and 2026-11-24; OpenRouter's model list, 2026-11-24; three papers
  read in full on 2026-11-23 (Voyager, MemGPT, Reflexion) and Anthropic's Agent Skills post. No wider literature
  search was done: the papers are a close reading of three designs, not a survey.
- Models and tools, by version: OpenClaw 2026.9.8's embedded agent (`openclaw agent --local`), Claude Haiku 5.5
  through OpenRouter with contextTokens 90,000 as in Alpha's configuration, Alpha's own prompt files and all its
  skills; tools ran in a Podman sandbox with no network and no Python, so nothing could reach the phone. Twelve
  requests (`experiment/prompts.json`: Levi's two of 2026-11-23 and ten written by the author), three runs each,
  for the old layout (one 17.4 KB skill file) and the new (a 7.6 KB core and side files), on 2026-11-24. Scoring was
  fixed after one trial run and before the scored ones (`experiment/README.md`).
- Dead ends and dropped claims, each with why: Alpha's own failure catalogue had filed the first refused turn
  (2026-10-23) as the model asserting something it had not observed; the log shows a real refusal, reported in the
  model's words, so that reading is dropped (the video shows it struck). An earlier test of the fix was simulated
  rather than run through the runtime; this one replaces it. That earlier simulation put the limit at 12,000 bytes, a
  guess; measured through the runtime it is 16,000 characters (15,822 served, 16,062 refused).
