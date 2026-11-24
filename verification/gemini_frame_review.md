# Gemini frame review — 2026-11-24

Model: `models/gemini-3.1-pro-preview`  
One settled frame per beat, paired with the narration line it is cued to.
The geometry gate had already passed every section clean, so everything
below is a judgement call rather than a defect.

## 1 · Open

01 b02 | BLOCKING | MISMATCH | The gold underline in the chat bubble violates the strict rule that gold only represents the PIN route.
01 b04 | WORTH-FIX | MISSED | The narration mentions testing a fix, but this action is not depicted on screen.
01 b05 | BLOCKING | MISMATCH | The path to the runtime door uses gold, violating the rule that gold is strictly reserved for the PIN route knowledge.
01 b05 | WORTH-FIX | MISSED | The scorecard spine is missing from the frame where the narration explicitly provides the first answer.

## 2 · The Refusal

02 b01 | BLOCKING | MISMATCH | The prompt index is drawn as a horizontal row, contradicting the shape grammar that explicitly defines it as a vertical column.
02 b04 | BLOCKING | MISMATCH | The runtime and budget are drawn as generic diagram nodes instead of the required blue door and cyan rule.
02 b06 | BLOCKING | MISMATCH | The phone skill size is labeled in bytes but plotted directly onto a chart axis that measures characters.

## 3 · Four of Four

03 b02 | BLOCKING | MISMATCH | The dots representing the four refused reads are white, but the grammar requires them to be red for runs where the knowledge did not get through.
03 b04 | BLOCKING | MISMATCH | The refused read is drawn as a blue arrow from the runtime, instead of a path from a skill stopped at the door with a red bar.
03 b06 | BLOCKING | MISMATCH | Alpha is drawn sending messages to two separate person circles, but the grammar defines only one person character.
03 b06 | WORTH-FIX | COMPOSITION | The isolated table row at the top is left over from the previous beat and clutters the new diagram.

## 4 · A Number in a Config

04 b01 | BLOCKING | MISMATCH | The cyan budget rule is drawn beside the runtime door instead of across its opening as the shape grammar requires.
04 b02 | BLOCKING | MISSED | The chart omits the 32,000-character budget for models at or above 100,000 tokens, missing the second half of the rule described in the line.
04 b06 | BLOCKING | MISMATCH | The statement about cost is wrapped in a white-stroked box, introducing an arbitrary container shape not defined in the video's grammar.

## 5 · Three Designs

05 b02 | BLOCKING | SEMANTIC MISMATCH | The white hexagon is exclusively reserved for Alpha, but is used here for Voyager's model.
05 b02 | BLOCKING | SEMANTIC MISMATCH | The unselected skill cards use a violet stroke, violating the rule that skills must have a white stroke.
05 b02 | WORTH-FIX | MISSED OPPORTUNITY | The visual leaves the prompt slots empty instead of showing the five fetched skills arriving.
05 b03 | BLOCKING | MISSED OPPORTUNITY | The diamond tools chart completely omits the data point for the single successful run with the library.
05 b04 | BLOCKING | SEMANTIC MISMATCH | A white hexagon is used for MemGPT's model, violating the grammar rule that reserves this shape solely for Alpha.
05 b05 | BLOCKING | SEMANTIC MISMATCH | The memory card is drawn with a violet stroke, incorrectly styling it as a published paper.

## 6 · A Vector Database?

06 b02 | BLOCKING | MISSED | The narration mentions splitting one file as a patch, but no corresponding visual appears in this frame.
06 b03 | BLOCKING | MISMATCH | The label "split one file: a patch" appears here but illustrates the narration from the previous beat.

## 7 · The Fix, Measured

07 b01 | WORTH-FIX | MISSED OPPORTUNITY | The narration specifies "under eight kilobytes", so adding a label under the new core SKILL.md showing its size would ground the claim.
07 b02 | BLOCKING | SEMANTIC MISMATCH | The frame shows a large block of text instead of the "index" shape defined in the grammar as a column of short grey lines in monospace.
07 b02 | WORTH-FIX | MISSED OPPORTUNITY | The narration explicitly names "the unlock script's name" as a trigger word, but "unlock.py" is not underlined like the others.
07 b03 | BLOCKING | SEMANTIC MISMATCH | The frame uses checkmarks to count successful test runs, but the shape grammar strictly requires runs to be drawn as dots.
07 b04 | BLOCKING | SEMANTIC MISMATCH | The prompt files are drawn as plain white squares, which the shape grammar reserves exclusively for "worker" agents.
07 b06 | BLOCKING | SEMANTIC MISMATCH | The 0 of 34 data point representing failed reads is colored green, but the grammar reserves green for successful reads and red for failed ones.

07 b07 | WORTH-FIX | MISSED OPPORTUNITY | The slope chart is missing the final data point and "0" label on the "new" side, failing to visually resolve the "none did" claim.
07 b08 | BLOCKING | SEMANTIC MISMATCH | The slope chart's Y-axis is distorted because the red "0 of 36" point on the right is positioned physically higher than the green "0 of 34" point on the left.
07 b09 | BLOCKING | MISSED OPPORTUNITY | The bottom row of brief cards lacks a text label for "17 of 17" to parallel the top row and explicitly reinforce the narrated count.

## 8 · Close

08 b01 | WORTH-FIX | COMPOSITION | A detached horizontal stroke floats arbitrarily between the notes grid and the retrieval box, appearing to be a broken connector.
08 b03 | BLOCKING | MISMATCH | The narration explicitly answers the third question ("Splitting the file fixed it"), but the scorecard's third row incorrectly remains an empty dashed box.

