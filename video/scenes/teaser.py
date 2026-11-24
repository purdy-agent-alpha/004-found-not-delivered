"""
The teaser Short: the four lines script/teaser.md names, drawn again upright for the phone from the main video's
figures for those lines: the shelf with the gold route and the question before the agent (01, line 1); the path from
store to model, ticked step by step until the read stops red at the door (01, line 5); the runtime's refusal on its
page (02, line 3); and the search of the session log, ending on "bad luck?" (03, line 1). The chip and the end card
are TeaserScene's.

Every text here is one the main video shows (the gate's `teaser_text`): the words and the animation of those figures
are figures.py's, which s01_open.py, s02_refusal.py and s03_four.py draw too; the shelf's names are s01's.
"""
from __future__ import annotations

from manim import *

import figures
import style
from pipeline import stage
from pipeline.beats import Beat, TeaserScene

S = stage.STAGE
CX = S.center[0]

SHELF = ("recall", "phone", "decide")            # three of s01's shelf, the phone skill in the middle


def path_figure() -> dict:
    """Store to model, upright: the phone card over three steps down the left, the read running right to the door
    and on to Alpha; a tick place left of each step."""
    col = CX - 1.3
    f = figures.path(card=(0.9, 1.15), door=(1.5, 0.9), alpha=1.05)
    f["card"].move_to([col, 3.17, 0])
    f["stored"].next_to(f["card"], RIGHT, buff=0.3)
    for box, y in zip(f["steps"], (1.95, 1.02, 0.1)):
        box.move_to([col, y, 0])
    chain = [f["card"], *f["steps"]]
    f["links"] = VGroup(*[style.glow_arrow(a.get_bottom(), b.get_top(), color=style.MUTED, width=2.6, buff=0.08)
                          for a, b in zip(chain, chain[1:])])
    f["ticks"] = VGroup(*[style.tick(scale=1.4).next_to(m, LEFT, buff=0.3) for m in chain])
    y = f["steps"][-1].get_y()
    f["door"].move_to([0.55, y + 0.15, 0])
    f["alpha"].move_to([1.95, y, 0])
    figures.stop_read(f, y, past=0.45, gap=0.1)
    return f


def refusal_page() -> dict:
    """The refusal as the runtime sent it, on a page headed by who sent it and when, a stop bar on its left edge.
    Its rows are the main video's at label size, the page as wide as the stage allows: any narrower and the scale
    closes their word gaps up (the gate's words_merged)."""
    rows = [style.label_text(t) for t in figures.REFUSAL]
    head = style.text_rows(style.label_text("runtime to Alpha", color=style.RUNTIME),
                           style.mono_text("2026-11-23 21:29", color=style.MUTED, size="label"))
    block = style.text_rows(head, style.text_rows(*rows), buff=0.4)
    sheet = style.page(block, (0.36, 0.4))
    bar = style.stop_bar(height=sheet.height - 0.2).move_to(sheet.get_left())
    stage.fit(VGroup(sheet, bar, block), S, pad=0.05)
    marks, unlit = figures.refusal_marks(rows)
    return {"sheet": sheet, "bar": bar, "head": head, "rows": rows, "marks": marks, "unlit": unlit}


class Teaser(TeaserScene):
    """The Short: the question, the turn, the runtime's words, and the search that asks whether it was luck."""

    def storyboard(self) -> list[Beat]:
        return [
            Beat("An AI agent has a skill written down", self.b_question, kind="diagram"),
            Beat("The first answer surprised me", self.b_turn, kind="flow"),
            Beat("The runtime answered", self.b_refusal, kind="document"),
            Beat("I searched my production log", self.b_search, kind="search"),
        ]

    def b_question(self, ctx):
        f = {"cards": VGroup(*[style.skill_card(n, width=1.05, height=1.45, route=n == "phone") for n in SHELF])}
        f["cards"].arrange(RIGHT, buff=0.3).move_to([CX, 2.95, 0])
        f["plank"] = plank = figures.plank(f["cards"])
        f["files"] = style.label_text("its own files", color=style.MUTED).next_to(plank, DOWN, buff=0.25)
        f["files"].align_to(plank, LEFT)
        f["agent"] = agent = style.alpha(size=1.1, name="agent").move_to([CX, -0.3, 0])
        f["phone"] = f["cards"][1]
        f["ask"] = ask = style.title_text("?").scale(1.9)
        ask.move_to([CX, (plank.get_y() + agent.get_top()[1]) / 2 - 0.2, 0])
        top, bottom = plank.get_y() - 0.12, agent.get_top()[1] + 0.1
        f["legs"] = figures.legs([CX, top, 0], [CX, ask.get_top()[1] + 0.12, 0], [CX, ask.get_bottom()[1] - 0.12, 0],
                                 [CX, bottom, 0])
        # Frame one: the shelf drops into place; the agent rises from below; the path down to it is broken.
        figures.question(ctx, f, drop=(0.2, 0.1), enter=UP * 0.4)

    def b_turn(self, ctx):
        figures.turn(ctx, path_figure())

    def b_refusal(self, ctx):
        figures.refuse(ctx, refusal_page(), bar_at=0.04)

    @staticmethod
    def on_line(ctx, frac: float, run_time: float) -> float:
        """ctx.at for a fraction of the line itself: the last beat's window runs on under the end card."""
        return ctx.at(frac * (ctx.beat.line_end - ctx.beat.start) / ctx.window, run_time)

    def b_search(self, ctx):
        end = ctx.beat.start + ctx.window
        self.qa_waive("text_too_brief", end - self._episode.END_CARD, end + 0.4,
                      "the end card is TeaserScene's: episode.END_CARD (6.5 s) less its fades holds this episode's "
                      "48-character title 6.2 s, short of the 6.4 s the check asks; its length is the pipeline's")
        ctx.clear_stage(run_time=0.3)
        f = figures.search(style.card(5.9, 0.7, style.WHITE).move_to([CX, 3.25, 0]),
                           style.card(5.9, 2.4).move_to([CX, 1.45, 0]), rows=(6, 2.1, 1.5, 1.1), hits=(1, 3, 5))
        f["luck"].move_to([CX, -0.25, 0])
        page = VGroup(f["panel"], f["name"])
        # "I searched my production log for every time I read a skill": the query typed, the log below it.
        ctx.show(f["field"], f["glass"], tag="field", run_time=0.3, nudge=False)
        self.play(Write(f["query"]), FadeIn(page), run_time=self.on_line(ctx, 0.04, 0.8))
        self._owned["query"] = VGroup(f["query"], page)
        self.play(LaggedStart(*[Create(r) for r in f["rows"]], lag_ratio=0.15), run_time=self.on_line(ctx, 0.22, 0.8))
        self.play(*[r.animate.set_color(style.WHITE).set_stroke(width=4) for r in f["hits"]],
                  LaggedStart(*[FadeIn(m, scale=1.6) for m in f["marks"]], lag_ratio=0.3), run_time=self.on_line(ctx, 0.4, 0.7))
        self._owned["rows"] = VGroup(f["rows"], f["marks"])
        # "Was that night bad luck?"
        ctx.show(f["luck"], tag="luck", anim=lambda m: FadeIn(m, shift=UP * 0.2), run_time=self.on_line(ctx, 0.62, 0.5),
                 nudge=False)
        self.play(Indicate(f["luck"][1], color=style.WHITE, scale_factor=1.12), run_time=self.on_line(ctx, 0.85, 0.5))
