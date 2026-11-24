"""
Section 05: three designs. The search for prior art lands three papers (Voyager, MemGPT, Reflexion), not a survey;
Voyager's library, where the harness, not the model, fetches the five closest programs; its Table 1 as two dumbbells
(iron tools in 29 iterations against 21, diamond tools in 0 of 3 runs against 1 of 3); MemGPT's model paging through
results and stopping before the end; Reflexion's memory of one to three reflections inside every attempt; and the
ledger of the three and Alpha: who decides to look, and whether a loss in delivery is measured.

Voyager's figures are video/data.py's (report/report.md, "Three published designs", Table 1); its three runs, the top
five and Reflexion's one to three are the script's and the report's. Papers are drawn in violet, the source colour.
"""
from __future__ import annotations

from manim import *

import data
import style
from pipeline.beats import Beat, BeatScene

PAPERS = (("Voyager", "Wang et al., 2023"), ("MemGPT", "Packer et al., 2023"), ("Reflexion", "Shinn et al., 2023"))
TOP_K = 5                     # Voyager's harness puts the five closest programs in the prompt (script; report)
VOYAGER_RUNS = 3              # diamond tools: runs per arm in Table 1 (script; report)
IRON_AXIS = 30                # the iron-tools row's axis runs from 0 to 30 iterations
REFLECTIONS = 3               # Reflexion keeps one to three (script; report)
LEDGER = (("Voyager", "the harness"), ("Reflexion", "nothing to look for"), ("MemGPT", "the model"),
          ("Alpha", "the model: me"))


def source_head(name: str, who: str) -> Text:
    """The paper a figure is drawn from, at the stage's top left, in the source colour."""
    return style.label_text(f"{name} · {who}", color=style.SOURCE).move_to([-6.4, 2.0, 0], aligned_edge=LEFT)


def program() -> VGroup:
    """One of Voyager's programs: a small violet card, its description line bright above two code lines."""
    body = style.card(0.8, 0.66, style.SOURCE, radius=0.06)
    desc = Line(LEFT * 0.26, RIGHT * 0.26, color=style.SOURCE, stroke_width=3.2)
    code = VGroup(*[Line(LEFT * 0.26, RIGHT * (0.1 if i else 0.2), color=style.MUTED, stroke_width=2,
                         stroke_opacity=0.6) for i in range(2)])
    VGroup(desc, *code).arrange(DOWN, buff=0.1, aligned_edge=LEFT).move_to(body)
    return VGroup(body, desc, code)


def reflection_card(width: float = 1.7, height: float = 1.4) -> VGroup:
    """Reflexion's memory: a violet card named "memory", room for its reflections. VGroup(card, word, lines)."""
    body = style.card(width, height, style.SOURCE)
    word = style.label_text("memory", color=style.SOURCE).next_to(body.get_top(), DOWN, buff=0.16)
    lines = VGroup(*[Line(LEFT * width * 0.32, RIGHT * width * 0.32, color=style.SOURCE, stroke_width=3)
                     for _ in range(REFLECTIONS)]).arrange(DOWN, buff=0.17)
    lines.next_to(word, DOWN, buff=0.2)
    return VGroup(body, word, lines)


class S05Designs(BeatScene):
    """Section 05: three published designs for keeping what an agent knows, and where Alpha sits among them."""

    section_id = "05_three_designs"
    title = "Three Designs"

    def storyboard(self) -> list[Beat]:
        return [
            Beat("Then: how do published agents", self.b_search, kind="search"),
            Beat("Voyager, a Minecraft agent", self.b_voyager, kind="diagram"),
            Beat("Without that library, iron tools", self.b_table, kind="dumbbell"),
            Beat("MemGPT lets the model page", self.b_memgpt, kind="loop"),
            Beat("Reflexion usually keeps one to three", self.b_reflexion, kind="proportional"),
            Beat("I work like MemGPT", self.b_ledger, kind="ledger"),
        ]

    # ------------------------------------------------------------- search --
    def b_search(self, ctx):
        words = style.label_text("how agents keep what they know", color=style.WHITE)
        glass = style.magnifier(radius=0.13, handle=0.14, handle_width=3.4)
        query = VGroup(glass, words).arrange(RIGHT, buff=0.3)
        field = style.card(query.width + 1.0, 0.72)
        query.move_to(field)
        bar = VGroup(field, glass, words).move_to([-0.9, 1.65, 0])
        papers = VGroup()
        for i, (name, who) in enumerate(PAPERS):
            page = style.paper(name).move_to([-4.3 + 3.4 * i, -0.35, 0])
            page[2].set_color(style.WHITE)   # the source colour on its own card is 4.5:1, at the limit
            papers.add(VGroup(page, style.label_text(who, color=style.MUTED).next_to(page, DOWN, buff=0.22)))
        chip = style.boxed(style.label_text("not a survey", color=style.WHITE), style.MUTED).move_to([5.0, -0.35, 0])
        # "Then: how do published agents keep what they know?"
        ctx.show(bar, tag="search", anim=lambda m: FadeIn(m, shift=DOWN * 0.1), run_time=0.5, nudge=False)
        self.play(glass.animate.shift(RIGHT * 0.12), rate_func=there_and_back, run_time=ctx.at(0.08, 0.6))
        # "I read three designs closely": three papers land.
        self.play(LaggedStart(*[FadeIn(p, shift=DOWN * 0.3) for p in papers], lag_ratio=0.35),
                  run_time=ctx.at(0.22, 1.4))
        self._own("papers", papers)
        # "this is not a survey of the field."
        ctx.show(chip, tag="chip", anim=lambda m: FadeIn(m, shift=LEFT * 0.15), run_time=ctx.at(0.72, 0.5),
                 nudge=False)

    # ------------------------------------------------------------ voyager --
    def _voyager(self) -> dict:
        """Voyager's retrieval: the library, the task, the harness, the prompt and the model, laid out left to right."""
        shelf = style.card(3.3, 3.2, style.SOURCE).move_to([-4.35, 0.1, 0])
        progs = VGroup(*[program() for _ in range(9)]).arrange_in_grid(rows=3, cols=3, buff=(0.2, 0.22))
        progs.move_to(shelf)
        filed = style.label_text("programs, filed by description", color=style.MUTED).next_to(shelf, DOWN, buff=0.22)
        task = style.boxed(style.label_text("the task", color=style.WHITE), style.WHITE).move_to([-0.6, 1.55, 0])
        harness = style.boxed(style.label_text("harness", color=style.WHITE), style.MUTED, pad=(0.8, 0.5))
        harness.move_to([-0.6, 0.0, 0])
        prompt = style.card(1.5, 2.5).move_to([2.55, 0.0, 0])
        prompt_word = style.label_text("prompt", color=style.MUTED).next_to(prompt, UP, buff=0.2)
        slots = VGroup(*[Rectangle(width=0.9, height=0.32).set_stroke(style.DIM, width=1.5) for _ in range(TOP_K)])
        slots.arrange(DOWN, buff=0.1).move_to(prompt)
        model = style.node("model", "model", size=1.2).move_to([5.3, 0.0, 0])
        return dict(shelf=shelf, progs=progs, filed=filed, task=task, harness=harness, prompt=prompt,
                    prompt_word=prompt_word, slots=slots, model=model)

    def b_voyager(self, ctx):
        ctx.clear_stage(run_time=0.35)
        v = self._voyager()
        head = source_head(*PAPERS[0])
        # "Voyager, a Minecraft agent, keeps each skill as a program"
        ctx.show(head, v["shelf"], tag="shelf", run_time=0.4, nudge=False)
        self.play(LaggedStart(*[FadeIn(p, scale=0.8) for p in v["progs"]], lag_ratio=0.12), run_time=ctx.at(0.03, 1.2))
        self._own("progs", v["progs"])
        ctx.show(v["task"], v["harness"], v["prompt"], v["prompt_word"], v["slots"], v["model"], tag="parts",
                 run_time=ctx.at(0.2, 0.5), nudge=False)
        # "filed under the embedding of a description the model wrote when it saved it"
        ctx.show(v["filed"], tag="filed", run_time=ctx.at(0.35, 0.4), nudge=False)
        self.play(*[p[1].animate.set_stroke(width=5.5) for p in v["progs"]], run_time=ctx.at(0.4, 0.5))
        self.play(*[p[1].animate.set_stroke(width=3.2) for p in v["progs"]], run_time=ctx.at(0.46, 0.4))
        # "The harness, not the model, fetches the five closest."
        down = style.glow_arrow(v["task"].get_bottom(), v["harness"].get_top(), color=style.WHITE)
        self.play(GrowArrow(down[1]), FadeIn(down[0]), *style.highlight(v["harness"][0], style.WHITE),
                  run_time=ctx.at(0.7, 0.4))
        self._own("down", down)
        self._fetch(ctx, v)

    def _fetch(self, ctx, v: dict):
        """The five closest programs light and their copies go into the prompt's slots; the harness is named."""
        closest = [v["progs"][i] for i in (0, 2, 4, 5, 7)]
        self.play(*[a for p in closest for a in style.highlight(p[0], style.WHITE)], run_time=ctx.at(0.73, 0.3))
        copies = VGroup(*[p.copy() for p in closest])
        self.add(copies)
        self.play(*[c.animate.scale(0.42).move_to(s) for c, s in zip(copies, v["slots"])], run_time=ctx.at(0.75, 0.7))
        self._own("copies", copies)
        feed = style.glow_arrow(v["prompt"].get_right(), v["model"].get_left(), color=style.WHITE, buff=0.12)
        chip = style.boxed(style.label_text("harness, not model", color=style.WHITE), style.WHITE)
        chip.next_to(v["harness"], DOWN, buff=0.55)
        self.play(GrowArrow(feed[1]), FadeIn(feed[0]), FadeIn(chip, shift=UP * 0.1), run_time=ctx.at(0.8, 0.4))
        self._own("named", VGroup(feed, chip))

    # -------------------------------------------------------------- table --
    def _row(self, y: float, name: str, unit: str, hi: int, ticks: tuple[str, str]) -> tuple[VGroup, callable]:
        """A dumbbell row on its own axis from 0 to `hi`: (frame, x of a value)."""
        left, right = -2.6, 5.4
        x = lambda v: left + (right - left) * v / hi   # noqa: E731
        track = style.band(right - left + 1.2, 1.25).move_to([(left + right) / 2 - 0.2, y + 0.15, 0])
        floor = y - 0.62
        axis = Line([left, floor, 0], [right, floor, 0], color=style.MUTED, stroke_width=2)
        axis.set_z_index(style.Z_BACKDROP)
        lo_t = style.label_text(ticks[0], color=style.MUTED).next_to([left, floor, 0], DOWN, buff=0.15)
        hi_t = style.label_text(ticks[1], color=style.MUTED).next_to([right, floor, 0], DOWN, buff=0.15)
        words = style.text_rows(style.label_text(name, color=style.WHITE), style.label_text(unit, color=style.MUTED))
        words.move_to([-6.4, y, 0], aligned_edge=LEFT)
        return VGroup(track, axis, lo_t, hi_t, words), x

    def _dumbbell(self, ctx, x, y: float, values: tuple[int, int], words: tuple[str, str], at: tuple[float, float]):
        """Without, then the line to with: grey end, violet end, each with its value."""
        a = style.end_mark(style.MUTED).move_to([x(values[0]), y, 0])
        b = style.end_mark(style.SOURCE).move_to([x(values[1]), y, 0])
        va = style.caption_text(words[0], color=style.MUTED).next_to(a, UP, buff=0.22)
        vb = style.caption_text(words[1], color=style.SOURCE).next_to(b, UP, buff=0.22)
        self.play(FadeIn(a, scale=0.5), FadeIn(va), run_time=ctx.at(at[0], 0.4))
        bar = Line(a.get_center(), a.get_center() + RIGHT * 0.001, color=style.MUTED, stroke_width=3)
        self.add(bar.set_z_index(style.Z_EDGE))
        self.play(bar.animate.put_start_and_end_on(a.get_center(), b.get_center()), run_time=ctx.at(at[1], 1.0))
        self.play(FadeIn(b, scale=0.5), FadeIn(vb), run_time=ctx.at(at[1] + 0.06, 0.4))
        return VGroup(a, va, bar, b, vb)

    def b_table(self, ctx):
        ctx.clear_stage(run_time=0.35)
        head = style.label_text("Voyager, Table 1", color=style.SOURCE).move_to([-6.4, 2.0, 0], aligned_edge=LEFT)
        key = VGroup(style.end_mark(style.MUTED), style.label_text("without the library", color=style.MUTED),
                     style.end_mark(style.SOURCE), style.label_text("with the library", color=style.SOURCE))
        key.arrange(RIGHT, buff=0.2)
        key[2:].shift(RIGHT * 0.35)
        key.move_to([2.6, 2.0, 0])
        iron, xi = self._row(0.7, "iron tools", "iterations, mean", IRON_AXIS, ("0", str(IRON_AXIS)))
        diamond, xd = self._row(-1.25, "diamond tools", "runs that got there", VOYAGER_RUNS,
                                ("0", str(VOYAGER_RUNS)))
        # "Without that library, iron tools took twenty-nine iterations on average instead of twenty-one"
        ctx.show(head, key, iron, diamond, tag="frame", run_time=0.5, nudge=False)
        first = self._dumbbell(ctx, xi, 0.7, data.VOYAGER_IRON, tuple(map(str, data.VOYAGER_IRON)), (0.05, 0.2))
        self._own("iron", first)
        # "and diamond tools were reached in none of three runs, against one of three with it."
        runs = tuple(f"{v} of {VOYAGER_RUNS}" for v in data.VOYAGER_DIAMOND)
        second = self._dumbbell(ctx, xd, -1.25, data.VOYAGER_DIAMOND, runs, (0.5, 0.78))
        self._own("diamond", second)

    # ------------------------------------------------------------- memgpt --
    def b_memgpt(self, ctx):
        ctx.clear_stage(run_time=0.35)
        head = source_head(*PAPERS[1])
        model = style.node("model", "model", size=1.3).move_to([-3.3, 0.0, 0])
        rows = VGroup(*[style.tile(3.0, 0.34, style.MUTED, opacity=0.18) for _ in range(7)]).arrange(DOWN, buff=0.17)
        rows.move_to([2.7, -0.15, 0])
        named = style.label_text("search results", color=style.MUTED).next_to(rows, UP, buff=0.25)
        go = CurvedArrow(model.get_top() + RIGHT * 0.3, rows.get_left() + LEFT * 0.2 + UP * 1.0, angle=-PI / 3,
                         color=style.WHITE, stroke_width=3)
        back = CurvedArrow(rows.get_left() + LEFT * 0.2 + DOWN * 1.0, model.get_bottom() + RIGHT * 0.3,
                           angle=-PI / 3, color=style.WHITE, stroke_width=3)
        loop_word = style.label_text("next page", color=style.WHITE).next_to(go, UP, buff=0.15)
        # "MemGPT lets the model page through its own memory."
        ctx.show(head, model, rows, named, tag="parts", run_time=0.5, nudge=False)
        self.play(Create(go), Create(back), FadeIn(loop_word), run_time=ctx.at(0.06, 0.7))
        self._read = []
        self._own("loop", VGroup(go, back, loop_word))
        cursor = SurroundingRectangle(rows[0], buff=0.07, color=style.WHITE, stroke_width=3, corner_radius=0.05)
        self.play(Create(cursor), rows[0].animate.set_fill(style.WHITE, opacity=0.5), run_time=ctx.at(0.14, 0.4))
        for i, frac in ((1, 0.25), (2, 0.36)):
            self.play(cursor.animate.move_to(rows[i]), rows[i].animate.set_fill(style.WHITE, opacity=0.5),
                      run_time=ctx.at(frac, 0.5))
        self._own("cursor", cursor)
        self._stop(ctx, model, rows)

    def _stop(self, ctx, model, rows):
        """"will often stop paging before it has exhausted the results": the loop breaks, the rest stays unread."""
        loop, cursor = self._owned["loop"], self._owned["cursor"]
        dim = [a.copy().set_stroke(opacity=0.3) for a in loop[:2]]
        for a in dim:
            a.tip.set_fill(opacity=0.3)
        self.play(*[Transform(a, d) for a, d in zip(loop[:2], dim)], loop[2].animate.set_opacity(0.4),
                  FadeOut(cursor), run_time=ctx.at(0.5, 0.4))
        self._owned.pop("cursor")
        out = style.glow_arrow(model.get_left(), model.get_left() + LEFT * 1.6, color=style.WHITE, buff=0.1)
        early = style.label_text("stops early", color=style.WHITE).next_to(out, DOWN, buff=0.2)
        self.play(GrowArrow(out[1]), FadeIn(out[0]), FadeIn(early), run_time=ctx.at(0.56, 0.5))
        self._own("out", VGroup(out, early))
        rest = rows[3:]
        brace = Brace(rest, RIGHT, color=style.MUTED, buff=0.15)
        unread = style.label_text("never read", color=style.MUTED).next_to(brace, RIGHT, buff=0.15)
        self.play(*[r.animate.set_fill(style.DIM, opacity=0.4).set_stroke(style.DIM) for r in rest], FadeIn(brace),
                  FadeIn(unread),
                  run_time=ctx.at(0.72, 0.6))
        self._own("unread", VGroup(brace, unread))

    # ---------------------------------------------------------- reflexion --
    def _attempts(self) -> VGroup:
        """Three attempts, each a grey context card of its own lines with a slot at the top for the memory."""
        out = VGroup()
        for i in range(3):
            body = style.card(2.6, 3.3).move_to([-2.0 + 3.05 * i, 0.05, 0])
            name = style.label_text(f"attempt {i + 1}", color=style.WHITE).next_to(body.get_top(), DOWN, buff=0.18)
            lines = VGroup(*[Line(LEFT * 0.85, RIGHT * (0.85 if k % 3 else 0.35), color=style.MUTED, stroke_width=2,
                                  stroke_opacity=0.55) for k in range(6)]).arrange(DOWN, buff=0.17, aligned_edge=LEFT)
            lines.next_to(body.get_bottom(), UP, buff=0.3)
            out.add(VGroup(body, name, lines))
        return out

    def b_reflexion(self, ctx):
        ctx.clear_stage(run_time=0.35)
        head = source_head(*PAPERS[2])
        memory = reflection_card().move_to([-5.3, 0.4, 0])
        few = VGroup(style.label_text(f"usually 1 to {REFLECTIONS}", color=style.MUTED),
                     style.label_text("reflections", color=style.MUTED)).arrange(DOWN, buff=0.22).next_to(memory, DOWN, buff=0.25)
        attempts = self._attempts()
        # "Reflexion usually keeps one to three short reflections"
        ctx.show(head, memory[0], memory[1], few, tag="memory", run_time=0.45, nudge=False)
        for k, frac in enumerate((0.04, 0.12, 0.2)):
            self.play(Create(memory[2][k]), run_time=ctx.at(frac, 0.35))
        self._own("lines", memory[2])
        # "and puts all of them into every attempt": a copy of the whole memory goes into each.
        self.play(LaggedStart(*[FadeIn(a, shift=UP * 0.15) for a in attempts], lag_ratio=0.3),
                  run_time=ctx.at(0.3, 0.9))
        self._own("attempts", attempts)
        # The copies leave the word behind: at half size it would be under the legible minimum.
        copies = VGroup(*[style.ignore(VGroup(memory[0], memory[2]).copy()) for _ in attempts])
        self.add(copies)
        self.play(*[c.animate.scale(0.55).next_to(a[1], DOWN, buff=0.2) for c, a in zip(copies, attempts)],
                  run_time=ctx.at(0.36, 0.7))
        for sub in copies.get_family():   # landed: part of the picture from here on
            sub.qa_ignore = False
        self._own("copies", copies)
        # "It keeps so little that all of it fits in every attempt."
        whole = style.caption_text("all of it, in every attempt", color=style.WHITE)
        scale = style.label_text("not to scale", color=style.MUTED)
        VGroup(whole, scale).arrange(RIGHT, buff=0.6).move_to([1.05, -1.95, 0])
        style.sit(scale, style.baseline(whole))
        self.play(*[a for c in copies for a in style.highlight(c[0], style.SOURCE)], FadeIn(whole),
                  run_time=ctx.at(0.5, 0.5))
        ctx.show(scale, tag="scale", run_time=ctx.at(0.58, 0.3), nudge=False)
        self._own("whole", whole)

    # ------------------------------------------------------------- ledger --
    def _ledger(self) -> tuple[VGroup, VGroup, list]:
        """The ledger's frame: (heads, rows of band and name, the y of each row)."""
        ys = [1.05, 0.3, -0.45, -1.2]
        heads = VGroup(style.label_text("who decides to look", color=style.MUTED).move_to([-2.9, 1.8, 0],
                                                                                         aligned_edge=LEFT),
                       style.label_text("delivery loss measured?", color=style.MUTED).move_to([1.9, 1.8, 0],
                                                                                             aligned_edge=LEFT))
        rows = VGroup()
        for (name, _), y in zip(LEDGER, ys):
            band = style.band(13.0, 0.62).move_to([0, y, 0])
            word = style.model_mark(name) if name == "Alpha" else style.label_text(name, color=style.SOURCE)
            rows.add(VGroup(band, word.move_to([-6.2, y, 0], aligned_edge=LEFT)))
        return heads, rows, ys

    def _dropped(self, y: float) -> VGroup:
        """Alpha's answer in the second column: a read that stops red at a door, and "this study"."""
        gate = style.door(height=0.56, width=0.5, label=False)
        path = style.read_path(LEFT * 1.0, gate[0].get_left(), served=False, width=3.2)
        path[1].stretch_to_fit_height(0.36).next_to(gate[0], LEFT, buff=0.02)
        mark = VGroup(path, gate)
        words = style.label_text("this study", color=style.WHITE)
        return VGroup(mark, words).arrange(RIGHT, buff=0.3).move_to([1.9, y, 0], aligned_edge=LEFT)

    def b_ledger(self, ctx):
        ctx.clear_stage(run_time=0.35)
        heads, rows, ys = self._ledger()
        who = VGroup(*[style.label_text(text, color=style.WHITE).move_to([-2.9, y, 0], aligned_edge=LEFT)
                       for (_, text), y in zip(LEDGER, ys)])
        # "I work like MemGPT: I decide when to look."
        ctx.show(heads, rows, tag="frame", run_time=0.45, nudge=False)
        self.play(LaggedStart(*[FadeIn(w, shift=RIGHT * 0.1) for w in who], lag_ratio=0.25), run_time=ctx.at(0.03, 1.0))
        self._own("who", who)
        brace = Brace(VGroup(who[2], who[3]), RIGHT, color=style.WHITE, buff=0.2)
        same = style.label_text("same", color=style.WHITE).next_to(brace, RIGHT, buff=0.15)
        self.play(FadeIn(brace), FadeIn(same), *[w.animate.set_color(style.WHITE) for w in who[2:]],
                  *[w.animate.set_opacity(0.55) for w in who[:2]], run_time=ctx.at(0.12, 0.5))
        self._own("same", VGroup(brace, same))
        # "But none of the three measures what happened to me"
        nots = VGroup(*[style.label_text("not measured", color=style.MUTED).move_to([1.9, y, 0], aligned_edge=LEFT)
                        for y in ys[:3]])
        ctx.at(0.25)
        self.play(FadeOut(brace), FadeOut(same), run_time=0.25)
        self._owned.pop("same")
        self.play(LaggedStart(*[FadeIn(t, shift=RIGHT * 0.1) for t in nots], lag_ratio=0.3), run_time=ctx.at(0.27, 0.9))
        self._own("nots", nots)
        # "a store that holds the knowledge while the path that delivers it drops it."
        ctx.show(self._dropped(ys[3]), tag="dropped", run_time=ctx.at(0.5, 0.5), nudge=False)
        # "That's my reading of three papers."
        reading = style.caption_text("my reading of three papers", color=style.MUTED).move_to([0, -1.95, 0])
        ctx.show(reading, tag="reading", run_time=ctx.at(0.74, 0.4), nudge=False)
