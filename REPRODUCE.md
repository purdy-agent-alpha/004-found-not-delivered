# Reproduce

Tools: https://github.com/lpurdy01/video_pipeline_workspace/tree/cdbab44 (Levi Purdy's video pipeline, public), changed for the channel in a copy that is not public

## The counts (everything the video's test figures rest on)

Python 3.10 or later. From `experiment/`:

```
python3 table.py                  # the table, counted from runs.jsonl
python3 -m pytest test_table.py   # the counts the report and the video give
```

`runs.jsonl` holds each of the 72 scored runs: its layout, request, the scored fields and the name of each tool call.
It does not hold the transcripts: they quote Alpha's phone skill and prompt files, which hold personal details, so
they stay on the laptop where the runs were made. Running the test again needs OpenClaw, an OpenRouter key and
Alpha's own prompt files and skills, which are private; the harness is described in `experiment/README.md`.

The production counts (4 refused reads of 4, 52 skill reads) come from Alpha's private session log and cannot be
rerun from here.

## The video

Rendered with a copy of Levi Purdy's verification-compiler video pipeline (branch `video2-section1-hook` at
`cdbab44` in his repository), with the channel's changes: new chart kinds, the voice step, and fixes to the gate and
the assembly. That copy is not published yet; releasing it as the channel's shared tools repository is planned, not
done. What is here: the video's own code, `video/style.py`, `video/data.py` and one scene per section in
`video/scenes/`.

- What cannot be reproduced exactly: the agents' runs, the checks made by models, and the voice render.
