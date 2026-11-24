# Thinking before the script

Written before the script, and kept beside it. The research itself was done first (report/report.md); this page is
the thinking the video is built on.

## First principles

An agent's operational knowledge (how to unlock its phone, which tool to use, what went wrong last time) has to make
three trips before it changes what the agent does. It has to be stored somewhere. The agent has to be pointed at it:
an index line, a retrieval hit, a memory it chooses to look up. And it has to be delivered: the bytes have to arrive in
the model's context whole enough to act on. A loss at any of the three looks the same from outside, an agent that
"forgot". So the question "did it forget?" has to be split: was the knowledge in the store, did anything point the
agent at it, did the agent look, and did the read succeed? Each can be measured: the store by reading the files, the
pointing by reading the index, the looking and the delivery by reading the agent's own tool calls and what the runtime
answered. Only the last one needs the runtime's log rather than the model's account, because the model reports a
failed read in its own words.

## In the limit

Push the store to its limit: thousands of notes, skills and memories, far more than an index in the prompt can list.
Then the pointing step must become retrieval (by embedding, by keyword, by the model paging), and that is where vector
databases belong; Voyager and MemGPT use them exactly there. But retrieval only moves the pointing step. Whatever finds
a piece, the piece still has to be delivered through a context budget, and as the store grows its pieces grow too. So
at the limit, every piece needs two properties checked, not one: it can be found, and it can still be delivered whole.
What breaks first in a small system like Alpha's (fifteen skills, all listed) is delivery, not finding. What breaks
first in a large one is finding, and then delivery behind it. The implication now: before adding retrieval, check that
everything already found can be delivered.

## The strongest counterargument

Context is finite and knowledge keeps growing, so loss of this kind is bound to happen (Levi's own starting point). A
fix that splits one file is a patch on one symptom: next month another file grows, or the index itself stops fitting,
and the real answer is retrieval by meaning, a vector database over everything the agent knows. Splitting files also
adds hops: each side file is one more read the model must choose to make, and in an earlier simulated test two of three
misses stopped before reading the side file.

Answer: tested and partly holds. On this failure the counterargument is wrong about the cause: the skill was found,
chosen and refused at delivery, four reads of four, by a budget set from a local configuration, and retrieval would
have handed the same file to the same refusal. It is right about the future: the index will stop fitting one day, and
knowledge that lives only in notes (where the loss is not looking) was not tested; the close says so. The side-file
cost is real and measured: the new layout takes a median of two more tool calls before deciding.
