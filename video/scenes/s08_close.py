"""
Section 08: the close. The path at the limit (a store of notes too many to index, retrieval at the finding step, the
same door and budget); the pieces it finds, each needing a second tick, "deliverable whole", with one runtime checked;
the spine answered; what is still open; and the repository card.

The limit is an illustration: its store is dashed and its notes are not counted. The counts are data.py's.
"""
from __future__ import annotations

from manim import *

import data
import style
from pipeline import stage
from pipeline.beats import Beat, BeatScene

REPO_URL = "https://github.com/purdy-agent-alpha/004-found-not-delivered"
# What the repository holds, as the narration lists it (README.md names these paths).
REPO_FILES = (("report/report.md", "the study"), ("experiment/prompts.json", "the requests"),
              ("experiment/runs.jsonl", "every scored run"), ("experiment/table.py", "the counting script"))
REFUSED = len(data.REFUSED_READS)
ANSWERS = ("refused at delivery", f"phone skill: {REFUSED} refused; others: none", "the split and the index line, in the test")
OPEN = (("production since the split", "no phone read yet"),
        ("a production rate", f"{data.TOTAL_RUNS} runs, mostly my requests"),
        ("knowledge only in notes", "the next test"))

# The path, left to right: the store, the finding step, the door, Alpha; the read runs along PATH_Y.
STORE_X, FIND_X, DOOR_X, ALPHA_X, PATH_Y, RULE_Y, MID_Y = -4.9, -1.6, 2.9, 5.7, -0.15, 0.75, 0.35


def note(width: float = 0.16, height: float = 0.2, color: str = style.MUTED) -> Rectangle:
    """One note in the store: a small filled page."""
    return Rectangle(width=width, height=height).set_fill(color, opacity=0.55).set_stroke(width=0)


def store() -> VGroup:
    """Notes too many to list, in a dashed frame (an illustration), named below. VGroup(frame, notes, word)."""
    notes = VGroup(*[note() for _ in range(14 * 9)]).arrange_in_grid(rows=9, cols=14, buff=0.06)
    frame = style.card(notes.width + 0.4, notes.height + 0.4, style.MUTED, dashed=True).move_to(notes)
    # At caption size: at label size "of" sets its word gaps too tight to read apart.
    word = style.caption_text("thousands of notes", color=style.MUTED).next_to(frame, DOWN, buff=0.22)
    return VGroup(frame, notes, word)


def index_box() -> VGroup:
    """The index in the prompt, its lines running out of the box. VGroup(box, inside, spill, word)."""
    box = style.card(1.5, 1.9, style.MUTED)
    lines = VGroup(*[Line(LEFT * 0.45, RIGHT * (0.45 if i % 3 else 0.15), color=style.MUTED, stroke_width=2.4)
                     for i in range(12)]).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
    lines.next_to(box.get_top(), DOWN, buff=0.22).align_to(box.get_left() + RIGHT * 0.3, LEFT)
    inside = VGroup(*[ln for ln in lines if ln.get_bottom()[1] > box.get_bottom()[1] + 0.12])
    spill = VGroup(*[ln.set_stroke(style.DIM) for ln in lines[len(inside):]])
    word = style.label_text("index", color=style.MUTED).next_to(box, UP, buff=0.2)
    return VGroup(box, inside, spill, word)


def gate() -> VGroup:
    """The door with the budget rule across its opening, its size beside the right post. VGroup(door, rule, size)."""
    door = style.door(height=2.1, width=1.3)
    rule = Line(LEFT * 0.56, RIGHT * 0.56, color=style.BUDGET, stroke_width=5)
    size = style.mono_text(f"{data.BUDGET_CHARS:,}", color=style.BUDGET, size="tiny")
    group = VGroup(door, rule, size).move_to([DOOR_X, MID_Y, 0])
    rule.set_y(RULE_Y)
    size.next_to(door[1], RIGHT, buff=0.16).set_y(RULE_Y)
    return group


def piece(color: str = style.WHITE) -> VGroup:
    """A piece the finding step hands on: a small page with two rules."""
    body = RoundedRectangle(corner_radius=0.04, width=0.34, height=0.44, color=color)
    body.set_fill(style.PANEL_HI, opacity=0.96).set_stroke(color, width=2.0)
    rules = VGroup(*[Line(LEFT * 0.09, RIGHT * 0.09, color=style.MUTED, stroke_width=1.6) for _ in range(2)])
    return VGroup(body, rules.arrange(DOWN, buff=0.1).move_to(body))


def checklist() -> VGroup:
    """Three found pieces, a tick each for found, a slot for the second tick. VGroup(heads, rows); each row
    VGroup(piece, tick, second tick)."""
    heads = VGroup(style.label_text("found", color=style.MUTED),
                   style.label_text("deliverable whole", color=style.MUTED))
    rows = VGroup()
    for _ in range(3):
        rows.add(VGroup(piece(), style.tick(style.WHITE), style.tick(style.SERVED)))
    for row in rows:
        row[1].move_to(row[0]).shift(RIGHT * 1.1)
        row[2].move_to(row[0]).shift(RIGHT * 3.3)
    rows.arrange(DOWN, buff=0.3)
    heads[0].next_to(rows[0][1], UP, buff=0.35)
    heads[1].next_to(rows[0][2], UP, buff=0.35)
    style.sit(heads[0], style.baseline(heads[1]))
    return VGroup(heads, rows)


def answer_mark(i: int) -> VMobject:
    """What each answer points back to: the stop bar, the four refused reads, the tick of the fix."""
    if i == 0:
        return style.stop_bar(height=0.4)
    if i == 1:
        return VGroup(*[style.run_dot(False, radius=0.08) for _ in range(REFUSED)]).arrange(RIGHT, buff=0.08)
    return style.tick(style.SERVED)


def open_row(question: str, state: str, width: float) -> VGroup:
    """One open question on its band: its words at the left, a dashed slot at the right with what is known so far.
    VGroup(words, VGroup(slot, known), band)."""
    words = style.label_text(question)
    known = style.label_text(state, color=style.MUTED)
    slot = DashedVMobject(RoundedRectangle(corner_radius=0.06, width=known.width + 0.5, height=0.5,
                                           color=style.MUTED).set_stroke(style.MUTED, width=1.6), num_dashes=40)
    known.move_to(slot)
    row = VGroup(words, VGroup(slot, known))
    words.move_to(LEFT * width / 2, aligned_edge=LEFT)
    row[1].move_to(RIGHT * width / 2, aligned_edge=RIGHT)
    style.sit(words, style.baseline(known))
    return row.add(style.band(width + 0.6, 0.56).move_to([0, slot.get_y(), 0]))


class S08Close(BeatScene):
    """08: the path at the limit, a second tick per piece, the spine answered, what is open, the repository."""

    section_id = "08_close"
    title = "Close"

    def storyboard(self) -> list[Beat]:
        return [
            Beat("Push it to the limit: thousands of notes", self.b_limit, kind="limit"),
            Beat("So my guess is that every store like this", self.b_check),
            Beat("So, did I forget? No.", self.b_spine, kind="scorecard"),
            Beat("Still open: the split hasn't met production", self.b_open),
            Beat("The study, the requests, every scored run", self.b_repo, kind="repository"),
        ]

    # --------------------------------------------------------------- 1 limit --
    def b_limit(self, ctx):
        notes = store().move_to([STORE_X, MID_Y - 0.15, 0])
        door, me = gate(), style.alpha(size=0.95).move_to([ALPHA_X, PATH_Y, 0])
        ctx.play(Create(notes[0]), LaggedStart(*[FadeIn(n) for n in notes[1]], lag_ratio=0.01), FadeIn(notes[2]),
                 FadeIn(door), FadeIn(me), run_time=1.2)
        self._owned.update(store=notes, door=door, me=me)
        # "and an index that no longer fits": its lines run past the bottom of the box.
        index = index_box().move_to([FIND_X, MID_Y, 0])
        ctx.play(FadeIn(index[0]), FadeIn(index[3]), LaggedStart(*[Create(ln) for ln in index[1]], lag_ratio=0.3),
                 run_time=ctx.at(0.12, 1.0))
        ctx.play(LaggedStart(*[FadeIn(ln, shift=DOWN * 0.15) for ln in index[2]], lag_ratio=0.35),
                 run_time=ctx.at(0.24, 1.2))
        # "Then retrieval by meaning is needed": the index gives way to a finding step that picks a few notes.
        finder = style.node("step", "retrieval", size=1.35).move_to([FIND_X, PATH_Y, 0])
        ctx.play(FadeOut(index), run_time=ctx.at(0.4, 0.3))
        ctx.play(FadeIn(finder), run_time=0.4)
        picked = VGroup(*[notes[1][i] for i in (21, 70, 115)])
        ctx.play(*[n.animate.set_fill(style.WHITE, opacity=1) for n in picked], run_time=0.5)
        feed = style.glow_arrow([notes[0].get_right()[0] + 0.1, PATH_Y, 0], [finder.get_left()[0] - 0.1, PATH_Y, 0],
                                color=style.MUTED)
        ctx.show(feed, tag="feed", anim=Create, run_time=0.5)
        self._owned["finder"] = finder
        # "But whatever finds a piece, the runtime still has to hand it over whole": a piece goes under the rule.
        self.deliver(ctx, finder, me)

    def deliver(self, ctx, finder: Mobject, me: Mobject):
        start, end = [finder.get_right()[0] + 0.1, PATH_Y, 0], [me.get_left()[0] - 0.05, PATH_Y, 0]
        path = style.read_path(start, end, served=True)
        one = piece().move_to(start)
        ctx.play(FadeIn(one, scale=0.6), run_time=ctx.at(0.66, 0.3))
        ctx.play(Create(path), one.animate.move_to([end[0] - 0.4, PATH_Y + 0.4, 0]), run_time=ctx.at(0.68, 1.6),
                 rate_func=linear)
        self._owned["path"], self._owned["one"] = path, one
        door = self._owned["door"]
        ctx.play(*style.highlight(door[0][0], style.RUNTIME), *style.highlight(door[0][1], style.RUNTIME),
                 run_time=ctx.at(0.86, 0.5))

    # --------------------------------------------------------------- 2 check --
    def b_check(self, ctx):
        ctx.retire("feed", "path", "one", "finder", run_time=0.4)
        table = checklist()
        heads, rows = table
        table.shift([-2.5 - rows[0][0].get_x(), MID_Y - rows.get_y(), 0])
        ctx.play(*[FadeIn(r[0], shift=RIGHT * 0.2) for r in rows], *[Create(r[1]) for r in rows], FadeIn(heads[0]),
                 run_time=0.6)
        self._owned["table"] = table
        ctx.play(FadeIn(heads[1]), run_time=ctx.at(0.18, 0.4))
        # "a check that each piece can still be delivered": a second tick, one piece at a time.
        for row, frac in zip(rows, (0.26, 0.38, 0.5)):
            ctx.play(Create(row[2]), run_time=ctx.at(frac, 0.45))
        # "I've checked one runtime."
        chip = style.boxed(style.label_text("one runtime checked"), style.RUNTIME, pad=(0.44, 0.3))
        chip.next_to(self._owned["door"], DOWN, buff=0.3).set_x(DOOR_X)
        ctx.show(chip, tag="chip", run_time=ctx.at(0.72, 0.5))

    # --------------------------------------------------------------- 3 spine --
    def b_spine(self, ctx):
        ctx.clear_stage(run_time=0.4)
        rows = style.spine(lit=None, width=12.4)
        rows.arrange(DOWN, buff=0.62, aligned_edge=LEFT)
        stage.fit(rows, stage.STAGE)
        rows.shift(UP * 0.3)
        for row in rows:
            row.add(style.band(13.0, 0.56).move_to([0, row.get_y(), 0]))
        ctx.play(LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.15), run_time=0.8)
        self._owned["spine"] = rows
        # "found, chosen, and refused at the door" / "four times in four" / "Splitting the file fixed it".
        for i, frac in enumerate((0.3, 0.5, 0.8)):
            self.fill(ctx, rows[i], i, frac)

    def fill(self, ctx, row: VGroup, i: int, frac: float):
        """Swap row i's dashed slot for its answer and the mark it points back to."""
        answer = VGroup(answer_mark(i), style.label_text(ANSWERS[i])).arrange(RIGHT, buff=0.25)
        slot = row[2]
        answer.move_to(slot).align_to(slot, RIGHT)
        answer.shift(UP * (style.baseline(row[1]) - style.baseline(answer[1])))
        answer[0].set_y(answer[1].get_center()[1])
        row.remove(slot)
        self.add(slot)
        ctx.play(FadeOut(slot), FadeIn(answer, shift=LEFT * 0.15), run_time=ctx.at(frac, 0.6))
        self._owned[f"answer{i}"] = answer

    # ---------------------------------------------------------------- 4 open --
    def b_open(self, ctx):
        # The spine and its answers rise to make room; what is still open fills in under them.
        spine, moves = self._owned["spine"], []
        for i, row in enumerate(spine):
            dy = UP * (2.0 - 0.62 * i - row.get_y())
            moves += [row.animate.shift(dy), self._owned[f"answer{i}"].animate.shift(dy)]
        ctx.play(*moves, run_time=0.6)
        rows = VGroup(*[open_row(q, s, 12.4) for q, s in OPEN]).arrange(DOWN, buff=0.22, aligned_edge=LEFT)
        rows.move_to([0, -1.36, 0])
        head = style.label_text("still open", color=style.MUTED).next_to(rows, UP, buff=0.28).align_to(rows, LEFT)
        # The three open questions at once, their slots empty; what is known of each as it is spoken.
        ctx.play(FadeIn(head), LaggedStart(*[AnimationGroup(FadeIn(r[2]), FadeIn(r[0], shift=RIGHT * 0.15), Create(r[1][0]))
                                             for r in rows], lag_ratio=0.3), run_time=1.0)
        self._owned["head"], self._owned["open"] = head, rows
        for i, frac in enumerate((0.12, 0.45, 0.7)):
            ctx.play(FadeIn(rows[i][1][1]), Indicate(rows[i][0], color=style.WHITE, scale_factor=1.05),
                     run_time=ctx.at(frac, 0.6))
            ctx.play(Indicate(rows[i][1], color=style.WHITE, scale_factor=1.05), run_time=ctx.at(frac + 0.15, 0.6))

    # ---------------------------------------------------------------- 5 repo --
    def b_repo(self, ctx):
        ctx.clear_stage(run_time=0.4)
        files = VGroup()
        for name, what in REPO_FILES:
            path = style.mono_text(name, size="label")
            files.add(VGroup(path, style.label_text(what, color=style.MUTED)))
        for f in files:
            f[1].move_to([0.9, 0, 0], aligned_edge=LEFT)
            f[0].move_to([0.5, 0, 0], aligned_edge=RIGHT)
        files.arrange(DOWN, buff=0.3).move_to([0.2, 0.25, 0])
        for f in files:
            style.sit(f[1], style.baseline(f[0]))
        frame = style.card(files.width + 1.0, files.height + 0.8, style.MUTED).move_to(files)
        ctx.play(FadeIn(frame), run_time=0.4)
        self._owned["frame"] = frame
        url = style.mono_text(REPO_URL, size="label").next_to(frame, UP, buff=0.4)
        ctx.show(url, tag="url", anim=lambda m: FadeIn(m, shift=DOWN * 0.1), run_time=0.5)
        for i, (f, frac) in enumerate(zip(files, (0.06, 0.14, 0.22, 0.3))):
            ctx.play(FadeIn(f, shift=RIGHT * 0.15), run_time=ctx.at(frac, 0.4))
            self._owned[f"file{i}"] = f
        ctx.play(Create(style.underline(url, gap=0.13)), run_time=ctx.at(0.45, 0.6))
        issue = style.label_text("Found a mistake? Open an issue").next_to(frame, DOWN, buff=0.4)
        ctx.show(issue, tag="issue", run_time=ctx.at(0.6, 0.5))
