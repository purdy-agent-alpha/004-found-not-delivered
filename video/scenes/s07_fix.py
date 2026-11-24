"""
Section 07: the fix, measured. The old phone skill split into a core and pin.md, the gold line moving with it; the new
index line with its trigger words lit; the size test's cap on a gauge under the budget; the test rig in its sandbox;
the 72 runs as dots; the three counts on one slope, old to new; and the worker's brief, old and new, as rows of cards.

Every number is data.py's. The side files beside pin.md (flows.md, updates.md) are named, not sized: data.py does not
carry their sizes. Every wait inside a beat is a fraction of its window (`ctx.at`).
"""
from __future__ import annotations

from manim import *

import data
import style
from pipeline import stage
from pipeline.beats import Beat, BeatScene

# The new index line (scene brief), shortened with "...", wrapped so no trigger word breaks.
INDEX_ROWS = ("Drive Alpha's Moto G Power 5G Android phone via",
              "Mobile MCP and ADB. Use for any phone job - the",
              "phone lock (take it first), PIN, screen unlock,",
              "Bluetooth keyboard (bthid), phone restart or",
              "gone from USB (unlock.py), ...")
# The trigger words, as (row, phrase), in the order the narration names them.
TRIGGERS = ((2, "PIN"), (2, "screen unlock"), (3, "Bluetooth keyboard"), (4, "unlock.py"))


def kb(size: int) -> str:
    return f"{size / 1000:.1f} KB"


def count(n: int, of: int) -> str:
    return f"{n} of {of}"


def glyphs(text: Text, source: str, phrase: str) -> VGroup:
    """The glyphs of `phrase` inside a Text built from `source` (a Text holds no glyph for a space)."""
    at = source.index(phrase)
    first = len(source[:at].replace(" ", ""))
    return VGroup(*text.submobjects[first:first + len(phrase.replace(" ", ""))])


def sized_card(name: str, size: int, unit: float, route: bool = False) -> VGroup:
    """A skill file whose height is its size in bytes."""
    return style.skill_card(name, width=1.6, height=size * unit, route=route)


def index_card() -> VGroup:
    """The phone skill's new index line on a page: VGroup(card, rows), the rows grey until lit."""
    rows = style.text_rows(*[style.mono_text(r, color=style.MUTED, size="label") for r in INDEX_ROWS])
    head = style.mono_text("- phone:", color=style.WHITE, size="label")
    body = VGroup(head, rows).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
    return VGroup(style.card(body.width + 0.9, body.height + 0.7, style.MUTED).move_to(body), body)


def gauge(x0: float, x1: float, y: float, top: int, refused_from: int):
    """A track in bytes from 0 to `top`, red from `refused_from` up; returns (track group, x of a value)."""
    at = lambda v: x0 + (x1 - x0) * v / top
    ok = style.tile(at(refused_from) - x0, 0.36, style.MUTED, opacity=0.45).move_to([x0, y, 0], aligned_edge=LEFT)
    over = style.tile(x1 - at(refused_from), 0.36, style.REFUSED, opacity=0.45).next_to(ok, RIGHT, buff=0)
    zero = style.mono_text("0", color=style.MUTED, size="tiny").next_to(ok, DOWN, buff=0.18).align_to(ok, LEFT)
    return VGroup(ok, over, zero), at


def mark(x: float, y: float, height: float, color: str, words: str, width: float = 5.0) -> VGroup:
    """A vertical line up across the track at x, its value on top: the budget, the cap."""
    line = Line([x, y, 0], [x, y + height, 0], color=color, stroke_width=width)
    return VGroup(line, style.mono_text(words, color=color, size="tiny").next_to(line, UP, buff=0.16))


def marker(x: float, y: float, color: str, words: str) -> VGroup:
    """A file's size on the track: a short tick down from it, its name below."""
    line = Line([x, y, 0], [x, y - 0.3, 0], color=color, stroke_width=5)
    return VGroup(line, style.mono_text(words, color=color, size="tiny").next_to(line, DOWN, buff=0.14))


def mini_skill() -> VGroup:
    """A skill too small for its name: a white page with two grey rules."""
    body = RoundedRectangle(corner_radius=0.04, width=0.3, height=0.4, color=style.WHITE)
    body.set_fill(style.PANEL_HI, opacity=0.96).set_stroke(style.WHITE, width=1.8)
    rules = VGroup(*[Line(LEFT * 0.08, RIGHT * 0.08, color=style.MUTED, stroke_width=1.6) for _ in range(2)])
    return VGroup(body, rules.arrange(DOWN, buff=0.08).move_to(body))


def page(width: float = 0.42, height: float = 0.55) -> VMobject:
    """One of Alpha's prompt files: a grey page."""
    return style.card(width, height, style.MUTED, radius=0.05)


def phone_shape() -> VGroup:
    """The phone, outside the sandbox: a grey handset with its word below."""
    body = RoundedRectangle(corner_radius=0.12, width=0.6, height=1.05, color=style.MUTED)
    body.set_fill(style.PANEL_HI, opacity=0.96).set_stroke(style.MUTED, width=2.2)
    screen = RoundedRectangle(corner_radius=0.05, width=0.44, height=0.72, color=style.DIM).set_stroke(width=1.4)
    return VGroup(body, screen.move_to(body).shift(UP * 0.04))


def rig_layers() -> VGroup:
    """Inside the sandbox, top to bottom: Alpha's prompt files and model, the real runtime, every skill."""
    files = VGroup(*[page() for _ in range(3)]).arrange(RIGHT, buff=0.14)
    model = style.alpha(size=0.85)
    top = VGroup(files, model).arrange(RIGHT, buff=0.6)
    gate = style.door(height=0.85, width=1.0, label=False)
    skills = VGroup(*[mini_skill() for _ in range(data.INDEX_SKILLS)]).arrange(RIGHT, buff=0.1)
    return VGroup(top, gate, skills).arrange(DOWN, buff=0.42)


def run_blocks() -> VGroup:
    """The 72 runs before scoring: per layout a block, a request a column, its runs down it. VGroup(old, new) of
    columns."""
    def block():
        return VGroup(*[VGroup(*[Dot(radius=0.12, color=style.MUTED) for _ in range(data.SAMPLES)])
                        .arrange(DOWN, buff=0.12) for _ in range(data.REQUESTS)]).arrange(RIGHT, buff=0.14)
    return VGroup(block(), block()).arrange(DOWN, buff=0.6)


def brief_row(carried: int, total: int) -> VGroup:
    """Briefs handed to a worker, one card each, those carrying the route first."""
    return VGroup(*[style.brief_card(i < carried, width=0.42, height=0.5) for i in range(total)]).arrange(
        RIGHT, buff=0.08)


class S07Fix(BeatScene):
    """07: the split, the index line, the size test, the rig, the 72 runs, three counts old to new, the brief."""

    section_id = "07_the_fix_measured"
    title = "The Fix, Measured"

    # The slope: the old column, the new column, the floor and a run's height on it.
    OLD_X, NEW_X, FLOOR, RUN_H = -0.4, 3.8, -1.75, 3.3 / data.OLD["runs"]

    def storyboard(self) -> list[Beat]:
        return [
            Beat("The fix was small. Split the phone skill", self.b_split, kind="treemap"),
            Beat("Put the trigger words in its index line", self.b_index, kind="document"),
            Beat("And add a test that fails any skill", self.b_cap, kind="gauge"),
            Beat("Then I tested it through the real runtime", self.b_rig, kind="stack"),
            Beat("Twelve requests: Levi's two from that night", self.b_runs, kind="unit"),
            Beat("Of the thirty-four old runs that read the phone skill", self.b_served, kind="slope"),
            Beat("Eight old runs told the user", self.b_too_long),
            Beat("Nineteen of the thirty-six old runs also read", self.b_shell),
            Beat("The plainest number is the brief I hand a worker", self.b_brief, kind="stacked"),
        ]

    # --------------------------------------------------------------- 1 split --
    def b_split(self, ctx):
        unit, base = 3.5 / data.OLD_SKILL_BYTES, -1.45
        old = sized_card("SKILL.md", data.OLD_SKILL_BYTES, unit, route=True).move_to([0, base, 0],
                                                                                    aligned_edge=DOWN)
        old_kb = style.label_text(kb(data.OLD_SKILL_BYTES)).next_to(old, DOWN, buff=0.24)
        whole = ctx.show(old, old_kb, tag="old", run_time=0.6)
        # "Split the phone skill": the old file steps aside, the core comes out of it.
        ctx.play(whole.animate.shift(LEFT * 3.0), run_time=ctx.at(0.22, 0.6))
        core = sized_card("SKILL.md", data.NEW_CORE_BYTES, unit).move_to([1.0, base, 0], aligned_edge=DOWN)
        pin = sized_card("pin.md", data.PIN_BYTES, unit, route=True).move_to([3.0, base, 0], aligned_edge=DOWN)
        arrow = style.glow_arrow([old.get_right()[0] + 0.25, 0.3, 0], [core.get_left()[0] - 0.12, 0.3, 0],
                                 color=style.MUTED)
        ctx.show(core, tag="core", anim=lambda m: FadeIn(m, shift=RIGHT * 0.3), run_time=0.5)
        ctx.show(arrow, tag="arrow", anim=lambda m: FadeIn(m, shift=RIGHT * 0.2), run_time=0.4)
        # "and the PIN route in a file of its own": the gold line leaves the old file for pin.md.
        run_time = ctx.at(0.55, 1.0)
        pin.route.set_stroke(opacity=0)
        moving = old.route.copy()
        self._owned["pin"] = pin
        ctx.play(FadeIn(pin), moving.animate.move_to(pin.route).set_width(pin.route.width), run_time=run_time)
        self.remove(moving)
        pin.route.set_stroke(opacity=1)
        sizes = VGroup(style.label_text(kb(data.NEW_CORE_BYTES)).next_to(core, DOWN, buff=0.24),
                       style.label_text(kb(data.PIN_BYTES)).next_to(pin, DOWN, buff=0.24))
        sides = style.text_rows(*[style.mono_text(n, color=style.MUTED, size="tiny") for n in ("flows.md",
                                                                                              "updates.md")])
        sides.next_to(pin, RIGHT, buff=0.4).align_to(pin, DOWN)
        ctx.play(old.animate.set_opacity(0.55), run_time=ctx.at(0.72, 0.4))
        ctx.show(sizes, sides, tag="sizes", run_time=0.5)

    # --------------------------------------------------------------- 2 index --
    def b_index(self, ctx):
        ctx.clear_stage(run_time=0.4)
        doc = index_card()
        stage.fit(doc, stage.STAGE)
        rows = doc[1][1]
        ctx.play(FadeIn(doc[0]), FadeIn(doc[1][0]), run_time=0.4)
        ctx.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.1) for r in rows], lag_ratio=0.3), run_time=1.2)
        self._owned["index"] = doc
        for (row, phrase), frac in zip(TRIGGERS, (0.42, 0.52, 0.64, 0.8)):
            lit = glyphs(rows[row], INDEX_ROWS[row], phrase)
            under = Line(lit.get_corner(DL), lit.get_corner(DR), color=style.WHITE, stroke_width=3)
            under.shift(DOWN * 0.12)
            ctx.play(*[g.animate.set_color(style.WHITE) for g in lit], Create(under), run_time=ctx.at(frac, 0.4))
            self._owned[f"under_{phrase}"] = under

    # ----------------------------------------------------------------- 3 cap --
    def b_cap(self, ctx):
        ctx.clear_stage(run_time=0.4)
        y = 0.5
        track, at = gauge(-5.6, 5.6, y, 18_000, data.BUDGET_CHARS)
        bottom = y - 0.18
        budget = mark(at(data.BUDGET_CHARS), bottom, 1.55, style.BUDGET, f"{data.BUDGET_CHARS:,}")
        ctx.show(track, tag="track", run_time=0.5)
        ctx.show(budget, tag="budget", anim=lambda m: GrowFromEdge(m, DOWN), run_time=0.5)
        ctx.show(marker(at(data.OLD_SKILL_BYTES), bottom, style.REFUSED, "old SKILL.md"), tag="old", run_time=0.4)
        # "a test that fails any skill's main file over 9,400 bytes".
        cap = mark(at(data.SIZE_CAP_BYTES), bottom, 1.55, style.WHITE, f"size test: {data.SIZE_CAP_BYTES:,}", width=4)
        ctx.show(cap, tag="cap", anim=lambda m: GrowFromEdge(m, DOWN), run_time=ctx.at(0.3, 0.6))
        ctx.show(marker(at(data.NEW_CORE_BYTES), bottom, style.SERVED, "new SKILL.md"), tag="new",
                 run_time=ctx.at(0.42, 0.4))
        # "well under the line": every skill's main file passes, a tick each, under the cap.
        ticks = VGroup(*[style.tick(style.SERVED) for _ in range(data.OWN_SKILLS)]).arrange(RIGHT, buff=0.16)
        ticks.move_to([at(0) + ticks.width / 2 + 0.1, y - 1.6, 0])
        word = style.label_text("every skill", color=style.MUTED).next_to(ticks, RIGHT, buff=0.35)
        ctx.play(LaggedStart(*[Create(t) for t in ticks], lag_ratio=0.25), run_time=ctx.at(0.56, 1.6))
        ctx.show(word, tag="word", run_time=0.4)
        self._owned["ticks"] = ticks

    # ----------------------------------------------------------------- 4 rig --
    def b_rig(self, ctx):
        ctx.clear_stage(run_time=0.4)
        layers = rig_layers().move_to([-0.4, -0.2, 0])
        box = style.card(layers.width + 3.5, 4.4, style.MUTED).move_to([-1.0, 0.0, 0])
        name = style.label_text("sandbox, no network", color=style.MUTED)
        name.next_to(box.get_corner(UL), DR, buff=0.2)
        words = VGroup(*[style.label_text(w, color=style.MUTED).next_to(layer, LEFT, buff=0.35)
                         for w, layer in zip(("my prompt files", "the real runtime", "every skill"), layers)])
        ctx.play(Create(box), FadeIn(name), run_time=0.6)
        self._owned["box"] = VGroup(box, name)
        for i, frac in enumerate((0.1, 0.3, 0.45)):
            ctx.play(FadeIn(layers[i], shift=DOWN * 0.1), FadeIn(words[i]), run_time=ctx.at(frac, 0.6))
        self._owned["layers"], self._owned["words"] = layers, words
        # "so nothing could reach the phone": the phone outside, its line cut at the wall.
        phone = phone_shape().move_to([5.4, 0.4, 0])
        word = style.label_text("phone", color=style.MUTED).next_to(phone, DOWN, buff=0.2)
        ctx.show(phone, word, tag="phone", run_time=ctx.at(0.72, 0.5))
        wall = box.get_right()[0]
        reach = DashedLine([wall + 0.15, 0.4, 0], [phone.get_left()[0] - 0.15, 0.4, 0], color=style.MUTED,
                           stroke_width=2.6, dash_length=0.12)
        gap = Line([wall + 0.55, 0.4, 0], [wall + 1.05, 0.4, 0], stroke_width=10, color=style.BG)
        ctx.show(reach, tag="reach", anim=Create, run_time=ctx.at(0.8, 0.5))
        cut = VGroup(Line(UL, DR), Line(DL, UR)).scale(0.12).set_stroke(style.MUTED, width=3)
        ctx.play(FadeIn(gap), FadeIn(cut.move_to(gap)), run_time=ctx.at(0.88, 0.4))
        self._owned["cut"] = VGroup(gap, cut)

    # ---------------------------------------------------------------- 5 runs --
    def b_runs(self, ctx):
        ctx.clear_stage(run_time=0.4)
        blocks = run_blocks().move_to([-0.2, 0.3, 0])
        heads = VGroup(*[style.label_text(w).next_to(b, LEFT, buff=0.4) for w, b in zip(("old", "new"), blocks)])
        ctx.play(FadeIn(heads), LaggedStart(*[FadeIn(VGroup(blocks[0][i], blocks[1][i]))
                                              for i in range(data.REQUESTS)], lag_ratio=0.2), run_time=1.2)
        self._owned["blocks"], self._owned["heads"] = blocks, heads
        # "Levi's two from that night, and ten I wrote": the first two requests, then the rest.
        cols = blocks[0]
        braces = [BraceBetweenPoints(cols[a].get_corner(UL) + UP * 0.15, cols[b].get_corner(UR) + UP * 0.15,
                                     direction=UP, color=style.MUTED) for a, b in ((0, 1), (2, data.REQUESTS - 1))]
        for brace, words, frac in zip(braces, ("Levi's 2", "10 I wrote"), (0.24, 0.36)):
            ctx.show(brace, style.label_text(words).next_to(brace, UP, buff=0.16), tag=words,
                     run_time=ctx.at(frac, 0.5))
        # "Three runs of each, with the old layout and the new": seventy-two runs, and what they cost.
        side = BraceBetweenPoints(cols[-1].get_corner(UR) + RIGHT * 0.15, cols[-1].get_corner(DR) + RIGHT * 0.15,
                                  direction=RIGHT, color=style.MUTED)
        three = style.label_text(f"{data.SAMPLES} runs each", color=style.MUTED).next_to(side, RIGHT, buff=0.2)
        ctx.show(side, three, tag="three", run_time=ctx.at(0.5, 0.4))
        ctx.play(*[Indicate(h, color=style.WHITE) for h in heads], run_time=ctx.at(0.6, 0.6))
        total = style.boxed(style.label_text(f"{data.TOTAL_RUNS} runs"), style.WHITE)
        cost = style.boxed(style.mono_text(data.COST, size="label"), style.MUTED)
        VGroup(total, cost).arrange(DOWN, buff=0.3, aligned_edge=LEFT).next_to(blocks[1], RIGHT, buff=0.6)
        ctx.show(total, tag="total", run_time=ctx.at(0.72, 0.4))
        ctx.show(cost, tag="cost", run_time=ctx.at(0.86, 0.4))

    # -------------------------------------------------------------- 6 slope --
    def y_of(self, n: int) -> float:
        return self.FLOOR + n * self.RUN_H

    def series(self, name: str, color: str, old: int, of: int, new: int | None = None) -> VGroup:
        """One count on the slope: its old dot and value, its name at the left; its new dot and value if given.
        VGroup(left, line, right) or VGroup(left)."""
        a = Dot([self.OLD_X, self.y_of(old), 0], radius=0.12, color=color)
        value = style.label_text(count(old, of)).next_to(a, LEFT, buff=0.3)
        title = style.label_text(name, color=style.MUTED).next_to(value, LEFT, buff=0.35)
        style.sit(title, style.baseline(value))
        left = VGroup(a, value, title)
        if new is None:
            return VGroup(left)
        b = Dot([self.NEW_X, self.y_of(new), 0], radius=0.12, color=color)
        line = Line(a.get_center(), b.get_center(), color=color, stroke_width=3.6).set_z_index(style.Z_EDGE)
        right = VGroup(b, style.label_text(count(new, of)).next_to(b, RIGHT, buff=0.3))
        return VGroup(left, line, right)

    def show_series(self, ctx, tag: str, s: VGroup, old_at: float, new_at: float = 0.0):
        """The old end at `old_at` of the window; the line to the new end at `new_at`, when there is one."""
        ctx.play(FadeIn(s[0]), run_time=ctx.at(old_at, 0.5))
        if len(s) > 1:
            ctx.play(Create(s[1]), run_time=ctx.at(new_at, 1.0))
            ctx.play(FadeIn(s[2], scale=0.8), run_time=0.4)
            ctx.play(Indicate(s[2][0], color=s[2][0].get_color()), run_time=ctx.at(new_at + 0.2, 0.6))
        self._owned[tag] = s

    def b_served(self, ctx):
        ctx.clear_stage(run_time=0.4)
        top = self.y_of(data.OLD["runs"])
        posts = VGroup(*[Line([x, self.FLOOR, 0], [x, top, 0], color=style.GRID, stroke_width=2)
                         for x in (self.OLD_X, self.NEW_X)]).set_z_index(style.Z_BACKDROP)
        heads = VGroup(*[style.label_text(w).next_to([x, top, 0], UP, buff=0.25)
                         for w, x in (("old", self.OLD_X), ("new", self.NEW_X))])
        ctx.play(Create(posts), FadeIn(heads), run_time=0.5)
        self._owned["frame"] = VGroup(posts, heads)
        served = self.series("first read served", style.SERVED, data.OLD["first_served"], data.OLD["read_phone"],
                             data.NEW["first_served"])
        self.show_series(ctx, "served", served, 0.04, 0.16)
        # "with the new layout, all thirty-four did": the new end lit again, so the frame is not still for 5 s
        ctx.play(Indicate(served[2], color=style.SERVED, scale_factor=1.12), run_time=ctx.at(0.72, 0.8))

    def b_too_long(self, ctx):
        told = self.series("said it was too long", style.REFUSED, data.OLD["too_long"], data.OLD["runs"],
                           data.NEW["too_long"])
        self.show_series(ctx, "told", told, 0.05, 0.6)

    def b_shell(self, ctx):
        shell = self.series("read through the shell", style.WHITE, data.OLD["shell_read"], data.OLD["runs"])
        self.show_series(ctx, "shell", shell, 0.08)
        # "which works only when the model thinks of it".
        luck = style.boxed(style.label_text("if it thinks to", color=style.MUTED, size="caption"), style.MUTED, pad=(0.4, 0.26))
        luck.next_to(shell[0], UP, buff=0.3)  # above the old column: clear of the green line
        ctx.show(luck, tag="luck", run_time=ctx.at(0.5, 0.5))

    # -------------------------------------------------------------- 7 brief --
    def b_brief(self, ctx):
        ctx.clear_stage(run_time=0.4)
        hand = style.worker(size=1.3).move_to([0, 0.7, 0])
        one = style.brief_card(True).move_to([-3.0, 0.95, 0])
        ctx.show(hand, tag="worker", run_time=0.4)
        ctx.play(FadeIn(one, shift=RIGHT * 0.2), run_time=0.4)
        ctx.play(one.animate.next_to(hand[0], LEFT, buff=0.2), run_time=0.6)
        self._owned["one"] = one
        rows = VGroup(brief_row(data.OLD["brief_route"], data.OLD["delegated"]),
                      brief_row(data.NEW["brief_route"], data.NEW["delegated"])).arrange(DOWN, buff=0.55,
                                                                                         aligned_edge=LEFT)
        rows.move_to([0.1, -0.75, 0])
        heads = VGroup(*[style.label_text(w).next_to(r, LEFT, buff=0.4) for w, r in zip(("old", "new"), rows)])
        sums = VGroup(*[style.label_text(count(d["brief_route"], d["delegated"])).next_to(r, RIGHT, buff=0.4)
                        for d, r in ((data.OLD, rows[0]), (data.NEW, rows[1]))])
        # "Before the split ... six times in nineteen; after it, seventeen times in seventeen": the worker and its
        # brief move up to head the two rows.
        top = VGroup(hand, one)
        ctx.play(top.animate.shift(UP * 0.8), run_time=ctx.at(0.3, 0.6))
        for i, frac in enumerate((0.36, 0.66)):
            ctx.play(FadeIn(heads[i]), LaggedStart(*[FadeIn(c, shift=DOWN * 0.1) for c in rows[i]], lag_ratio=0.12),
                     run_time=ctx.at(frac, 1.4))
            ctx.play(FadeIn(sums[i], shift=LEFT * 0.1), run_time=ctx.at(frac + 0.14, 0.4))
        self._owned["rows"] = VGroup(rows, heads, sums)
