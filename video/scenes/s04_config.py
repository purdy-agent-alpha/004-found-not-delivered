"""
Section 04: a number in a config. Where the 16,000-character budget comes from: the context window the config gives
the model, into the runtime's rule, out as characters per skill read; the budget by window (16,000 under 100,000
tokens, 32,000 from it, Alpha's 90,000 under the first bar); 90,000 set against the 1,000,000 OpenRouter lists; Levi's
words of 2026-11-23 21:50 beside the config plate, and the plate's question mark: no record of why, and a larger window
costs more every turn.

Every number is video/data.py's (report/report.md, "The finding"); the 100,000-token step is the script's and the
runtime source's (data.BUDGET_AT_100K's comment). Levi's words are the brief's, verbatim, the first sentence cut.
"""
from __future__ import annotations

from manim import *

import data
import style
from pipeline.beats import Beat, BeatScene

STEP_TOKENS = 100_000                      # the window at which the budget doubles (script; runtime source)
LEVI_WHEN = "2026-11-23 21:50"
LEVI_LINES = ("... Because of context limits of LLMs", "this kind of knowledge drop", "is bound to happen.")
LISTED_ON = "2026-11-24"


def n(v: int) -> str:
    """A count as the script reads it: thousands with commas."""
    return f"{v:,}"


def setting() -> VGroup:
    """Alpha's context-window setting, as the config holds it."""
    return style.plate(f"contextTokens: {data.WINDOW_SET}")


class S04Config(BeatScene):
    """Section 04: the budget is set by a number in Alpha's config, not by the model."""

    section_id = "04_a_number_in_a_config"
    title = "A Number in a Config"

    def storyboard(self) -> list[Beat]:
        return [
            Beat("Where does sixteen thousand come from?", self.b_flow, kind="flow"),
            Beat("My chat model is Claude Haiku", self.b_bars, kind="bars"),
            Beat("OpenRouter lists that model", self.b_dumbbell, kind="dumbbell"),
            Beat("Levi's starting point was", self.b_request, kind="request"),
            Beat("Here, the limit was a number", self.b_plate),
            Beat("Why ninety thousand?", self.b_why),
        ]

    # --------------------------------------------------------------- flow --
    def _flow(self) -> tuple[VGroup, ...]:
        """The setting's path: (rule, per, gate, rule_word, plate, where, told, into, out), set a fifth larger than
        the type scale so the section's first figure fills the stage."""
        y = 0.35
        rule = style.budget_rule(width=1.5, text=n(data.BUDGET_CHARS)).move_to([3.9, y, 0])
        per = style.label_text("characters per skill read", color=style.MUTED).next_to(rule, DOWN, buff=0.5)
        gate = style.door(height=2.0, width=1.2).move_to([0.2, y + 0.1, 0])
        rule_word = style.label_text("its rule", color=style.MUTED).next_to(gate[:3], DOWN, buff=0.3)
        plate = setting().move_to([-4.3, y, 0])
        where = style.label_text("my config", color=style.MUTED).next_to(plate, UP, buff=0.3)
        told = style.label_text("the window it is told", color=style.MUTED).next_to(plate, DOWN, buff=0.3)
        into = style.glow_arrow(plate.get_right() + RIGHT * 0.1, gate[0].get_left() + LEFT * 0.1, color=style.WHITE)
        out = style.glow_arrow(gate[1].get_right() + RIGHT * 0.1, rule.get_left() + LEFT * 0.2, color=style.WHITE)
        parts = (rule, per, gate, rule_word, plate, where, told, into, out)
        VGroup(*parts).scale(1.15, about_point=[0, y, 0])
        return parts

    def b_flow(self, ctx):
        rule, per, gate, rule_word, plate, where, told, into, out = self._flow()
        ask = style.caption_text("?").next_to(rule, LEFT, buff=0.35)
        # "Where does sixteen thousand come from?": the budget, the question, and quickly what stands behind it.
        ctx.show(rule, per, tag="budget", run_time=0.4, nudge=False)
        ctx.show(ask, tag="ask", anim=lambda m: FadeIn(m, scale=1.4), run_time=0.3, nudge=False)
        ctx.show(gate, rule_word, tag="door", run_time=ctx.at(0.08, 0.4), nudge=False)
        ctx.show(plate, where, told, tag="plate", run_time=ctx.at(0.16, 0.4), nudge=False)
        # "The budget follows the context window the runtime is told the model has."
        ctx.at(0.3)
        ctx.retire("ask", run_time=0.2)
        self.play(GrowArrow(into[1]), FadeIn(into[0]), run_time=ctx.at(0.4, 0.35))
        self._own("into", into)
        self.play(GrowArrow(out[1]), FadeIn(out[0]), run_time=ctx.at(0.5, 0.35))
        self._own("out", out)
        # The setting flows through: a pulse from the plate, through the door, to the budget.
        pulse = Dot(radius=0.1, color=style.WHITE).move_to(into[1].get_start())
        self.add(pulse)
        self.play(pulse.animate.move_to(out[1].get_end()), run_time=ctx.at(0.64, 1.2), rate_func=smooth)
        self.play(FadeOut(pulse), *style.highlight(rule[0], style.BUDGET), run_time=ctx.at(0.85, 0.3))

    # --------------------------------------------------------------- bars --
    def _bars(self) -> tuple[VGroup, ...]:
        """The budget by window: (floor, bars, values, names, what). Heights are to scale."""
        base, unit = -0.75, 2.5 / data.BUDGET_AT_100K
        xs = (-0.5, 3.4)
        floor = Line([-2.0, base, 0], [4.9, base, 0], color=style.MUTED, stroke_width=2).set_z_index(style.Z_BACKDROP)
        bars, values, names = VGroup(), VGroup(), VGroup()
        for x, chars, name in zip(xs, (data.BUDGET_CHARS, data.BUDGET_AT_100K),
                                  (f"under {n(STEP_TOKENS)} tokens", f"{n(STEP_TOKENS)} to 199,999 tokens")):
            bar = style.tile(1.8, chars * unit, style.BUDGET, opacity=0.35).move_to([x, base, 0], aligned_edge=DOWN)
            bars.add(bar)
            values.add(style.mono_text(n(chars), color=style.BUDGET, size="label").next_to(bar, UP, buff=0.2))
            names.add(style.label_text(name, color=style.MUTED).next_to([x, base, 0], DOWN, buff=0.22))
        what = style.label_text("characters per skill read", color=style.MUTED).move_to([-0.5, 2.0, 0])
        return floor, bars, values, names, what

    def b_bars(self, ctx):
        ctx.clear_stage(run_time=0.35)
        model = style.alpha(size=1.15).move_to([-4.7, 1.1, 0])
        name = style.label_text("Claude Haiku 5.5", color=style.WHITE).next_to(model, DOWN, buff=0.25)
        plate = setting().next_to(name, DOWN, buff=0.4)
        floor, bars, values, names, what = self._bars()
        # "My chat model is Claude Haiku 5.5, and my config sets its window to ninety thousand tokens."
        ctx.show(model, name, floor, what, tag="model", run_time=0.5, nudge=False)
        ctx.show(plate, tag="plate", anim=lambda m: FadeIn(m, shift=UP * 0.15), run_time=ctx.at(0.15, 0.5),
                 nudge=False)
        # "Below a hundred thousand tokens, a skill read gets sixteen thousand characters"
        ctx.show(names[0], tag="axis", run_time=ctx.at(0.44, 0.4), nudge=False)
        self.play(GrowFromEdge(bars[0], DOWN), run_time=ctx.at(0.47, 0.7))
        self.play(FadeIn(values[0], shift=UP * 0.1), run_time=ctx.at(0.55, 0.3))
        self._own("first", VGroup(bars[0], values[0]))
        # Alpha's 90,000, marked under the first bar.
        mine = VGroup(RegularPolygon(n=6, radius=0.17, color=style.WHITE).set_stroke(style.WHITE, width=2.4)
                      .set_fill(style.PANEL_HI, opacity=0.96),
                      style.mono_text(n(data.WINDOW_SET), color=style.WHITE, size="label")).arrange(RIGHT, buff=0.2)
        mine.next_to(names[0], DOWN, buff=0.3)
        self.play(FadeIn(mine, shift=UP * 0.15), *style.highlight(plate, style.WHITE), run_time=ctx.at(0.64, 0.6))
        self._own("mine", mine)
        # "at a hundred thousand, it doubles."
        self.play(FadeIn(names[1]), GrowFromEdge(bars[1], DOWN), run_time=ctx.at(0.8, 0.8))
        twice = style.label_text("× 2", color=style.BUDGET).next_to(values[1], LEFT, buff=0.3)
        self.play(FadeIn(values[1], shift=UP * 0.1), FadeIn(twice), run_time=ctx.at(0.86, 0.4))
        self._own("second", VGroup(names[1], bars[1], values[1], twice))

    # ----------------------------------------------------------- dumbbell --
    def b_dumbbell(self, ctx):
        ctx.clear_stage(run_time=0.35)
        left, right, y, base = -4.6, 4.6, 0.55, -0.85
        x = lambda v: left + (right - left) * v / data.WINDOW_LISTED   # noqa: E731
        track = style.band(right - left + 1.2, 1.0).move_to([0, y, 0])
        axis = Line([left, base, 0], [right, base, 0], color=style.MUTED, stroke_width=2.2)
        axis.set_z_index(style.Z_BACKDROP)
        ticks = VGroup(*[style.label_text(n(v), color=style.MUTED).next_to([x(v), base, 0], DOWN, buff=0.18)
                         for v in (0, data.WINDOW_LISTED)])
        title = style.label_text("context window, tokens", color=style.MUTED).next_to(axis, DOWN, buff=0.75)
        set_end = style.end_mark(style.MUTED).move_to([x(data.WINDOW_SET), y, 0])
        list_end = style.end_mark(style.SOURCE).move_to([x(data.WINDOW_LISTED), y, 0])
        bar = Line(set_end.get_center(), list_end.get_center(), color=style.MUTED, stroke_width=3)
        bar.set_z_index(style.Z_EDGE)
        set_words = style.text_rows(style.mono_text(n(data.WINDOW_SET), color=style.WHITE, size="label"),
                                    style.label_text("set in my config", color=style.MUTED))
        set_words.next_to(track, UP, buff=0.2).align_to(set_end, LEFT).shift(LEFT * 0.1)
        list_words = style.text_rows(style.mono_text(n(data.WINDOW_LISTED), color=style.SOURCE, size="label"),
                                     style.label_text(f"listed by OpenRouter · {LISTED_ON}", color=style.MUTED),
                                     align=RIGHT)
        list_words.next_to(track, UP, buff=0.2).align_to(list_end, RIGHT).shift(RIGHT * 0.1)
        guide = DashedLine([x(data.WINDOW_SET), base, 0], set_end.get_bottom(), color=style.MUTED, stroke_width=2,
                           dash_length=0.08).set_z_index(style.Z_BACKDROP)
        # "OpenRouter lists that model at a million tokens."
        ctx.show(track, axis, ticks, title, tag="axis", run_time=0.4, nudge=False)
        ctx.show(set_end, set_words, guide, tag="set", run_time=ctx.at(0.04, 0.4), nudge=False)
        self.add(bar.put_start_and_end_on(set_end.get_center(), set_end.get_center() + RIGHT * 0.01))
        self.play(bar.animate.put_start_and_end_on(set_end.get_center(), list_end.get_center()),
                  run_time=ctx.at(0.12, 1.4), rate_func=smooth)
        self._own("bar", bar)
        ctx.show(list_end, list_words, tag="listed", anim=lambda m: FadeIn(m, scale=0.9), run_time=ctx.at(0.3, 0.4),
                 nudge=False)
        # "So this ceiling came from a setting, not from the model."
        ceiling = style.label_text("the ceiling: a setting", color=style.WHITE)
        ceiling.next_to(track, DOWN, buff=0.2).align_to(set_end, LEFT).shift(RIGHT * 0.3)
        self.play(*style.highlight(set_end, style.WHITE), set_words[1].animate.set_color(style.WHITE),
                  run_time=ctx.at(0.58, 0.4))
        ctx.show(ceiling, tag="ceiling", run_time=ctx.at(0.62, 0.4), nudge=False)

    # ------------------------------------------------------------ request --
    def b_request(self, ctx):
        ctx.clear_stage(run_time=0.35)
        words = style.text_rows(*[style.caption_text(t, color=style.MUTED) for t in LEVI_LINES], buff=0.24)
        page, head, words = style.person_page("Levi", "Telegram", LEVI_WHEN, words).move_to([-1.6, 0.35, 0])
        # "Levi's starting point": his message, dated, the first sentence cut.
        ctx.show(page, head, tag="page", run_time=0.5, nudge=False)
        self.play(LaggedStart(*[FadeIn(t, shift=RIGHT * 0.1) for t in words], lag_ratio=0.35),
                  run_time=ctx.at(0.1, 1.0))
        self._own("words", words)
        # "the context limits of language models make this kind of loss bound to happen": his line lit.
        lit = words[0][len("...Becauseof"):]
        under = style.underline(lit, width=2.4)
        self.play(*[t.animate.set_color(style.WHITE) for t in words], run_time=ctx.at(0.4, 0.5))
        self.play(Create(under), run_time=ctx.at(0.55, 0.5))
        self._own("under", under)
        self._page, self._lit = page, words[0]

    # -------------------------------------------------------------- plate --
    def b_plate(self, ctx):
        plate = setting().move_to([4.6, 1.1, 0])
        where = style.label_text("my config", color=style.MUTED).next_to(plate, UP, buff=0.3)
        limit = style.label_text("the limit", color=style.WHITE).next_to(plate, DOWN, buff=0.3)
        start = [self._page.get_right()[0] + 0.1, self._lit.get_center()[1], 0]
        link = style.glow_arrow(start, plate.get_left() + LEFT * 0.1, color=style.WHITE)
        ctx.waive("text_too_brief", "this line's claim chip (the script's tag) is up only as long as the 2.4 s "
                                    "line is spoken; the scene does not set it")
        # "Here, the limit was a number in a config."
        self.play(GrowArrow(link[1]), FadeIn(link[0]), run_time=ctx.at(0.0, 0.4))
        ctx.show(plate, where, tag="plate", anim=lambda m: FadeIn(m, shift=LEFT * 0.2), run_time=0.4, nudge=False)
        ctx.show(limit, tag="limit", run_time=ctx.at(0.35, 0.35), nudge=False)
        self._own("link", link)
        self._plate = plate

    # ---------------------------------------------------------------- why --
    def b_why(self, ctx):
        mark = style.caption_text("?").next_to(self._plate, RIGHT, buff=0.2)
        none = style.label_text("why: no record found", color=style.MUTED)
        none.next_to(self._owned["limit"], DOWN, buff=0.3).align_to(self._plate, LEFT)
        cost = style.boxed(style.text_rows(style.label_text("a larger window", color=style.WHITE),
                                           style.label_text("costs more every turn", color=style.WHITE)))
        cost.next_to(none, DOWN, buff=0.4).align_to(none, LEFT)
        # "Why ninety thousand? I didn't find a record."
        ctx.show(mark, tag="mark", anim=lambda m: FadeIn(m, scale=1.5), run_time=0.4, nudge=False)
        ctx.show(none, tag="none", run_time=ctx.at(0.15, 0.4), nudge=False)
        # "A larger window also costs more every turn, so I'm not calling the setting a mistake."
        ctx.show(cost, tag="cost", anim=lambda m: FadeIn(m, shift=UP * 0.15), run_time=ctx.at(0.4, 0.5), nudge=False)
        self.play(*style.highlight(cost[0], style.WHITE), run_time=ctx.at(0.7, 0.4))
        self.play(self._owned["words"].animate.set_opacity(0.5), self._owned["under"].animate.set_opacity(0.4),
                  run_time=ctx.at(0.82, 0.5))
