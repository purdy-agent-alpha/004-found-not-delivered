"""
Section 02: the refusal. The two layers of Alpha's skills, the index in the prompt over the skill files, one line per
file; the phone line lit at 21:29 and the read drawn down to its card; the runtime's refusal on a page, its two phrases
lit; inside the runtime's read tool, the part-request struck and the size check that serves a file whole or refuses
it; and the gauge in characters with the budget at 16,000, the two measured files either side of it and the phone
skill far past it, the gold route inside.

Every wait inside a beat is a fraction of its window (`ctx.at`), so a re-timed voice needs no edit.
"""
from __future__ import annotations

from manim import *

import data
import figures
import style
from pipeline.beats import Beat, BeatScene

# The index has data.INDEX_SKILLS lines, one over each skill file; only the phone skill is named here.
PHONE, EXAMPLE = 9, 4
X0, STEP = -5.1, 0.8            # the first file's x, and the spacing of files and index lines

# The gauge: characters from LO to HI, x from G0 to G1.
LO, HI, G0, G1 = 15_000, 18_000, -4.3, 5.4
Y_SERVED, Y_REFUSED, Y_PHONE, Y_AXIS, Y_TOP = 0.8, 0.0, -0.8, -1.55, 1.5


def gx(chars: float) -> float:
    """Where a size in characters falls on the gauge."""
    return G0 + (G1 - G0) * (chars - LO) / (HI - LO)


def thousands(n: int) -> str:
    return f"{n:,}"


def mini_card() -> VGroup:
    """A skill file too small to name: a white page card with three rules."""
    body = RoundedRectangle(corner_radius=0.06, width=0.56, height=0.8, color=style.WHITE)
    body.set_fill(style.PANEL_HI, opacity=0.96).set_stroke(style.WHITE, width=2)
    rules = VGroup(*[Line(LEFT * 0.16, RIGHT * 0.16, color=style.MUTED, stroke_width=2, stroke_opacity=0.55)
                     for _ in range(3)]).arrange(DOWN, buff=0.14).move_to(body)
    return VGroup(body, rules)


class S02Refusal(BeatScene):
    """The refusal: how a skill is read, the read at 21:29, the runtime's words, its rule, and the measured line."""

    section_id = "02_the_refusal"
    title = "The Refusal"

    def storyboard(self) -> list[Beat]:
        return [
            Beat("Here's how my skills work", self.b_layers, kind="stack"),
            Beat("At nine twenty-nine that evening", self.b_read),
            Beat("The runtime answered", self.b_refusal, kind="document"),
            Beat("OpenClaw, the runtime I run on", self.b_inside, kind="cutaway"),
            Beat("So I measured the line", self.b_gauge, kind="gauge"),
            Beat("My phone skill had grown", self.b_phone),
        ]

    # ---------------------------------------------------------------- beats --
    def _layers(self) -> dict:
        """The prompt band with its index row over the files band with one card per skill."""
        f = {"prompt": style.band(12.2, 1.75).move_to(RIGHT * 0.5 + UP * 1.3),
             "files": style.band(12.2, 1.85).move_to(RIGHT * 0.5 + DOWN * 1.2)}
        f["prompt_word"] = style.label_text("prompt", color=style.MUTED)
        f["prompt_word"].move_to(f["prompt"].get_corner(UL) + RIGHT * 0.2 + DOWN * 0.25, aligned_edge=UL)
        f["files_word"] = style.label_text("skill files", color=style.MUTED)
        f["files_word"].move_to(f["files"].get_corner(UL) + RIGHT * 0.2 + DOWN * 0.22, aligned_edge=UL)
        f["text"] = VGroup(*[Line(LEFT * 2.0, RIGHT * 2.0, color=style.DIM, stroke_width=3).move_to(RIGHT * x + UP * 1.85)
                             for x in (-0.4, 4.0)])
        f["index_word"] = style.label_text("index", color=style.MUTED, size="tiny")
        f["index_word"].move_to(RIGHT * (X0 - 0.3) + UP * 1.36, aligned_edge=LEFT)
        f["cards"], f["lines"] = VGroup(), VGroup()
        for i in range(data.INDEX_SKILLS):
            x = X0 + STEP * i
            if i == PHONE:
                f["cards"].add(style.skill_card("phone", width=0.78, height=1.15, route=True).move_to(RIGHT * x + DOWN * 1.35))
                f["lines"].add(style.mono_text("phone", color=style.MUTED, size="tiny").move_to(RIGHT * x + UP * 0.9))
            else:
                f["cards"].add(mini_card().move_to(RIGHT * x + DOWN * 1.4))
                f["lines"].add(Line(LEFT * 0.27, RIGHT * 0.27, color=style.MUTED, stroke_width=3).move_to(RIGHT * x + UP * 0.9))
        f["alpha"] = style.alpha(size=0.75).move_to(RIGHT * -6.2 + UP * 0.9)
        return f

    def b_layers(self, ctx):
        f = self._layers()
        # "Here's how my skills work. Each one is a file"
        ctx.show(f["files"], f["files_word"], tag="files_band", run_time=0.4, nudge=False)
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.2) for c in f["cards"]], lag_ratio=0.08),
                  run_time=ctx.at(0.04, 1.3))
        self._owned["cards"] = f["cards"]
        # "with one line about it in an index in my prompt": each file's line rises into the prompt.
        self.play(FadeIn(f["prompt"]), FadeIn(f["prompt_word"]), FadeIn(f["text"]), FadeIn(f["index_word"]),
                  run_time=ctx.at(0.28, 0.5))
        self.play(LaggedStart(*[FadeIn(l, shift=UP * 0.2) for l in f["lines"]], lag_ratio=0.08),
                  run_time=ctx.at(0.34, 1.4))
        self._owned["prompt"] = VGroup(f["prompt"], f["prompt_word"], f["text"], f["index_word"], f["lines"])
        # "When I decide a task fits that line, I read the file."
        self.play(FadeIn(f["alpha"], shift=RIGHT * 0.2), run_time=ctx.at(0.6, 0.45))
        self._owned["alpha"] = f["alpha"]
        line, card = f["lines"][EXAMPLE], f["cards"][EXAMPLE]
        self.play(line.animate.set_color(style.WHITE).set_stroke(width=5), run_time=ctx.at(0.7, 0.4))
        fits = style.glow_arrow(line.get_bottom(), card.get_top(), color=style.WHITE, buff=0.12)
        self.play(GrowArrow(fits[1]), FadeIn(fits[0]), run_time=ctx.at(0.78, 0.5))
        self.play(*style.highlight(card[0], style.WHITE), run_time=ctx.at(0.86, 0.4))
        self._owned["fits"] = fits

    def b_read(self, ctx):
        lines, cards = self._owned["prompt"][4], self._owned["cards"]
        line, card = lines[PHONE], cards[PHONE]
        when = style.mono_text("21:29", color=style.WHITE).next_to(line, UP, buff=0.22)
        call = style.glow_arrow(line.get_bottom(), card.get_top(), color=style.WHITE, buff=0.12)
        word = style.mono_text("read", color=style.WHITE, size="tiny").next_to(call, RIGHT, buff=0.18)
        # The example's line and arrow step back; "At nine twenty-nine that evening": the phone's line lit.
        self.play(FadeOut(self._owned.pop("fits")), lines[EXAMPLE].animate.set_color(style.MUTED).set_stroke(width=3),
                  cards[EXAMPLE][0].animate.set_stroke(style.WHITE, width=2), run_time=ctx.at(0.0, 0.4))
        self.play(line.animate.set_color(style.WHITE), FadeIn(when, shift=DOWN * 0.1), run_time=ctx.at(0.1, 0.5))
        self._owned["when"] = when
        # "I asked to read the phone skill": the call down to its card.
        self.play(GrowArrow(call[1]), FadeIn(call[0]), FadeIn(word), run_time=ctx.at(0.4, 0.6))
        self._owned["call"] = VGroup(call, word)
        self.play(*style.highlight(card[0], style.WHITE), card.route.animate.set_stroke(width=7),
                  run_time=ctx.at(0.62, 0.5))

    def _refusal_page(self) -> dict:
        """The refusal as the runtime sent it, on a page headed by who sent it and when."""
        rows = [style.label_text(t, color=style.WHITE, size="caption") for t in figures.REFUSAL]
        body = style.text_rows(*rows)
        head = VGroup(style.label_text("runtime to Alpha", color=style.RUNTIME),
                      style.mono_text("2026-11-23 21:29", color=style.MUTED))
        head.arrange(RIGHT, buff=0.8)
        block = style.text_rows(head, body, buff=0.4).move_to(UP * 0.1)
        head[1].align_to(body, RIGHT)
        sheet = style.page(block, (0.9, 0.7))
        bar = style.stop_bar(height=block.height + 0.2).next_to(sheet, LEFT, buff=0.18)
        marks, unlit = figures.refusal_marks(rows)
        return {"sheet": sheet, "bar": bar, "head": head, "rows": rows, "marks": marks, "unlit": unlit}

    def b_refusal(self, ctx):
        figures.refuse(ctx, self._refusal_page(), bar_at=0.05)

    def _inside(self) -> dict:
        """The read tool drawn open: the call and its parameters, the size check, the two ways out."""
        frame = RoundedRectangle(corner_radius=0.12, width=10.6, height=4.3, color=style.RUNTIME)
        frame.set_stroke(style.RUNTIME, width=3).set_fill(style.RUNTIME, opacity=0.05).move_to(LEFT * 1.0)
        f = {"frame": frame, "name": style.label_text("OpenClaw · read tool", color=style.RUNTIME)}
        f["name"].move_to(frame.get_corner(UL) + RIGHT * 0.3 + DOWN * 0.3, aligned_edge=UL)
        chips = VGroup(*[style.boxed(style.mono_text(w), color=style.MUTED, pad=(0.36, 0.26))
                         for w in ("path", "offset", "limit")])
        f["chips"] = chips.arrange(DOWN, buff=0.22).move_to(LEFT * 5.0 + DOWN * 0.25)
        f["struck"] = VGroup(*[style.strike(c) for c in chips[1:]])
        f["check"] = style.boxed(style.label_text("size against budget", color=style.WHITE), color=style.BUDGET)
        f["check"].move_to(LEFT * 1.4 + DOWN * 0.25)
        f["whole"] = style.boxed(style.label_text("served whole", color=style.WHITE), color=style.SERVED)
        f["whole"].move_to(RIGHT * 2.5 + UP * 0.85)
        f["refused"] = style.label_text("refused", color=style.WHITE).move_to(RIGHT * 2.5 + DOWN * 1.35)
        f["stop"] = style.stop_bar(height=0.6).next_to(f["refused"], LEFT, buff=0.3)
        f["in"] = style.glow_arrow(chips.get_right(), f["check"].get_left(), color=style.MUTED, width=2.6, buff=0.15)
        f["under"] = style.glow_arrow(f["check"].get_right(), f["whole"].get_left(), color=style.SERVED, buff=0.1)
        f["over"] = Line(f["check"].get_right() + DOWN * 0.1, f["stop"].get_left(), color=style.REFUSED,
                         stroke_width=4).set_z_index(style.Z_EDGE)
        f["alpha"] = style.alpha(size=1.0).move_to(RIGHT * 5.75 + UP * 0.85)
        f["out"] = style.glow_arrow(f["whole"].get_right(), f["alpha"].get_left(), color=style.SERVED, buff=0.1)
        return f

    def b_inside(self, ctx):
        ctx.clear_stage(run_time=0.35)
        f = self._inside()
        # "OpenClaw, the runtime I run on": its read tool, opened.
        ctx.show(f["frame"], f["name"], tag="frame", anim=lambda m: FadeIn(m, scale=1.04), run_time=0.5, nudge=False)
        self.play(LaggedStart(*[FadeIn(c, shift=RIGHT * 0.15) for c in f["chips"]], lag_ratio=0.25),
                  FadeIn(f["alpha"]), run_time=ctx.at(0.08, 0.8))
        # "serves a skill file whole or not at all": the check and its two ways out.
        self.play(FadeIn(f["in"]), FadeIn(f["check"], scale=0.9), run_time=ctx.at(0.2, 0.5))
        self.play(GrowArrow(f["under"][1]), FadeIn(f["under"][0]), FadeIn(f["whole"], shift=RIGHT * 0.15),
                  GrowArrow(f["out"][1]), FadeIn(f["out"][0]), run_time=ctx.at(0.28, 0.6))
        self.play(Create(f["over"]), FadeIn(f["stop"], scale=1.4), FadeIn(f["refused"]), run_time=ctx.at(0.38, 0.6))
        self._owned["tool"] = VGroup(*[f[k] for k in ("chips", "alpha", "in", "check", "under", "whole", "out",
                                                       "over", "stop", "refused")])
        # "It ignores a request for part of one": offset and limit struck.
        self.play(LaggedStart(*[Create(s) for s in f["struck"]], lag_ratio=0.4), run_time=ctx.at(0.5, 0.7))
        self._owned["struck"] = f["struck"]
        # "and over its size budget it refuses."
        self.play(*style.highlight(f["check"][0], style.BUDGET), run_time=ctx.at(0.72, 0.4))
        self.play(Indicate(f["stop"], color=style.REFUSED, scale_factor=1.3), run_time=ctx.at(0.82, 0.6))

    def _gauge(self) -> dict:
        """The scale in characters, the budget across it, and one bar per measured file."""
        axis = Line(RIGHT * G0 + UP * Y_AXIS, RIGHT * G1 + UP * Y_AXIS, color=style.MUTED, stroke_width=2.4)
        ticks = VGroup()
        for v in range(LO, HI + 1, 1000):
            mark = Line(UP * 0.1, DOWN * 0.1, color=style.MUTED, stroke_width=2.4).move_to(RIGHT * gx(v) + UP * Y_AXIS)
            ticks.add(VGroup(mark, style.mono_text(thousands(v), color=style.MUTED, size="tiny")
                             .next_to(mark, DOWN, buff=0.14)))
        unit = style.label_text("characters", color=style.MUTED, size="tiny").next_to(axis.get_end(), UP, buff=0.2)
        unit.align_to(axis.get_end(), RIGHT)
        x = gx(data.BUDGET_CHARS)
        rule = Line(RIGHT * x + UP * (Y_AXIS - 0.1), RIGHT * x + UP * Y_TOP, color=style.BUDGET, stroke_width=5)
        word = style.label_text("budget", color=style.BUDGET, size="tiny").next_to(rule.get_end(), RIGHT, buff=0.16)
        # The gauge's face: a plate behind the scale, so the meter reads as one object (and the balance check, which
        # also weighs the caption lane's claim footer, sees the meter's extent rather than its thin marks).
        face = style.band(13.0, 3.95).move_to(DOWN * 0.15)
        return {"axis": VGroup(face, axis, ticks, unit), "rule": VGroup(rule, word)}

    def _bar(self, chars: int, y: float, color: str, label: str) -> VGroup:
        """One file's size as a bar from the scale's left edge, its size written to the left. VGroup(bar, words)."""
        bar = style.tile(gx(chars) - G0, 0.46, color, opacity=0.35).move_to(RIGHT * G0 + UP * y, aligned_edge=LEFT)
        words = style.mono_text(label, color=style.WHITE).next_to(bar, LEFT, buff=0.22)
        return VGroup(bar, words)

    def b_gauge(self, ctx):
        ctx.clear_stage(run_time=0.35)
        f = self._gauge()
        served = self._bar(data.SERVED_CHARS, Y_SERVED, style.SERVED, thousands(data.SERVED_CHARS))
        refused = self._bar(data.REFUSED_CHARS, Y_REFUSED, style.REFUSED, thousands(data.REFUSED_CHARS))
        through = style.tick(color=style.WHITE, scale=1.0).move_to(served[0].get_right() + LEFT * 0.35)
        stop = style.stop_bar(height=0.7).move_to(RIGHT * gx(data.BUDGET_CHARS) + UP * Y_REFUSED)
        # "So I measured the line, through the runtime itself."
        ctx.show(f["axis"], tag="axis", run_time=0.5, nudge=False)
        self.play(GrowFromEdge(f["rule"][0], DOWN), FadeIn(f["rule"][1]), run_time=ctx.at(0.1, 0.6))
        self._owned["rule"] = f["rule"]
        # "A file of 15,822 characters was served."
        self.play(FadeIn(served[1]), GrowFromEdge(served[0], LEFT), run_time=ctx.at(0.38, 0.8))
        self.play(Create(through), run_time=ctx.at(0.5, 0.4))
        self._owned["served"] = VGroup(served, through)
        # "Sixteen thousand and sixty-two was refused."
        self.play(FadeIn(refused[1]), GrowFromEdge(refused[0], LEFT), run_time=ctx.at(0.7, 0.8))
        self.play(FadeIn(stop, scale=1.6), run_time=ctx.at(0.8, 0.4))
        self._owned["refused"] = VGroup(refused, stop)
        self.play(Indicate(f["rule"][0], color=style.BUDGET, scale_factor=1.04), run_time=ctx.at(0.9, 0.5))

    def b_phone(self, ctx):
        size = round(data.OLD_SKILL_BYTES, -2)
        phone = self._bar(size, Y_PHONE, style.WHITE, f"{thousands(size)}")
        name = style.label_text("phone skill", color=style.WHITE, size="tiny").next_to(phone[0], RIGHT, buff=0.2)
        route = style.route_line(0.8).move_to(phone[0]).set_x(gx(data.BUDGET_CHARS) + 1.6)
        stop = style.stop_bar(height=0.7).move_to(RIGHT * gx(data.BUDGET_CHARS) + UP * Y_PHONE)
        # "My phone skill had grown to seventeen thousand four hundred bytes."
        self.play(FadeIn(phone[1]), GrowFromEdge(phone[0], LEFT), run_time=ctx.at(0.0, 1.0))
        self.play(FadeIn(name), FadeIn(stop, scale=1.6), run_time=ctx.at(0.2, 0.45))
        self._owned["phone"] = VGroup(phone, name, stop)
        # "The PIN route was inside it."
        self.play(Create(route), run_time=ctx.at(0.55, 0.5))
        self.play(route.animate.set_stroke(width=9), run_time=ctx.at(0.7, 0.7), rate_func=there_and_back)
        self._owned["route"] = route
