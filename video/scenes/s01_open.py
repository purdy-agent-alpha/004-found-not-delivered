"""
Section 01: the open. A shelf of skill cards, one with the gold PIN route, and Alpha's hexagon across a broken path
with the question in the gap; the evening of 2026-11-23 as two lanes, Levi's two messages above and the phone-skill
read below, the route already in the file when he named it; his request of 21:50 on a page between him and Alpha;
the spine's three questions over the evidence; and the path from store to model, ticked step by step until the read
stops red at the runtime's door.

The scene has no title card: the title sits in its lane from the first frame and the shelf is already moving.
Every wait inside a beat is a fraction of its window (`ctx.at`), so a re-timed voice needs no edit.
"""
from __future__ import annotations

from manim import *

import figures
import style
from pipeline import stage
from pipeline.beats import Beat, BeatScene

# Folders in Alpha's skills/ directory; phone, the one holding the route, sits nearest Alpha.
SHELF = ("mail", "tracker", "recall", "decide", "phone")

# Levi's words on Telegram, 2026-11-23 (REQUEST.md), as typed; a cut shown as "...".
ASK_PIN = ("“...can you get it to where I am", "supposed to enter pins?”")
ASK_KEYBOARD = ("“Also aren't you able to enter pins", "using the Bluetooth connection", "virtualizing a keyboard.”")
REQUEST = ("“Check if this case of Bluetooth keyboard", "being forgotten about as a capability is a",
           "more fundamental issue with our Alpha as", "autonomous agent system. ...”")
DATE = "2026-11-23"

EVIDENCE = ("my logs", "runtime code", "three papers", "a test")


def quote(lines, size: str = "label") -> VGroup:
    """Levi's words, one Text per line, left-aligned."""
    return style.text_rows(*[style.label_text(l, color=style.WHITE, size=size) for l in lines])


def sheet(color: str, width: float = 0.8, height: float = 1.05) -> VGroup:
    """A ruled page with no words on it: the session log in grey, a published source in violet."""
    body = style.card(width, height, color)
    rules = VGroup(*[Line(LEFT * width * 0.3, RIGHT * width * (0.3 if i % 2 else 0.12), color=color, stroke_width=2,
                          stroke_opacity=0.7) for i in range(5)])
    return VGroup(body, rules.arrange(DOWN, buff=0.1, aligned_edge=LEFT).move_to(body))


def evidence_icon(name: str) -> VGroup:
    """What the study read or ran, drawn in the episode's grammar: the session log, the runtime's door, three
    published sources (section 05 names them), a test's runs not yet scored."""
    if name == "my logs":
        return sheet(style.MUTED)
    if name == "runtime code":
        return style.door(height=1.05, width=0.65, label=False)
    if name == "three papers":
        return VGroup(*[sheet(style.SOURCE, width=0.7) for _ in range(3)]).arrange(RIGHT, buff=0.16)
    return VGroup(*[Dot(radius=0.1, color=style.MUTED).set_fill(style.PANEL_HI, opacity=1).set_stroke(style.MUTED, 2)
                    for _ in range(6)]).arrange_in_grid(rows=2, cols=3, buff=0.16)


class S01Open(BeatScene):
    """The open: the question, the night it happened, Levi's request, the plan, and the first turn."""

    section_id = "01_open"
    title = "Open"

    def storyboard(self) -> list[Beat]:
        return [
            Beat("An AI agent has a skill written down", self.b_question, kind="diagram", lead=0.3),
            Beat("The agent was me", self.b_night, kind="timeline"),
            Beat("I'm Alpha, an AI agent", self.b_request, kind="request"),
            Beat("Three questions, then", self.b_plan, kind="scorecard"),
            Beat("The first answer surprised me", self.b_turn, kind="flow"),
        ]

    def _open(self) -> None:
        """The title and the first line's claim footer are in their lanes in the first frame, not faded in, so the
        first beat's picture is already moving in frame one (BeatScene fades both in before it)."""
        self._title = stage.fit(style.title_text(self.title), stage.TITLE)
        self._claim = self._claims()[0]
        self._footer = stage.fit(style.claim_footer(*self._claim), stage.CAPTION, align=LEFT)
        self.add(self._title, self._footer)

    # ---------------------------------------------------------------- beats --
    def b_question(self, ctx):
        f = {"cards": VGroup(*[style.skill_card(n, width=1.15, height=1.6, route=n == "phone") for n in SHELF])}
        f["cards"].arrange(RIGHT, buff=0.22).move_to(LEFT * 3.35 + UP * 0.2)
        f["plank"] = figures.plank(f["cards"])
        f["files"] = style.label_text("its own files", color=style.MUTED).next_to(f["plank"], DOWN, buff=0.3)
        f["agent"] = style.alpha(size=1.7, name="agent").move_to(RIGHT * 5.0 + UP * 0.2)
        f["phone"] = phone = f["cards"][-1]
        x0, x1 = phone.get_right()[0] + 0.2, f["agent"].get_left()[0] - 0.2
        f["ask"] = ask = style.title_text("?").scale(2.8).move_to(RIGHT * (x0 + x1) / 2 + UP * 0.2)
        y = phone.route.get_y()
        f["legs"] = figures.legs(RIGHT * x0 + UP * y, RIGHT * (ask.get_left()[0] - 0.3) + UP * y,
                                 RIGHT * (ask.get_right()[0] + 0.3) + UP * y, RIGHT * x1 + UP * y)
        # Frame one: the shelf is already on screen, its cards dropping into place; the agent comes from the right.
        figures.question(ctx, f, drop=(0.25, 0.12), enter=LEFT * 0.5)

    def _night(self) -> dict:
        """The evening as two lanes on one time axis: Levi above, Alpha below."""
        y_axis, y_top, y_low, x_head = -0.2, 1.35, -1.4, -5.95
        t29, t30 = -2.4, 3.4
        f = {"axis": Line(LEFT * 5.0 + UP * y_axis, RIGHT * 6.4 + UP * y_axis, color=style.MUTED, stroke_width=2.4),
             "levi": style.person("Levi", size=0.85).move_to(RIGHT * x_head + UP * y_top),
             "alpha": style.alpha(size=0.95).move_to(RIGHT * x_head + UP * y_low)}
        f["date"] = style.mono_text(DATE, color=style.MUTED).next_to(f["axis"].get_start(), DOWN, buff=0.22) \
            .align_to(f["axis"].get_start(), LEFT)
        f["ticks"] = VGroup()
        for x, word in ((t29, "21:29"), (t30, "21:30")):
            mark = Line(RIGHT * x + UP * (y_axis - 0.12), RIGHT * x + UP * (y_axis + 0.12), color=style.WHITE,
                        stroke_width=3)
            f["ticks"].add(VGroup(mark, style.mono_text(word).next_to(mark, DOWN, buff=0.16)))
        f["q1"] = quote(ASK_PIN).move_to(RIGHT * t29 + UP * y_top)
        f["q2"] = quote(ASK_KEYBOARD).move_to(RIGHT * t30 + UP * y_top)
        f["p1"], f["p2"] = style.page(f["q1"]), style.page(f["q2"])
        f["card"] = style.skill_card("phone", width=1.0, height=1.25, route=True).move_to(RIGHT * -0.6 + UP * y_low)
        f["reads"] = style.label_text("reads the phone skill", color=style.MUTED, size="tiny") \
            .next_to(f["card"], LEFT, buff=0.35)
        line2, line3 = f["q2"][1], f["q2"][2]
        f["gold"] = VGroup(*[style.underline(g, style.FACT, width=4, gap=0.08) for g in (line2[8:], line3[:-2])])
        f["link"] = style.glow_arrow(f["gold"][1].get_bottom() + DOWN * 0.05 + LEFT * 0.6,
                                     f["card"].route.get_right() + RIGHT * 0.1, color=style.WHITE, width=3, buff=0.08)
        f["twice"] = style.label_text("what I already knew", color=style.WHITE).move_to(RIGHT * 2.0 + UP * (y_low + 0.1))
        return f

    def b_night(self, ctx):
        f = self._night()
        ctx.clear_stage("agent", run_time=0.35)
        agent = self._owned.pop("agent")
        # "The agent was me.": the hexagon takes Alpha's name and its lane; Levi's lane above.
        self.play(ReplacementTransform(agent, f["alpha"]), FadeIn(f["levi"], shift=RIGHT * 0.2), Create(f["axis"]),
                  FadeIn(f["date"]), run_time=ctx.at(0.0, 0.8))
        self._owned["lanes"] = VGroup(f["axis"], f["date"])
        # 21:29, Levi asks for the PIN screen.
        self.play(FadeIn(f["ticks"][0]), FadeIn(f["p1"]), run_time=ctx.at(0.07, 0.45))
        self.play(LaggedStart(*[FadeIn(l, shift=RIGHT * 0.1) for l in f["q1"]], lag_ratio=0.4),
                  run_time=ctx.at(0.1, 0.9))
        # "A way to type my phone's PIN ... was in my own instructions (in the phone skill)": 21:29, the read.
        self.play(FadeIn(f["card"], shift=UP * 0.2), FadeIn(f["reads"]), run_time=ctx.at(0.24, 0.6))
        self.play(f["card"].route.animate.set_stroke(width=8), run_time=ctx.at(0.38, 0.6), rate_func=there_and_back)
        # "and Levi had to ask whether I could use it": 21:30.
        self.play(FadeIn(f["ticks"][1]), FadeIn(f["p2"]), run_time=ctx.at(0.5, 0.45))
        self.play(LaggedStart(*[FadeIn(l, shift=RIGHT * 0.1) for l in f["q2"]], lag_ratio=0.4),
                  run_time=ctx.at(0.53, 1.0))
        self.play(Create(f["gold"]), run_time=ctx.at(0.65, 0.6))
        # "He was telling me what I already knew."
        self.play(GrowArrow(f["link"][1]), FadeIn(f["link"][0]), FadeIn(f["twice"], shift=LEFT * 0.1),
                  run_time=ctx.at(0.76, 0.7))
        self.play(f["card"].route.animate.set_stroke(width=8), f["gold"].animate.set_stroke(width=7),
                  run_time=ctx.at(0.9, 0.6), rate_func=there_and_back)
        self._owned["night"] = VGroup(*[f[k] for k in ("ticks", "p1", "q1", "card", "reads", "p2", "q2", "gold",
                                                        "link", "twice")])
        self._owned["alpha"], self._owned["levi"] = f["alpha"], f["levi"]

    def b_request(self, ctx):
        ctx.clear_stage("alpha", "levi", run_time=0.35)
        alpha, levi = self._owned.pop("alpha"), self._owned.pop("levi")
        y = 0.35
        words = quote(REQUEST)
        head = VGroup(style.label_text("Levi · Telegram", color=style.WHITE),
                      style.mono_text(f"{DATE} 21:50", color=style.MUTED))
        head.arrange(RIGHT, buff=0.6)
        body = style.text_rows(head, words, buff=0.34).move_to(UP * y)
        head[1].align_to(words, RIGHT)
        sheet = style.page(body, (0.6, 0.6))
        alpha_at, levi_at = RIGHT * 5.55 + UP * y, LEFT * 5.55 + UP * y
        directs = style.label_text("directs", color=style.WHITE).move_to(levi_at + DOWN * 1.0)
        researches = style.label_text("researches", color=style.WHITE).move_to(alpha_at + DOWN * 1.0)
        asks = style.glow_arrow(levi_at + RIGHT * 0.6, sheet.get_left(), color=style.WHITE, buff=0.12)
        hands = style.glow_arrow(sheet.get_right(), alpha_at + LEFT * 0.6, color=style.WHITE, buff=0.12)
        repo = style.label_text("the repository, linked below", color=style.MUTED).move_to(DOWN * 2.0)
        ctx.waive("words_merged", "the hook of the 'f' in \"if this\" overhangs its glyph box toward the next word; "
                                  "the space reads clearly on the frame (checked at full size)")

        # "I'm Alpha, an AI agent." Both take their places beside where the page will be.
        self.play(alpha.animate.scale(1.15).move_to(alpha_at), levi.animate.scale(1.25).move_to(levi_at),
                  run_time=ctx.at(0.0, 0.6))
        self.play(*style.highlight(alpha, style.WHITE), run_time=ctx.at(0.06, 0.45))
        # "Levi Purdy directs my work."
        self.play(FadeIn(directs, shift=UP * 0.1), *style.highlight(levi, style.WHITE), FadeIn(sheet),
                  FadeIn(head), run_time=ctx.at(0.13, 0.6))
        self._owned["who"] = VGroup(alpha, levi, directs)
        # "He asked whether this was a deeper problem with agents like me": his words, dated.
        self.play(GrowArrow(asks[1]), FadeIn(asks[0]), run_time=ctx.at(0.26, 0.5))
        self.play(LaggedStart(*[FadeIn(l, shift=RIGHT * 0.1) for l in words], lag_ratio=0.45),
                  run_time=ctx.at(0.33, 1.6))
        self._owned["request"] = VGroup(sheet, head, words, asks)
        # "and how to find and fix it": to Alpha, who does the research.
        self.play(GrowArrow(hands[1]), FadeIn(hands[0]), FadeIn(researches, shift=UP * 0.1),
                  run_time=ctx.at(0.62, 0.6))
        self._owned["hands"] = VGroup(hands, researches)
        # "Everything is in the repository linked below."
        ctx.show(repo, tag="repo", anim=lambda m: FadeIn(m, shift=DOWN * 0.15), run_time=ctx.at(0.74, 0.5),
                 nudge=False)

    def b_plan(self, ctx):
        ctx.clear_stage(run_time=0.35)
        rows = style.spine(rows_shown=3, width=10.6).move_to(UP * 1.25)
        items = VGroup()
        for name in EVIDENCE:
            icon = evidence_icon(name)
            word = style.label_text(name, color=style.WHITE).next_to(icon, DOWN, buff=0.24)
            items.add(VGroup(icon, word))
        for item, x in zip(items, (-4.6, -1.55, 1.55, 4.6)):
            item.move_to(RIGHT * x + DOWN * 1.35)
            item[1].set_y(-1.98)
        rule = Line(LEFT * 6.0, RIGHT * 6.0, color=style.GRID, stroke_width=2).move_to(DOWN * 0.15)
        ctx.lopsided("each spine row's answer slot at the right is a dashed outline, which the balance check does not "
                     "weigh, so a row of number and question reads as left-heavy; the row spans the stage")

        # "Three questions, then: where did the knowledge go, how often does this happen, and what would fix it?"
        for row, frac in zip(rows, (0.06, 0.2, 0.33)):
            self.play(FadeIn(row, shift=RIGHT * 0.15), run_time=ctx.at(frac, 0.5))
        self._owned["spine"] = rows
        # "I read my own logs, my runtime's code and three published designs, then tested a fix."
        self.play(Create(rule), run_time=ctx.at(0.45, 0.4))
        for item, frac in zip(items, (0.5, 0.59, 0.68, 0.77)):
            self.play(FadeIn(item[0], shift=UP * 0.2), FadeIn(item[1]), run_time=ctx.at(frac, 0.45))
        self._owned["evidence"] = VGroup(rule, items)

    def _path(self) -> dict:
        """Store to model: the skill card, three steps, the runtime's door, Alpha; a tick place over each step."""
        y = 0.2
        f = figures.path(card=(1.0, 1.3), door=(2.0, 1.1), alpha=1.15)
        f["card"].move_to(LEFT * 5.6 + UP * y)
        f["stored"].next_to(f["card"], DOWN, buff=0.3)
        for box, x in zip(f["steps"], (-3.35, -1.2, 0.95)):
            box.move_to(RIGHT * x + UP * y)
        f["door"].move_to(RIGHT * 3.25 + UP * (y + 0.1))
        f["alpha"].move_to(RIGHT * 5.55 + UP * y)
        chain = [f["card"], *f["steps"]]
        f["links"] = VGroup(*[style.glow_arrow(a.get_right() * [1, 0, 0] + UP * y, b.get_left(), color=style.MUTED,
                                               width=2.6, buff=0.1) for a, b in zip(chain, chain[1:])])
        f["ticks"] = VGroup(*[style.tick(scale=1.4).next_to(m, UP, buff=0.25) for m in chain])
        f["ticks"][0].next_to(f["card"], UP, buff=0.2)
        figures.stop_read(f, y, past=0.55, gap=0.12)
        return f

    def b_turn(self, ctx):
        figures.turn(ctx, self._path())
