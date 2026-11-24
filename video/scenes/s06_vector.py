"""
Section 06: a vector database? Levi's line of 2026-11-23 21:50, the strongest case against; an illustration (dashed,
no numbers on its axes, labelled so) of knowledge growing past a prompt that does not, where the index stops fitting
and retrieval by meaning is needed, splitting one file a patch; Voyager and MemGPT past that point; Alpha's index
opened, fifteen lines in about 5,500 characters with the phone's line lit and seen; and the path again, with a vector
store doing the finding: found, chosen, still stopped red at the door.

The index's size is video/data.py's (report/report.md, "A vector database"). The other fourteen skills' lines are drawn
as unnamed grey rules: the video shows only the phone's. The line chart is an illustration, not data: its curve's shape
is invented, and it says so on screen.
"""
from __future__ import annotations

from manim import *

import data
import style
from pipeline import charts
from pipeline.beats import Beat, BeatScene

LEVI_WHEN = "2026-11-23 21:50"
LEVI_LIT = ("First thing that comes to mind", "is vector databases,")
LEVI_REST = "but it could be something else."
PHONE_ROW = 6                 # where the phone's line sits in the drawn index (the order is not shown)
ROOM = 0.55                   # the illustration's prompt, as a share of its y axis


def knows(x: float) -> float:
    """The illustration's knowledge curve over x in 0..10: an invented shape that grows ever faster."""
    return 0.1 + 0.85 * (x / 10) ** 1.7


CROSS = 10 * ((ROOM - 0.1) / 0.85) ** (1 / 1.7)    # where knows(x) reaches ROOM


def levi_note() -> VGroup:
    """Levi's line on a page, his circle in its header: VGroup(page, head, VGroup(lit lines, the rest))."""
    lit = style.text_rows(*[style.caption_text(t, color=style.MUTED) for t in LEVI_LIT], buff=0.24)
    words = style.text_rows(lit, style.caption_text(LEVI_REST, color=style.MUTED), buff=0.24)
    return style.person_page("Levi", "Telegram", LEVI_WHEN, words)


def index_rows() -> VGroup:
    """Alpha's index as drawn: fifteen rows, the phone's named in monospace and the rest unnamed grey rules."""
    rows = VGroup()
    for i in range(data.INDEX_SKILLS):
        if i == PHONE_ROW:
            rows.add(style.mono_text("- phone", color=style.MUTED, size="label"))
        else:
            rows.add(Line(ORIGIN, RIGHT * (1.4 + 1.4 * ((i * 7) % 5) / 4), color=style.MUTED, stroke_width=4,
                          stroke_opacity=0.6))
    return rows.arrange(DOWN, buff=0.17, aligned_edge=LEFT)


class S06Vector(BeatScene):
    """Section 06: Levi's vector database at its best, and why it would not have helped this time."""

    section_id = "06_a_vector_database"
    title = "A Vector Database?"

    def storyboard(self) -> list[Beat]:
        return [
            Beat("Levi's first idea was a vector", self.b_request, kind="request"),
            Beat("Knowledge keeps growing", self.b_line, kind="line"),
            Beat("That's right about where retrieval", self.b_papers),
            Beat("My index lists fifteen skills", self.b_index, kind="cutaway"),
            Beat("This time a vector store", self.b_flow, kind="flow"),
        ]

    # ------------------------------------------------------------ request --
    def b_request(self, ctx):
        note = levi_note().move_to([-1.5, 0.3, 0])
        page, head, (lit, rest) = note
        case = style.boxed(style.text_rows(style.label_text("the strongest case", color=style.WHITE),
                                           style.label_text("against my answer", color=style.WHITE)), style.WHITE)
        case.move_to([4.6, 0.3, 0])
        # "Levi's first idea was a vector database."
        ctx.show(page, head, tag="page", run_time=0.4, nudge=False)
        self.play(LaggedStart(*[FadeIn(t, shift=RIGHT * 0.1) for t in (*lit, rest)], lag_ratio=0.3),
                  run_time=ctx.at(0.04, 0.9))
        self._own("words", VGroup(lit, rest))
        vector = lit[1][len("is"):len("isvectordatabases")]
        under = style.underline(vector, width=2.4)
        self.play(*[t.animate.set_color(style.WHITE) for t in lit], run_time=ctx.at(0.2, 0.5))
        self.play(Create(under), run_time=ctx.at(0.28, 0.4))
        self._own("under", under)
        # "It's the strongest case against my answer, so here it is at its best."
        ctx.show(case, tag="case", anim=lambda m: FadeIn(m, shift=LEFT * 0.2), run_time=ctx.at(0.3, 0.5),
                 nudge=False)
        self.play(*style.highlight(case[0], style.WHITE), run_time=ctx.at(0.75, 0.4))

    # --------------------------------------------------------------- line --
    def _chart(self) -> dict:
        """The illustration: axes without numbers, the prompt's room and knowledge as dashed lines, their labels."""
        plot = charts.Plot((-5.9, -1.85, 0), 9.0, 3.6, (0, 10), (0, 1), x_title="time", y_title="size")
        panel = style.band(12.9, 3.9).move_to([0.15, -0.0, 0])   # wide enough for the labels at the right
        room = DashedVMobject(charts.line(plot, [(0, ROOM), (10, ROOM)], color=style.MUTED, width=3), num_dashes=40)
        grow = DashedVMobject(charts.line(plot, [(x / 4, knows(x / 4)) for x in range(41)], color=style.WHITE,
                                          width=3.4), num_dashes=60)
        room_word = style.label_text("room in the prompt", color=style.MUTED).next_to(plot.at(10, ROOM), RIGHT,
                                                                                    buff=0.2)
        grow_word = style.label_text("what the agent knows", color=style.WHITE).next_to(plot.at(10, knows(10)),
                                                                                     RIGHT, buff=0.2)
        note = style.label_text("illustration, not data", color=style.MUTED)
        tag = VGroup(style.card(note.width + 0.5, note.height + 0.36, dashed=True), note)
        note.move_to(tag[0])
        tag.move_to(plot.at(0, 0.97) + RIGHT * 0.45, aligned_edge=UL)
        return dict(panel=panel, plot=plot, room=room, grow=grow, room_word=room_word, grow_word=grow_word, tag=tag)

    def b_line(self, ctx):
        ctx.clear_stage(run_time=0.35)
        c = self._chart()
        plot = c["plot"]
        # "Knowledge keeps growing, and the prompt doesn't."
        ctx.show(c["panel"], plot, c["room"], c["room_word"], c["tag"], tag="chart", run_time=0.45, nudge=False)
        self.play(Create(c["grow"]), run_time=ctx.at(0.04, 2.4), rate_func=linear)
        ctx.show(c["grow_word"], tag="grow_word", run_time=ctx.at(0.26, 0.3), nudge=False)
        self._own("grow", c["grow"])
        # "One day the index can't list every skill"
        cross = Dot(plot.at(CROSS, ROOM), radius=0.1, color=style.WHITE)
        stops = style.label_text("index stops fitting", color=style.WHITE).move_to(plot.at(CROSS, ROOM) + UL * 0.5)
        stops.shift(LEFT * (stops.width / 2 - 0.3))
        ctx.show(cross, stops, tag="cross", anim=lambda m: FadeIn(m, scale=1.3), run_time=ctx.at(0.32, 0.4),
                 nudge=False)
        # "and retrieval by meaning is the only way."
        region = Rectangle(width=plot.at(10, 0)[0] - plot.at(CROSS, 0)[0], height=3.6, stroke_width=0)
        region.set_fill(style.GRID, opacity=0.6).move_to(plot.at(CROSS, 0), aligned_edge=DL)
        region.set_z_index(style.Z_BACKDROP)
        need = style.label_text("retrieval by meaning", color=style.WHITE)
        need.next_to(region, UP, buff=0.25)
        ctx.show(region, need, tag="region", run_time=ctx.at(0.58, 0.5), nudge=False)
        # "Splitting one file is a patch."
        at = plot.at(3, knows(3))
        mark = Line(at + UP * 0.22, at + DOWN * 0.22, color=style.WHITE, stroke_width=4)
        patch = style.label_text("split one file: a patch", color=style.MUTED).next_to(at, DOWN, buff=0.35)
        ctx.show(mark, patch, tag="patch", run_time=ctx.at(0.82, 0.4), nudge=False)
        self._plot = plot

    # ------------------------------------------------------------- papers --
    def b_papers(self, ctx):
        plot = self._plot
        papers = VGroup(*[style.paper(name, width=1.15, height=1.2) for name in ("Voyager", "MemGPT")])
        for p in papers:
            p[2].set_color(style.WHITE)   # the source colour on its own card is 4.5:1, at the limit
        papers.arrange(RIGHT, buff=0.25).move_to((plot.at(CROSS, 0) + plot.at(10, ROOM)) / 2 + UP * 0.12)
        # "That's right about where retrieval helps."
        self.play(Indicate(self._owned["region"][1], color=style.WHITE, scale_factor=1.12), run_time=ctx.at(0.02, 0.8))
        # "In Voyager and MemGPT the libraries are too big to list in the prompt"
        ctx.show(papers, tag="papers", anim=lambda m: LaggedStart(*[FadeIn(p, shift=DOWN * 0.4) for p in m],
                                                                  lag_ratio=0.4), run_time=ctx.at(0.25, 0.9),
                 nudge=False)
        # "and retrieval does the choosing."
        self.play(*[a for p in papers for a in style.highlight(p[0], style.SOURCE)], run_time=ctx.at(0.72, 0.5))
        self.play(self._owned["grow"].animate.set_stroke(width=5), run_time=ctx.at(0.8, 0.5))

    # -------------------------------------------------------------- index --
    def b_index(self, ctx):
        ctx.clear_stage(run_time=0.35)
        me = style.alpha(size=1.3).move_to([-5.3, 0.1, 0])
        prompt = style.card(4.6, 4.3).move_to([-0.6, 0.0, 0])
        head = style.label_text("my prompt · the index", color=style.MUTED).next_to(prompt.get_top(), DOWN, buff=0.2)
        rows = index_rows().next_to(head, DOWN, buff=0.25).align_to(prompt, LEFT).shift(RIGHT * 0.5)
        shut = style.card(0.8, 1.0).move_to([-3.6, 0.1, 0])
        count = style.text_rows(style.caption_text(f"{data.INDEX_SKILLS} skills"),
                                style.label_text(f"about {data.INDEX_CHARS:,} characters", color=style.MUTED))
        count.move_to([4.5, 0.6, 0])
        # "My index lists fifteen skills": the prompt beside me opens.
        ctx.show(me, shut, tag="me", run_time=0.35, nudge=False)
        self.play(ReplacementTransform(shut, prompt), run_time=ctx.at(0.06, 0.6))
        self._owned["me"] = me
        self._own("prompt", VGroup(prompt, head))
        self.play(FadeIn(head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.1) for r in rows], lag_ratio=0.12),
                  run_time=ctx.at(0.12, 1.3))
        self._own("rows", rows)
        # "in about fifty-five hundred characters"
        ctx.show(count, tag="count", run_time=ctx.at(0.3, 0.4), nudge=False)
        # "and it showed me the phone skill's line."
        phone = rows[PHONE_ROW]
        ring = SurroundingRectangle(phone, buff=0.08, color=style.WHITE, stroke_width=2.6, corner_radius=0.05)
        seen = style.glow_arrow([prompt.get_left()[0] - 0.05, phone.get_y(), 0], me.get_right() + RIGHT * 0.05,
                                color=style.WHITE, buff=0.05)
        self.play(phone.animate.set_color(style.WHITE), Create(ring), run_time=ctx.at(0.62, 0.4))
        self.play(GrowArrow(seen[1]), FadeIn(seen[0]), run_time=ctx.at(0.68, 0.4))
        check = VGroup(style.tick(scale=0.8), style.label_text("seen", color=style.WHITE)).arrange(RIGHT, buff=0.15)
        check.next_to(seen, UP, buff=0.15)
        ctx.show(check, tag="seen", run_time=ctx.at(0.74, 0.3), nudge=False)
        self._own("lit", VGroup(ring, seen))

    # --------------------------------------------------------------- flow --
    def _path(self) -> dict:
        """The path from 01 with a vector store doing the finding: skill, store, door, Alpha, and their links."""
        y = -0.45
        skill = style.skill_card("phone", route=True, width=1.25, height=1.6).move_to([-5.0, y, 0])
        gate = style.door(height=2.0, width=1.2).move_to([0.7, y, 0])
        me = style.alpha(size=1.2).move_to([5.0, y, 0])
        store = style.boxed(style.label_text("vector store", color=style.WHITE), style.MUTED, pad=(0.6, 0.45))
        store.move_to([-0.6, 1.75, 0])
        ask = style.glow_arrow(me.get_top() + LEFT * 0.2, store.get_right(), color=style.WHITE)
        find = style.glow_arrow(store.get_left(), skill.get_top() + RIGHT * 0.2, color=style.WHITE)
        found = VGroup(style.tick(scale=0.8), style.label_text("found", color=style.WHITE)).arrange(RIGHT, buff=0.15)
        found.move_to(find.get_center() + LEFT * 0.45 + UP * 0.5)
        chosen = VGroup(style.tick(scale=0.8), style.label_text("chosen", color=style.WHITE)).arrange(RIGHT, buff=0.15)
        chosen.next_to(me, DOWN, buff=0.3)
        read = style.read_path(skill.get_right() + RIGHT * 0.1, gate[0].get_left() + LEFT * 0.05, served=False)
        lost = style.label_text("lost in delivery", color=style.WHITE).next_to(gate[:3], DOWN, buff=0.3)
        return dict(skill=skill, gate=gate, me=me, store=store, ask=ask, find=find, found=found, chosen=chosen,
                    read=read, lost=lost)

    def b_flow(self, ctx):
        ctx.clear_stage(run_time=0.35)
        p = self._path()
        # "This time a vector store wouldn't have helped."
        ctx.show(p["skill"], p["gate"], p["me"], p["store"], tag="path", run_time=0.45, nudge=False)
        self.play(GrowArrow(p["ask"][1]), FadeIn(p["ask"][0]), GrowArrow(p["find"][1]), FadeIn(p["find"][0]),
                  run_time=0.5)
        self._own("links", VGroup(p["ask"], p["find"]))
        # "The skill was found and chosen."
        ctx.show(p["found"], tag="found", anim=lambda m: FadeIn(m, scale=1.3), run_time=0.3,
                 nudge=False)
        ctx.show(p["chosen"], tag="chosen", anim=lambda m: FadeIn(m, scale=1.3), run_time=0.3,
                 nudge=False)
        # "It was lost in delivery."
        path, bar = p["read"]
        self.play(Create(path), run_time=0.35, rate_func=rush_into)
        self.play(FadeIn(bar, scale=1.6), FadeIn(p["lost"]), run_time=0.3)
        self._own("read", VGroup(p["read"], p["lost"]))
