"""
The episode's figures that more than one scene draws: the shelf and its question and the path from store to model
(01 and the Short), the runtime's refusal on its page (02 and the Short), and the search of the session log (03 and
the Short). A scene lays a figure out for its own frame; its words and its animation are here once, so the Short's
text stays the main video's (the gate's `teaser_text`).
"""
from __future__ import annotations

from manim import *

import data
import style

STEPS = ("indexed", "chosen", "read")
# The runtime's refusal, verbatim (OpenClaw 2026.9.8), broken into lines, and its two lit phrases by line.
REFUSAL = ("Skill instructions cannot be partially served:", "the whole document exceeds this call's read",
           "or model-context budget.", "Ask the operator to reduce the document", "or increase the model context.")
LIT = ((0, "cannot be partially served"), (3, REFUSAL[3]))
QUERY = "every skill read, {} to {}".format(*data.SEARCHED)


def plank(cards: Mobject) -> Line:
    """The shelf's ground under a row of skill cards."""
    return Line(cards.get_corner(DL) + DOWN * 0.12 + LEFT * 0.15, cards.get_corner(DR) + DOWN * 0.12
                + RIGHT * 0.15, color=style.MUTED, stroke_width=3)


def legs(a, b, c, d) -> VGroup:
    """The path toward the agent, broken around the question: dashed from a to b and from c to d."""
    return VGroup(DashedLine(a, b, color=style.MUTED), DashedLine(c, d, color=style.MUTED)).set_stroke(width=3) \
        .set_z_index(style.Z_EDGE)


def question(ctx, f: dict, drop: tuple[float, float], enter) -> None:
    """The shelf drops in by `drop` (first card, then more per card), the agent enters along `enter`; the route lit,
    the path toward the agent broken with the question in the gap, the gold lost on the way. f: cards, phone, agent,
    plank, files, legs, ask."""
    scene, cards, agent, phone = ctx.scene, f["cards"], f["agent"], f["phone"]
    for i, c in enumerate(cards):
        c.shift(UP * (drop[0] + drop[1] * i))
    scene.add(cards)
    scene.play(*[c.animate.shift(DOWN * (drop[0] + drop[1] * i)) for i, c in enumerate(cards)],
               FadeIn(agent, shift=enter), run_time=ctx.at(0.0, 0.9))
    scene._owned["shelf"], scene._owned["agent"] = cards, agent
    # "has a skill written down in its own files": the shelf's ground, and the route lit in the phone card.
    scene.play(Create(f["plank"]), FadeIn(f["files"], shift=UP * 0.1), run_time=ctx.at(0.13, 0.5))
    scene._owned["plank"] = VGroup(f["plank"], f["files"])
    scene.play(phone.route.animate.set_stroke(width=8), run_time=ctx.at(0.24, 0.4), rate_func=there_and_back)
    # "and doesn't use it when it's needed": the path toward the agent, broken, and the question in the gap.
    scene.play(Create(f["legs"]), *style.highlight(agent, style.WHITE), run_time=ctx.at(0.4, 0.7))
    ctx.show(f["ask"], tag="ask", anim=lambda m: FadeIn(m, scale=0.5), run_time=ctx.at(0.5, 0.45), nudge=False)
    scene._owned["legs"] = f["legs"]
    ghost = style.ignore(style.route_line(0.5).move_to(phone.route))
    scene.add(ghost)
    scene.play(ghost.animate.move_to(f["legs"][0].get_end()).set_opacity(0), run_time=ctx.at(0.6, 1.0),
               rate_func=rush_into)
    scene.remove(ghost)
    # "Did it forget?"
    scene.play(Indicate(f["ask"], color=style.WHITE, scale_factor=1.18), run_time=ctx.at(0.8, 0.7))


def path(card: tuple[float, float], door: tuple[float, float], alpha: float) -> dict:
    """Store to model, to be laid out: the phone card (width, height) and "stored", the three steps, the runtime's
    door (height, width) and Alpha."""
    f = {"card": style.skill_card("phone", width=card[0], height=card[1], route=True),
         "stored": style.label_text("stored"), "steps": VGroup(*[style.boxed(style.label_text(w)) for w in STEPS]),
         "door": style.door(height=door[0], width=door[1]), "alpha": style.alpha(size=alpha)}
    for box in f["steps"]:
        box[0].stretch_to_fit_width(1.6)
    return f


def stop_read(f: dict, y: float, past: float, gap: float) -> None:
    """The read from the last step at height y, stopped red `past` the door's left post, and the dashed rest of the
    way to within `gap` of Alpha: f["read"], f["beyond"]."""
    stop = f["door"][0].get_x() + past
    f["read"] = style.read_path(f["steps"][-1].get_right() + RIGHT * 0.06, None, served=False, stop_at=[stop, y, 0])
    f["beyond"] = DashedLine([stop + 0.3, y, 0], f["alpha"].get_left() + LEFT * gap, color=style.DIM,
                             stroke_width=2.4).set_z_index(style.Z_EDGE)


def turn(ctx, f: dict) -> None:
    """The path laid out in f (path(), its links and ticks, stop_read()) shown whole, ticked step by step with the
    gold route travelling along, until the read stops red at the door."""
    scene = ctx.scene
    ctx.clear_stage(run_time=0.35)
    # "The first answer surprised me.": the whole path, store to model.
    scene.play(FadeIn(f["card"]), FadeIn(f["stored"]), LaggedStart(*[FadeIn(s) for s in f["steps"]], lag_ratio=0.2),
               FadeIn(f["links"]), FadeIn(f["door"]), FadeIn(f["alpha"]), Create(f["beyond"]),
               run_time=ctx.at(0.0, 0.8))
    scene._owned["path"] = VGroup(*[f[k] for k in ("card", "stored", "steps", "links", "door", "alpha", "beyond")])
    # "Nothing was forgotten. I found the file, chose it and asked for it": a tick on each step, the gold with them.
    ghost = style.ignore(style.route_line(0.5).move_to(f["card"].route))
    scene.add(ghost)
    for i, frac in enumerate((0.2, 0.38, 0.5, 0.6)):
        target = (f["card"].route if i == 0 else f["steps"][i - 1][0]).get_center()
        scene.play(Create(f["ticks"][i]), ghost.animate.move_to(target), run_time=ctx.at(frac, 0.45))
    scene._owned["ticks"] = f["ticks"]
    # "and my runtime refused to hand it over": the read stops red at the door; the gold goes no further.
    scene.play(Create(f["read"][0]), ghost.animate.move_to(f["read"][1]), run_time=ctx.at(0.7, 0.6),
               rate_func=rush_into)
    scene.play(FadeIn(f["read"][1], scale=1.6), ghost.animate.set_opacity(0), f["alpha"].animate.set_opacity(0.4),
               run_time=ctx.at(0.78, 0.45))
    scene.remove(ghost)
    scene._owned["read"] = f["read"]
    scene.play(f["read"][1].animate.scale(1.25), run_time=ctx.at(0.9, 0.5), rate_func=there_and_back)


def glyphs(text: Text, source: str, phrase: str) -> VGroup:
    """The glyphs of `phrase` inside a Text built from `source` (a Text holds no glyph for a space)."""
    first = len(source[:source.index(phrase)].replace(" ", ""))
    return VGroup(*text.submobjects[first:first + len(phrase.replace(" ", ""))])


def refusal_marks(rows: list[Text]) -> tuple[VGroup, list]:
    """For the refusal's rows (one Text per line of REFUSAL): the underlines of its two lit phrases, and every glyph
    outside them."""
    lit = [glyphs(rows[i], REFUSAL[i], p) for i, p in LIT]
    unlit = [g for row in rows for g in row if not any(g in m for m in lit)]
    return VGroup(*[style.underline(m) for m in lit]), unlit


def refuse(ctx, f: dict, bar_at: float) -> None:
    """The refusal on its page (f: sheet, head, bar, rows, marks, unlit): line by line beside its stop bar, which
    grows at `bar_at`; its first phrase underlined; the second, as the rest steps back; the bar pulsing."""
    scene = ctx.scene
    ctx.clear_stage(run_time=0.35)
    # "The runtime answered:" its words, line by line, on a page marked as a refused read.
    ctx.show(f["sheet"], f["head"], tag="sheet", run_time=0.45, nudge=False)
    scene.play(GrowFromCenter(f["bar"]), run_time=ctx.at(bar_at, 0.4))
    for row, frac in zip(f["rows"], (0.06, 0.13, 0.2, 0.27, 0.34)):
        scene.play(FadeIn(row, shift=RIGHT * 0.1), run_time=ctx.at(frac, 0.45))
    scene._owned["refusal"] = VGroup(f["bar"], *f["rows"])
    # "Skill instructions cannot be partially served."
    scene.play(Create(f["marks"][0]), run_time=ctx.at(0.42, 0.5))
    # "Ask the operator to reduce the document": the second phrase lit, the rest steps back.
    scene.play(Create(f["marks"][1]), *[g.animate.set_color(style.MUTED) for g in f["unlit"]],
               run_time=ctx.at(0.72, 0.6))
    scene._owned["marks"] = f["marks"]
    scene.play(Indicate(f["bar"], color=style.REFUSED, scale_factor=1.1), run_time=ctx.at(0.88, 0.6))


def search(field: Mobject, panel: Mobject, rows: tuple[int, float, float, float], hits: tuple[int, ...]) -> dict:
    """The query typed in `field` over the session log in `panel` (both placed cards), its rows ruled (count, long,
    short at the left, short at the right), the rows `hits` marked, and "bad luck?" to place."""
    count, long, left, right = rows
    glass = style.magnifier().move_to(field.get_left() + RIGHT * 0.4)
    name = style.label_text("session log", color=style.MUTED)
    name.move_to(panel.get_corner(UL) + RIGHT * 0.25 + DOWN * 0.2, aligned_edge=UL)
    lines = VGroup(*[Line(LEFT * (long if i % 3 else left), RIGHT * (long if i % 2 else right), color=style.DIM,
                          stroke_width=3) for i in range(count)])
    lines.arrange(DOWN, buff=0.2, aligned_edge=LEFT).move_to(panel).shift(DOWN * 0.15 + RIGHT * 0.2)
    lit = VGroup(*[lines[i] for i in hits])
    return {"field": field, "glass": glass, "query": style.mono_text(QUERY).next_to(glass, RIGHT, buff=0.3),
            "panel": panel, "name": name, "rows": lines, "hits": lit,
            "marks": VGroup(*[Dot(radius=0.07, color=style.WHITE).next_to(r, LEFT, buff=0.18) for r in lit]),
            "luck": style.boxed(style.label_text("bad luck?"), style.WHITE)}
