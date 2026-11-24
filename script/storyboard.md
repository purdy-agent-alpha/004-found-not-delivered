# Storyboard

One beat per narration line, in the script's order, under a heading per section. Each beat starts with
`[kind; role; role]`: the kind from video-tools/CATALOGUE.md, or `~` when it transforms the figure on screen; the
roles the gate looks for: question, stakes, disclosure, plan, turn (the open); check, dropped, counter, limit,
answer, unknown, cta (the arc and the close).

The grammar this storyboard assumes (video/style.py): a skill is a page card whose height follows its size, and the
PIN route inside it is one gold line, gold meaning that piece of knowledge and nothing else; Alpha's model is a white
hexagon; the runtime is a blue door (a frame with an opening) that every read passes through; the budget is a cyan
rule across the door's opening, at 16,000 characters; a read that is served is a green path through the door, a
refused one stops at the door in red; the index is a list of short grey lines, one per skill, the phone's lit when it
is seen; a worker is a white square, its brief a small card it receives; a published source is a violet page; a run
is a dot, green when the knowledge got through, red when it did not; a setting from Alpha's configuration is a grey
plate with its value in monospace.

## 01 Open
1. [diagram; question] Alpha's hexagon beside a shelf of skill cards; one card holds a gold line; a question mark on the path between them
2. [timeline; stakes] 2026-11-23: 21:29 Levi asks for the PIN screen; 21:29 Alpha reads the phone skill; 21:30 Levi asks about the Bluetooth keyboard; "what I already knew" closes the line
3. [request; disclosure] Levi's request of 2026-11-23 21:50 on a framed page, dated; Levi (circle, directs) and Alpha (hexagon, researches) named beside it
4. [scorecard; plan] The spine: three rows to fill (where did it go? how often? what fixes it?), and the evidence below: logs, runtime code, three papers, a test
5. [flow; turn] The path from store to model: stored, indexed, chosen, read, through the runtime's door; ticks on the first steps, then the read stops red at the door

## 02 The Refusal
1. [stack] The layers: the prompt with the index of fifteen lines on top, the skill files below; a line that fits points down to its file
2. [~] The phone line lit, 21:29, the read call drawn down to the phone card
3. [document] The runtime's refusal on a page, its two phrases lit: "cannot be partially served", "Ask the operator to reduce the document"
4. [cutaway] Inside the runtime's read tool: offset and limit struck for skill files; a size check: under the budget served whole, over it refused
5. [gauge; check] A rule in characters with the budget at 16,000: a 15,822 file passes green, a 16,062 file stops red
6. [~] The phone skill's bar added at 17,400 bytes, past the line, its gold line inside

## 03 Four of Four
1. [search] A search over the production log for every skill read, 10-12 to 11-24; then the question, bad luck?
2. [timeline] 10-19 the skill passes 16,000; four reads after it (10-23 twice, 11-03, 11-23), each red; the span marked 35 days
3. [unit] 52 squares, one per skill read: 48 green, 4 red, all four the phone skill
4. [side-by-side] What the runtime told the model (the refusal) beside what the model told the person (the instructions are too long), 10-23
5. [ledger; dropped] The failure catalogue's entry for that turn, "asserted, not observed", struck red; beside it, "refused by the runtime"
6. [~] Only the model's hexagon sees the refusal; the people outside see the reply alone; a month's span greyed: nobody looked

## 04 A Number in a Config
1. [flow] How the budget is set: the model's context window from the config, into the runtime's rule, out as characters per skill read
2. [bars] The budget by window: under 100,000 tokens 16,000 characters, from 100,000 32,000; Alpha's 90,000 marked under the first bar
3. [dumbbell] The window: 90,000 tokens set in the config against 1,000,000 listed by OpenRouter, dated 2026-11-24
4. [request] Levi's words of 2026-11-23 21:50, the context-limits line lit
5. [~] Beside it the config plate, contextTokens 90000: the limit was this number
6. [~] A question mark on the plate: reason not found; a cost note, a larger window costs more each turn

## 05 Three Designs
1. [search] The search for prior art: three papers land (Voyager, MemGPT, Reflexion), a chip "not a survey"
2. [diagram] Voyager: a library of programs with descriptions; the harness embeds the task and puts the top five in the prompt; "harness, not model" lit
3. [dumbbell] Voyager's Table 1: iron tools 29 against 21 iterations, diamond tools 0 of 3 against 1 of 3, without and with the library
4. [loop] MemGPT: the model pages through results in a loop, and leaves before the end of the list
5. [proportional] Reflexion: a memory of one to three reflections, all of it inside every attempt, drawn small inside the context
6. [ledger] The three and Alpha: who decides to look (harness, model, nothing to look for), and whether delivery loss is measured: none; Alpha's row beside MemGPT's

## 06 A Vector Database?
1. [request] Levi's line of 2026-11-23 21:50, "First thing that comes to mind is vector databases", lit
2. [line; counter] An illustration, dashed: knowledge growing against a fixed prompt; where they cross, "index stops fitting"; "a patch" on the split
3. [~] Voyager and MemGPT placed past the crossing, where retrieval is needed
4. [cutaway] Alpha's index opened: fifteen lines, about 5,500 characters, the phone's line lit, seen
5. [flow] The path from 01 again with a vector store at the finding step: found, chosen, still stopped red at the door

## 07 The Fix, Measured
1. [treemap] The old phone skill, 17.4 KB, against the new: a 7.6 KB core and side files, pin.md holding the gold line
2. [document] The new index line, its trigger words lit: PIN, screen unlock, Bluetooth keyboard, unlock.py
3. [gauge] The size test's cap at 9,400 bytes against the line at 16,000; each skill a tick under the cap
4. [stack] The test rig: the real runtime, Alpha's prompt files, the model route, every skill, inside a sandbox; the phone and the network outside, cut off
5. [unit] 72 dots: twelve requests, three runs each, two layouts; the cost chip, $0.42
6. [slope; check] Old to new, first phone read served: 0 of 34 to 34 of 34
7. [~] Added: told the user it was too long, 8 to 0
8. [~] Added: read through the shell, 19 old runs, marked "if it thinks to"
9. [stacked] The brief to the worker: old, the route in 6 of 19; new, 17 of 17

## 08 Close
1. [limit; limit] The path from 01 at the limit: thousands of notes, retrieval at the finding step, the same door
2. [~] Each note given a second tick, "deliverable whole"; a chip, one runtime checked
3. [scorecard; answer] The spine filled: where (refused at delivery), how often (phone skill: 4 refused; others: none), what fixes it (the split and the index line, in the test)
4. [~; unknown] Still open, three rows: production since the split, a production rate, knowledge only in notes
5. [repository; cta] The repository: the study, the requests, the scored runs and the counting script; its address; issues
