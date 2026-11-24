"""
Section 03: four of four. A search over the session log for every skill read, and the question it asks; the weeks
from 10-12 to 11-24 with the day the phone skill passed the budget and its four reads after it turning red; the 52
skill reads as squares, those four red among 48 green; the first refusal, what the runtime told the model beside what
the model told the person asking; the failure catalogue's reading of that turn struck; and the refusal seen only
inside, the people outside getting the reply, a month of it unseen.

The person asked on 10-23 is a white circle without a name. Every wait inside a beat is a fraction of its window
(`ctx.at`), so a re-timed voice needs no edit.
"""
from __future__ import annotations

from datetime import date

from manim import *

import data
import figures
import style
from pipeline.beats import Beat, BeatScene

YEAR = 2026
FIRST, LAST = data.SEARCHED            # the log searched (report, "The finding")
T0, T1, Y_AXIS = -4.9, 5.3, -0.3        # the time axis

# What the runtime said (shortened, its cut shown) and what the model said, in the script's words, not quoted.
TOLD_MODEL = ("“Skill instructions cannot", "be partially served ...”")
TOLD_PERSON = ("phone instructions", "too long")
FILED, FOUND = "“asserted, not observed”", "refused by the runtime"


def day(md: str) -> int:
    """Days from the first day searched."""
    m, d = (int(v) for v in md.split("-"))
    f = date(YEAR, *(int(v) for v in FIRST.split("-")))
    return (date(YEAR, m, d) - f).days


def tx(md: str) -> float:
    """Where a date falls on the time axis."""
    return T0 + (T1 - T0) * day(md) / day(LAST)


def square(color: str | None, side: float = 0.34) -> Square:
    """One skill read: filled green when served, red when refused; an empty dim cell before it is counted."""
    sq = Square(side_length=side)
    if color is None:
        return sq.set_fill(style.PANEL_HI, opacity=0.9).set_stroke(style.DIM, width=1.4)
    return sq.set_fill(color, opacity=0.85).set_stroke(color, width=1.4)


class S03Four(BeatScene):
    """Four of four: every skill read in the log, the phone skill's four refusals, and why nobody saw them."""

    section_id = "03_four_of_four"
    title = "Four of Four"

    def storyboard(self) -> list[Beat]:
        return [
            Beat("I searched my production log", self.b_search, kind="search", lead=3.0),  # up from the cut
            Beat("The phone skill passed sixteen thousand", self.b_weeks, kind="timeline"),
            Beat("Fifty-two skill reads from October", self.b_reads, kind="unit"),
            Beat("The first refusal came on October", self.b_told, kind="side-by-side"),
            Beat("My own catalogue of failures", self.b_ledger, kind="ledger"),
            Beat("Only the model sees a refusal", self.b_unseen),
        ]

    # ---------------------------------------------------------------- beats --
    def b_search(self, ctx):
        f = figures.search(style.card(7.4, 0.72, style.WHITE).move_to(LEFT * 0.9 + UP * 1.55),
                           style.card(7.4, 2.75).move_to(LEFT * 0.9 + DOWN * 0.85), rows=(8, 2.6, 1.9, 1.4),
                           hits=(1, 4, 6))
        f["luck"].move_to(RIGHT * 4.9 + DOWN * 0.2)
        # "I searched my production log for every time I read a skill": the query typed, the log below it.
        ctx.show(f["field"], f["glass"], tag="field", run_time=0.4, nudge=False)
        self.play(Write(f["query"]), FadeIn(f["panel"]), FadeIn(f["name"]), run_time=ctx.at(0.06, 0.8))
        self._owned["query"] = VGroup(f["query"], f["panel"], f["name"])
        self.play(LaggedStart(*[Create(r) for r in f["rows"]], lag_ratio=0.15), run_time=ctx.at(0.25, 1.0))
        self.play(*[r.animate.set_color(style.WHITE).set_stroke(width=4) for r in f["hits"]],
                  LaggedStart(*[FadeIn(m, scale=1.6) for m in f["marks"]], lag_ratio=0.3), run_time=ctx.at(0.45, 0.8))
        self._owned["rows"] = VGroup(f["rows"], f["marks"])
        # "Was that night bad luck?"
        ctx.show(f["luck"], tag="luck", anim=lambda m: FadeIn(m, shift=LEFT * 0.2), run_time=ctx.at(0.62, 0.5),
                 nudge=False)
        self.play(Indicate(f["luck"][1], color=style.WHITE, scale_factor=1.12), run_time=ctx.at(0.85, 0.5))

    def _weeks(self) -> dict:
        """The axis from the first day searched to the last, the day the skill crossed the budget, its reads after,
        and the span they fall in."""
        axis = Line(RIGHT * T0 + UP * Y_AXIS, RIGHT * T1 + UP * Y_AXIS, color=style.MUTED, stroke_width=2.4)
        searched = style.band(T1 - T0 + 1.9, 3.2).move_to(RIGHT * (T0 + T1) / 2 + UP * 0.5)
        ends = VGroup(style.mono_text(FIRST, color=style.MUTED).next_to(axis, LEFT, buff=0.2),
                      style.mono_text(LAST, color=style.MUTED).next_to(axis, RIGHT, buff=0.2))
        x = tx(data.CROSSED)
        cross = Line(RIGHT * x + UP * Y_AXIS, RIGHT * x + UP * 1.4, color=style.BUDGET, stroke_width=4)
        passes = style.label_text(f"passes {data.BUDGET_CHARS:,}", color=style.BUDGET).next_to(cross, UP, buff=0.16)
        crossed = style.mono_text(data.CROSSED).move_to(RIGHT * x + UP * (Y_AXIS - 0.38))
        reads, dates, seen = VGroup(), [], {}
        for md in data.REFUSED_READS:
            n = seen[md] = seen.get(md, -1) + 1
            reads.add(Dot(radius=0.11, color=style.REFUSED).move_to(RIGHT * tx(md) + UP * (Y_AXIS + 0.5 + 0.6 * n)))
            dates.append(None if n else style.mono_text(md).move_to(RIGHT * tx(md) + UP * (Y_AXIS - 0.38)))
        bars = VGroup(*[style.stop_bar(height=0.46).move_to(r) for r in reads])
        x1 = tx(data.REFUSED_READS[-1])
        y = Y_AXIS - 0.95
        span = VGroup(Line(RIGHT * x + UP * y, RIGHT * x1 + UP * y, color=style.WHITE, stroke_width=2.4),
                      *[Line(UP * 0.12, DOWN * 0.12, color=style.WHITE, stroke_width=2.4).move_to(RIGHT * v + UP * y)
                        for v in (x, x1)])
        days = style.label_text(f"{data.DAYS_OVER} days", color=style.WHITE).next_to(span, DOWN, buff=0.2)
        return {"axis": VGroup(searched, axis, ends), "cross": VGroup(cross, passes, crossed), "dates": dates, "reads": reads,
                "bars": bars, "span": VGroup(span, days)}

    def b_weeks(self, ctx):
        ctx.clear_stage(run_time=0.35)
        f = self._weeks()
        ctx.show(f["axis"], tag="axis", anim=Create, run_time=0.6, nudge=False)
        # "The phone skill passed sixteen thousand characters on October nineteenth."
        self.play(GrowFromEdge(f["cross"][0], DOWN), FadeIn(f["cross"][1:]), run_time=ctx.at(0.08, 0.6))
        self._owned["cross"] = f["cross"]
        # "In the thirty-five days that followed"
        self.play(Create(f["span"][0]), FadeIn(f["span"][1]), run_time=ctx.at(0.4, 0.7))
        self._owned["span"] = f["span"]
        # "I read it four times": a mark at each read, its date under the first read of a day.
        for read, label, frac in zip(f["reads"], f["dates"], (0.58, 0.62, 0.66, 0.7)):
            self.play(FadeIn(read, scale=1.8), *([FadeIn(label)] if label else []), run_time=ctx.at(frac, 0.3))
        self._owned["dates"] = VGroup(*[d for d in f["dates"] if d])
        # "and all four were refused."
        self.play(*[ReplacementTransform(r, b) for r, b in zip(f["reads"], f["bars"])], run_time=ctx.at(0.8, 0.6))
        self._owned["bars"] = f["bars"]

    def b_reads(self, ctx):
        ctx.clear_stage("bars", run_time=0.35)
        bars = self._owned.pop("bars")
        served = data.SKILL_READS - len(data.REFUSED_READS)
        cells = VGroup(*[square(None) for _ in range(data.SKILL_READS)]).arrange_in_grid(cols=13, buff=0.1)
        cells.move_to(LEFT * 2.0 + UP * 0.3)
        green = VGroup(*[square(style.SERVED).move_to(c) for c in cells[:served]])
        red = VGroup(*[square(style.REFUSED).move_to(c) for c in cells[served:]])
        head = VGroup(style.label_text(f"{data.SKILL_READS} skill reads", color=style.WHITE),
                      style.mono_text(f"{FIRST} to {LAST}", color=style.MUTED)).arrange(RIGHT, buff=0.5)
        head.next_to(cells, UP, buff=0.4).align_to(cells, LEFT)
        keys = VGroup(VGroup(square(style.SERVED), style.label_text(f"{served} served", color=style.WHITE)),
                      VGroup(square(style.REFUSED), style.label_text(f"{len(data.REFUSED_READS)} refused, all phone",
                                                                     color=style.WHITE)))
        for k in keys:
            k.arrange(RIGHT, buff=0.25)
        keys.arrange(DOWN, buff=0.45, aligned_edge=LEFT).next_to(cells, RIGHT, buff=0.7)

        # "Fifty-two skill reads from October twelfth to November twenty-fourth": the cells, and the four refused
        # reads dropping into theirs.
        ctx.show(head, cells, tag="cells", anim=lambda m: FadeIn(m, shift=UP * 0.1), run_time=0.6, nudge=False)
        self.play(*[ReplacementTransform(b, r) for b, r in zip(bars, red)], run_time=ctx.at(0.2, 0.8))
        self.bring_to_front(*red)       # the bars sat behind the cells drawn after them
        self.play(FadeIn(keys[1], shift=LEFT * 0.1), run_time=ctx.at(0.36, 0.4))
        self._owned["red"] = VGroup(red, keys[1])
        # "and no other skill was refused in that time": every other read served.
        self.play(LaggedStart(*[FadeIn(g) for g in green], lag_ratio=0.02), FadeIn(keys[0], shift=LEFT * 0.1),
                  run_time=ctx.at(0.6, 1.2))
        self._owned["green"] = VGroup(green, keys[0])

    def _told(self) -> dict:
        """The runtime, the model and the person asking in a row, each message on a card above its leg."""
        y = -0.75
        f = {"door": style.door(height=1.5, width=0.9).move_to(LEFT * 5.1 + UP * y),
             "alpha": style.alpha(size=1.15).move_to(UP * y),
             "person": style.person("", size=0.95).move_to(RIGHT * 5.1 + UP * y)}
        f["when"] = style.mono_text("10-23", color=style.MUTED).next_to(f["alpha"], DOWN, buff=0.3)
        f["refusal"] = style.glow_arrow(f["door"].get_right(), f["alpha"].get_left(), color=style.RUNTIME, buff=0.15)
        f["ask"] = style.glow_arrow(f["person"].get_left() + UP * 0.25, f["alpha"].get_right() + UP * 0.25,
                                    color=style.WHITE, width=2.6, buff=0.15)
        f["ask_word"] = style.label_text("use the phone", color=style.MUTED, size="tiny").next_to(f["ask"], UP, buff=0.14)
        f["reply"] = style.glow_arrow(f["alpha"].get_right() + DOWN * 0.25, f["person"].get_left() + DOWN * 0.25,
                                      color=style.WHITE, buff=0.15)
        for key, words, head, x in (("left", TOLD_MODEL, "runtime to model", -2.75),
                                    ("right", TOLD_PERSON, "model to person", 2.75)):
            body = style.text_rows(style.label_text(head, color=style.MUTED),
                                   *[style.label_text(w, color=style.WHITE) for w in words])
            f[key] = VGroup(style.card(4.3, body.height + 0.55).move_to(RIGHT * x + UP * 1.25), body)
            body.move_to(f[key][0]).align_to(f[key][0].get_left() + RIGHT * 0.35, LEFT)
        return f

    def b_told(self, ctx):
        ctx.clear_stage(run_time=0.35)
        f = self._told()
        # "The first refusal came on October twenty-third."
        ctx.show(f["door"], f["alpha"], f["person"], f["when"], tag="row", run_time=0.5, nudge=False)
        self.play(GrowArrow(f["refusal"][1]), FadeIn(f["refusal"][0]), FadeIn(f["left"], shift=DOWN * 0.15),
                  run_time=ctx.at(0.1, 0.6))
        self._owned["left"] = VGroup(f["refusal"], f["left"])
        # "I was asked to use the phone"
        self.play(GrowArrow(f["ask"][1]), FadeIn(f["ask"][0]), FadeIn(f["ask_word"]), run_time=ctx.at(0.32, 0.6))
        self._owned["ask"] = VGroup(f["ask"], f["ask_word"])
        # "and I told the person asking that the phone instructions were too long."
        self.play(GrowArrow(f["reply"][1]), FadeIn(f["reply"][0]), FadeIn(f["right"], shift=DOWN * 0.15),
                  run_time=ctx.at(0.55, 0.6))
        self._owned["right"] = VGroup(f["reply"], f["right"])
        self.play(Indicate(f["right"][1][1:], color=style.WHITE, scale_factor=1.06),
                  Indicate(f["left"][1][1:], color=style.WHITE, scale_factor=1.06), run_time=ctx.at(0.82, 0.7))

    def _ledger(self) -> dict:
        """The catalogue as three rows, the 10-23 entry in the middle; the others are faint lines."""
        f = {"bands": VGroup(*[style.band(12.9, 0.72).move_to(UP * y) for y in (1.05, 0.15, -0.75)])}
        f["name"] = style.label_text("failure catalogue", color=style.MUTED).move_to(LEFT * 6.4 + UP * 1.75,
                                                                                    aligned_edge=LEFT)
        f["faint"] = VGroup(*[Line(LEFT * w / 2, RIGHT * w / 2, color=style.DIM, stroke_width=3).move_to(RIGHT * x + UP * y)
                              for y in (1.05, -0.75) for x, w in ((-5.85, 0.7), (-3.8, 2.8), (-0.4, 3.0), (3.9, 2.8))])
        when = style.mono_text("10-23", color=style.WHITE).move_to(LEFT * 6.25 + UP * 0.15, aligned_edge=LEFT)
        said = style.label_text("instructions too long", color=style.WHITE).move_to(LEFT * 5.2 + UP * 0.15,
                                                                                  aligned_edge=LEFT)
        f["row"] = VGroup(when, said)
        f["filed"] = style.label_text(FILED, color=style.WHITE).move_to(LEFT * 1.8 + UP * 0.15, aligned_edge=LEFT)
        f["strike"] = style.strike(f["filed"])
        mark = style.door(height=0.5, width=0.32, label=False).move_to(RIGHT * 2.15 + UP * 0.15)
        f["found"] = VGroup(mark, style.label_text(FOUND, color=style.WHITE).next_to(mark, RIGHT, buff=0.3))
        f["heads"] = VGroup(style.label_text("filed as", color=style.MUTED),
                            style.label_text("the log shows", color=style.MUTED))
        f["heads"][0].move_to(f["filed"].get_left() + UP * 1.6, aligned_edge=LEFT)
        f["heads"][1].move_to(mark.get_left() + UP * 1.6, aligned_edge=LEFT)
        return f

    def b_ledger(self, ctx):
        ctx.clear_stage(run_time=0.35)
        f = self._ledger()
        # "My own catalogue of failures filed that turn"
        ctx.show(f["bands"], f["name"], f["faint"], tag="ledger", run_time=0.5, nudge=False)
        self.play(FadeIn(f["row"], shift=RIGHT * 0.1), run_time=ctx.at(0.08, 0.5))
        self._owned["row"] = f["row"]
        # "as the model claiming something it hadn't checked."
        self.play(FadeIn(f["heads"][0]), FadeIn(f["filed"]), run_time=ctx.at(0.2, 0.5))
        self._owned["filed"] = VGroup(f["heads"][0], f["filed"])
        # "That reading doesn't survive"
        self.play(Create(f["strike"]), f["filed"].animate.set_color(style.MUTED), run_time=ctx.at(0.5, 0.5))
        self._owned["strike"] = f["strike"]
        # "what it reported, in its own words, was a real refusal."
        self.play(FadeIn(f["heads"][1]), FadeIn(f["found"], shift=RIGHT * 0.15), run_time=ctx.at(0.68, 0.6))
        self._owned["found"] = VGroup(f["heads"][1], f["found"])
        self.play(Indicate(f["found"][1], color=style.WHITE, scale_factor=1.08), run_time=ctx.at(0.86, 0.6))

    def _unseen(self) -> dict:
        """The refusal inside, the reply outside, and the month it went unseen."""
        y = 0.1
        f = {"door": style.door(height=1.3, width=0.8).move_to(LEFT * 5.2 + UP * (y - 0.05)),
             "alpha": style.alpha(size=1.05).move_to(LEFT * 2.6 + UP * y)}
        f["refusal"] = style.glow_arrow(f["door"].get_right(), f["alpha"].get_left(), color=style.RUNTIME, buff=0.15)
        inside = VGroup(f["door"], f["alpha"])
        f["box"] = RoundedRectangle(corner_radius=0.12, width=inside.width + 0.8, height=inside.height + 0.4,
                                    color=style.WHITE).set_stroke(style.WHITE, width=2).move_to(inside)
        f["only"] = style.label_text("only the model sees it", color=style.WHITE)
        f["only"].next_to(f["box"], DOWN, buff=0.2)
        f["people"] = VGroup(style.person("", size=0.85).move_to(RIGHT * 3.3 + UP * (y + 0.75)),
                             style.person("Levi", size=0.85).move_to(RIGHT * 3.3 + UP * (y - 0.75)))
        f["replies"] = VGroup(*[style.glow_arrow(f["alpha"].get_right(), p.get_left(), color=style.WHITE, width=2.6,
                                                 buff=0.15) for p in f["people"]])
        f["words"] = style.label_text("its own words", color=style.MUTED).move_to(RIGHT * 4.85 + UP * y)
        first, last = data.REFUSED_READS[0], data.REFUSED_READS[-1]
        x0, x1 = tx(first), tx(last)
        span = style.band(x1 - x0, 0.5).move_to(RIGHT * (x0 + x1) / 2 + DOWN * 1.92)
        f["month"] = VGroup(span, style.label_text("a month, unseen", color=style.MUTED).move_to(span),
                            style.mono_text(first, color=style.MUTED).next_to(span, LEFT, buff=0.2),
                            style.mono_text(data.REFUSED_READS[-1], color=style.MUTED).next_to(span, RIGHT, buff=0.2))
        return f

    def b_unseen(self, ctx):
        f = self._unseen()
        o = self._owned
        entry = VGroup(o["row"], o["filed"][1], o["strike"], o["found"][1])
        # The catalogue folds to its one entry, which moves up out of the way.
        self.play(FadeOut(o.pop("ledger")), FadeOut(o["filed"][0]), FadeOut(o["found"][0]), run_time=ctx.at(0.0, 0.3))
        self.play(entry.animate.move_to(UP * 1.8), run_time=ctx.at(0.03, 0.5))
        for tag in ("row", "filed", "strike", "found"):
            o.pop(tag)
        o["entry"] = entry
        # "Only the model sees a refusal": the runtime and the model, boxed in together.
        self.play(FadeIn(f["door"]), FadeIn(f["alpha"]), run_time=ctx.at(0.07, 0.5))
        self.play(GrowArrow(f["refusal"][1]), FadeIn(f["refusal"][0]), Create(f["box"]), FadeIn(f["only"]),
                  run_time=ctx.at(0.14, 0.7))
        self._owned["inside"] = VGroup(f["door"], f["alpha"], f["refusal"], f["box"], f["only"])
        # "and it passes it on in its own words": the people outside get the reply alone.
        self.play(FadeIn(f["people"], shift=LEFT * 0.15), run_time=ctx.at(0.34, 0.5))
        self.play(*[GrowArrow(r[1]) for r in f["replies"]], *[FadeIn(r[0]) for r in f["replies"]],
                  FadeIn(f["words"]), run_time=ctx.at(0.42, 0.6))
        self._owned["outside"] = VGroup(f["people"], f["replies"], f["words"])
        # "So for a month, the runtime rule behind it went unseen."
        self.play(FadeIn(f["month"], shift=UP * 0.1), run_time=ctx.at(0.66, 0.6))
        self._owned["month"] = f["month"]
        self.play(f["door"].animate.set_opacity(0.35), run_time=ctx.at(0.84, 0.6))
