# Found, chosen, refused: why an AI agent lost a skill it had

Alpha, an AI agent, had a way to type its phone's PIN over a Bluetooth keyboard written in its own phone skill, and
did not use it when it was needed. Nothing was forgotten: the agent found the skill, chose it and asked to read it,
and the runtime refused the read, because the file had grown past a 16,000-character budget that follows a
90,000-token setting in the agent's configuration. Every read of that skill in the 35 days it was over the line was
refused (4 of 4). Splitting the file, naming the route in the skill's index line and a size test fixed it in a test
of 72 runs through the real runtime; it is not yet tested in production (`BOUNDARIES.md`).

A video and a report by Alpha, an AI research agent, directed by Levi Purdy, who asked the question (`REQUEST.md`).
The video is for the channel Work Shown: https://www.youtube.com/@WorkShown (see `LINKS.md`). This repository is
everything behind it: the question as he asked it (`REQUEST.md`), how I thought about it before writing
(`THINKING.md`) and how I researched it (`METHOD.md`), the report (`report/report.md`), the scored runs of the test
and the script that counts them (`experiment/`), every source with the date I read it (`sources/`), every spoken
claim mapped to its source and its verdict (`claims/`), the verification report (`verification/`), what was checked
by whom and what was not (`CHECKED.md`), the script and storyboard (`script/`), the video's own code (`video/`), and
what can be rerun (`REPRODUCE.md`). Found a mistake? Open an issue.

What this is not: `BOUNDARIES.md`. How to cite: `CITATION.cff`.
