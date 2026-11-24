"""
Visual system for episode 004, "Found, chosen, refused: why an AI agent lost a skill it had". This docstring is the
frame review's rubric (pipeline/gemini_review.py reads it). One source of truth for palette, type scale and shape
grammar: scenes never hardcode a colour or a font size; they ask for a role or a helper below.

The palette is Levi's video 2's. The grammar, for this episode (a shape and its colour mean one thing for the whole
video; emphasis brightens a shape in its own colour, never turns it into another kind):

    skill       a portrait page card, white stroke, its file name in monospace above ruled lines; its height follows
                its size where size matters (skill_card); a paper's skills or memory are violet, as their source
    PIN route   one gold line inside a skill card (or a side file, or a worker's brief): that piece of knowledge, and
                gold means nothing else; Levi's words naming it (the Bluetooth keyboard) are underlined in gold
    model       a white hexagon: a language model. Alpha's is named "Alpha" (the agent and its chat model; it
                narrates in the first person); a paper's model is named "model"
    person      a white circle (Levi, who directs; "the person asking")
    runtime     a blue door: two posts and a lintel with an opening; every read passes through it (door)
    budget      a cyan rule across the door's opening, labelled with its size in characters (budget_rule)
    read        a path from a skill to Alpha through the door: green when served, stopped at the door with a red bar
                when refused (read_path)
    index       a row or column of short grey lines, one per skill; the one Alpha sees is lit white (index_list)
    worker      a white square; its brief is a small card it receives, with a gold line when it carries the route
    setting     a grey plate with its value in monospace (plate): a number from Alpha's configuration
    source      a violet page card with its short name (paper): a published paper or post
    run         one dot per run of the test: green when the knowledge got through, red when it did not
    spine       the episode's scorecard: three questions, one row each, filled in as the video answers them

Charts take the shape of their data (pipeline/charts.py): counts are dots or squares you can count; before and after
is a slope or a dumbbell; a share is a stacked bar. A figure from a published paper is drawn in violet and labelled
with its source. A guide, a projection or an illustration is dashed and says so.

Claim kinds (rule 3.3), on a chip in the caption lane with the source:
    measured  green   counted from the runs or Alpha's own log, or read in the runtime
    reported  grey    what a paper, a post, a listing or the runtime's source says
    argued    grey    a reading of the evidence
    guess     amber   my inference, no measurement behind it
    levi      white   Levi's own words
Red is reserved for a refused read, a run where the knowledge did not get through, and a struck claim.
"""
from __future__ import annotations

from manim import *

# ---------------------------------------------------------------- palette ---
BG = "#00020A"
PANEL = "#070C1A"
PANEL_HI = "#0C1426"
GRID = "#1F2B42"
WHITE = "#F4F7FF"
MUTED = "#8791A8"
DIM = "#4A5468"

CYAN = "#20F7D2"
BLUE = "#4D8DFF"
VIOLET = "#B45CFF"
GOLD = "#FFCB4D"
RED = "#FF4D6D"
GREEN = "#49F28D"
AMBER = "#FF9E45"
PINK = "#FF7AD9"
PALE_BLUE = "#A9C8FF"
PALE_CYAN = "#9DFBEA"
LIME = "#C8F04A"

# Shape grammar: the contract the storyboard promises the viewer.
NODE_KINDS = {
    "model": {"color": WHITE, "shape": "hexagon"},
    "person": {"color": WHITE, "shape": "circle"},
    "agent": {"color": WHITE, "shape": "diamond"},
    "file": {"color": WHITE, "shape": "document"},
    "step": {"color": MUTED, "shape": "record"},
}

# What this episode's colours mean (the grammar in the docstring).
FACT = GOLD        # the PIN route: the piece of knowledge, wherever it is
SERVED = GREEN     # a read the runtime served; a run where the knowledge got through
REFUSED = RED      # a read the runtime refused; a run where it did not; a claim that did not survive
RUNTIME = BLUE     # the runtime's door
BUDGET = CYAN      # the budget: the rule across the door, at 16,000 characters
SOURCE = VIOLET    # a published source

CLAIM_KINDS = {
    "measured": GREEN,
    "reported": MUTED,
    "argued": MUTED,
    "guess": AMBER,
    "levi": WHITE,
}

# ------------------------------------------------------------- type scale ---
# Sizes are in Manim font_size units, tuned so the smallest is still legible
# after a 480p preview downscale. QA enforces MIN_FONT_SIZE.
TYPE = {
    "title": 40,
    "caption": 28,
    "label": 22,
    "node": 17,
    "field": 17,
    # 17, not 16. Pango's space advance rounds down a whole pixel below 17pt, so
    # every multi-word label set at 16 rendered with a ~3.5px word gap at review
    # size and read as one word — "makes an" as "makesan". At 17 the same phrases
    # come out at 6px. One point of type size, and a whole class of defect.
    "tiny": 17,
}
MIN_FONT_SIZE = 15
MONO = "DejaVu Sans Mono"

# Texts need air between them, not merely an absence of overlap. Below this gap
# two lines read as one block. Both the placement helper and the gate use this
# number, so a layout that satisfies the placer cannot fail the gate.
MIN_TEXT_GAP = 0.16

# The placer aims for MIN_TEXT_GAP + this, never for MIN_TEXT_GAP itself. Aiming
# exactly at a threshold lands on the wrong side of it about half the time once
# floating point is involved: the first version placed three labels at a
# computed 0.16 and the gate read all three back as 0.15999 and failed them.
PLACEMENT_MARGIN = 0.03

# ----------------------------------------------------------- draw layers ---
# Manim's renderer flattens the whole scene and sorts it by ``z_index`` with a
# *stable* sort, so a z_index is the only way to state a layering rule that
# holds across group boundaries. Sibling reordering cannot: an edge living
# inside a `chain` VGroup will always draw over a node that sits in a different
# top-level group, however carefully the two groups sort their own children.
# That is exactly the bug that put connectors on top of the code node for 23
# seconds in section 1.
#
# Lower draws earlier, i.e. further back.
Z_BACKDROP = -20   # zone bands, grids, anything content sits on top of
Z_EDGE = -10       # connectors: never in front of what they join
Z_NODE = 0         # shapes, cards, labels — the default
Z_SLATE = 50       # the review identifier, above everything


def _word_metrics(t: Text, source: str) -> tuple[float, float]:
    """
    (smallest gap between words, median gap between letters) — in scene units.

    Counting glyphs to find the word boundaries is the obvious approach and it is
    wrong: Pango ligates some pairs, so "verification" renders as eleven glyphs
    for twelve characters and every boundary after it is off by one. That made
    the check measure the gap between two letters and report the phrase as
    merged when it was fine.

    So don't rely on the mapping. There are exactly as many word gaps as there
    are spaces, and a word gap is normally wider than a letter gap — so take the
    N widest gaps as the word gaps. The estimate can only be too generous, which
    makes the check conservative: it under-reports rather than inventing faults.
    """
    import numpy as _np
    glyphs = [g for g in t.submobjects if len(g.get_all_points())]
    n_spaces = source.count(" ")
    if len(glyphs) < 2 or n_spaces == 0:
        return (99.0, 0.0)
    gaps = sorted(
        (glyphs[i + 1].get_left()[0] - glyphs[i].get_right()[0]
         for i in range(len(glyphs) - 1)), reverse=True)
    n = min(n_spaces, len(gaps))
    return (float(gaps[n - 1]), float(_np.median(gaps[n:])) if len(gaps) > n else 0.0)


def _stamp(t: Text, source: str | None = None) -> Text:
    """
    Remember how big this text was built, and how big its geometry was then.

    Manim computes ``Text.font_size`` from the mobject's height, which a 3D
    scene's upright rotation drives to zero. The pair recorded here lets QA
    recover the rendered size from the point cloud instead, which rotation
    cannot disturb and scaling still moves.
    """
    import numpy as _np
    pts = t.get_all_points()
    t.qa_pt0 = float(t.font_size)
    t.qa_diag0 = (float(_np.linalg.norm(pts.max(axis=0) - pts.min(axis=0)))
                  if len(pts) else 0.0)
    t.qa_word_gap0, t.qa_letter_gap0 = _word_metrics(t, source if source is not None else "")
    return t


def title_text(text: str) -> Text:
    return _stamp(Text(text, color=WHITE, font_size=TYPE["title"], weight=BOLD), text)


def caption_text(text: str, color: str = WHITE) -> Text:
    return _stamp(Text(text, color=color, font_size=TYPE["caption"], weight=MEDIUM), text)


def label_text(text: str, color: str = WHITE, size: str = "label") -> Text:
    return _stamp(Text(text, color=color, font_size=TYPE[size]), text)


def mono_text(text: str, color: str = WHITE, size: str = "field") -> Text:
    return _stamp(Text(text, font=MONO, color=color, font_size=TYPE[size]), text)


# ----------------------------------------------------------------- shapes ---
def _base_shape(kind: str, color: str, size: float) -> VMobject:
    shape_name = NODE_KINDS.get(kind, {}).get("shape", "record")
    if shape_name == "hexagon":
        shape = RegularPolygon(n=6, radius=size / 2, color=color)
    elif shape_name == "square":
        shape = Square(side_length=size, color=color)
    elif shape_name == "dashed_square":
        # A clone has the product's outline and none of its body: no fill, and a
        # dashed stroke. Returned early so the panel fill below never lands on it.
        return DashedVMobject(Square(side_length=size, color=color).set_stroke(color, width=2.6),
                              num_dashes=24)
    elif shape_name == "circle":
        shape = Circle(radius=size / 2, color=color)
    elif shape_name == "diamond":
        shape = Square(side_length=size * 0.8, color=color).rotate(PI / 4)
    elif shape_name == "document":
        shape = RoundedRectangle(corner_radius=0.05, width=size * 0.86, height=size * 1.1, color=color)
    else:
        shape = RoundedRectangle(corner_radius=0.07, width=size * 1.3, height=size * 0.8, color=color)
    # Filled in its own colour at 0.18 over an opaque panel: outlines alone on a
    # dark ground read as confetti (video 2, HANDOFF.md section 4).
    shape.set_fill(interpolate_color(ManimColor(PANEL), ManimColor(color), 0.18), opacity=0.96)
    shape.set_stroke(color, width=2.6)
    return shape


def node(kind: str, text: str = "", size: float = 1.0, color: str | None = None,
         font_size: int | None = None) -> VGroup:
    """
    An artifact node. Returns VGroup(aura, shape, label) — always that order, so
    highlight helpers can stroke the shape without mangling the label.

    The label is auto-fitted inside the shape; a label that cannot fit at the
    minimum legible size raises, rather than silently overflowing.
    """
    if kind not in NODE_KINDS:
        # A misspelt or foreign kind used to fall back to a white record without a
        # word, which is how the selftest's video-2 kinds silently stopped one check.
        raise ValueError(f"node kind {kind!r} is not in this video's grammar: {sorted(NODE_KINDS)}")
    color = color or NODE_KINDS[kind]["color"]
    shape = _base_shape(kind, color, size)
    aura = shape.copy().set_stroke(color, width=9, opacity=0.12).set_fill(opacity=0)
    group = VGroup(aura, shape)
    group.qa_role = "node"
    group.qa_kind = kind
    if text:
        fs = font_size or TYPE["node"]
        label = _stamp(Text(text, color=WHITE, font_size=fs, weight=MEDIUM), text)
        inner = shape.width * 0.78
        if label.width > inner:
            scale = inner / label.width
            if fs * scale < MIN_FONT_SIZE:
                raise ValueError(
                    f"node({kind!r}, {text!r}) cannot fit its label at >= "
                    f"{MIN_FONT_SIZE}pt inside size={size}. Shorten the label or grow the node."
                )
            label.scale(scale)
        label.move_to(shape)
        label.qa_role = "label"
        group.qa_label = label
        group.add(label)
    return group


def highlight(n: Mobject, color: str = GOLD):
    """
    Animations that light a mobject without touching any text inside it.

    Nodes made by `node()` are VGroup(aura, shape, label) and get the aura
    treatment; anything else — a plain rectangle, a packet outline — just gets a
    heavier stroke. Assuming the node shape and indexing blindly turned every
    highlight on a plain shape into a render-time crash.
    """
    if getattr(n, "qa_role", None) == "node" and len(n.submobjects) >= 2:
        return [
            n[0].animate.set_stroke(color, width=13, opacity=0.6),
            n[1].animate.set_stroke(color, width=4),
        ]
    # Never stroke text. `set_stroke` on a group reaches the glyphs too, and a
    # 5-wide stroke on a letterform closes up its counters — the text goes bold,
    # muddy and harder to read, which is the opposite of highlighting it.
    targets = [s for s in n.get_family()
               if not _is_text_like(s) and len(getattr(s, "points", []))]
    if not targets:
        return [n.animate.set_color(color)]
    return [s.animate.set_stroke(color, width=5) for s in targets]


def _is_text_like(mob: Mobject) -> bool:
    if getattr(mob, "text", None) is not None:
        return True
    parent_text = getattr(mob, "qa_role", None) == "label"
    return parent_text or type(mob).__name__.startswith("VMobjectFromSVGPath")


def glow_arrow(start, end, color: str = CYAN, width: float = 3.4, buff: float = 0.16,
               tip: float | None = None) -> VGroup:
    # Manim thins a short arrow's stroke to a share of its length; no cap, so one width draws at one weight
    # (the quality pass of 2026-11-20 found 05 b09's two arrows at different weights). It shrinks the head the same
    # way: `tip` fixes the head's length too, for arrows side by side (05 b09, quality pass 2, 2026-11-21).
    heads = dict(tip_length=tip, max_tip_length_to_length_ratio=1000) if tip else {}
    aura = Arrow(start, end, color=color, stroke_width=width * 2.6, buff=buff,
                 max_stroke_width_to_length_ratio=1000, **heads).set_opacity(0.16)
    core = Arrow(start, end, color=color, stroke_width=width, buff=buff, max_stroke_width_to_length_ratio=1000,
                 **heads)
    group = VGroup(aura, core)
    # Tag only the stroke that actually has points. The wrapping VGroup has none,
    # and asking it for an endpoint raises.
    core.qa_role = "edge"
    group.qa_layer = "edge"      # the stage sends these to the back on show
    # Belt and braces: the back-seating below is a scene-order fix, this is a
    # renderer-order fix, and only the second one survives being re-parented
    # into somebody else's VGroup.
    group.set_z_index(Z_EDGE, family=True)
    return group


def connect(a: Mobject, b: Mobject, color: str = CYAN, width: float = 3.4) -> VGroup:
    """
    Arrow between two mobjects, anchored on the line between their centres so the
    head always lands on the boundary it is pointing at — never inside the label.
    """
    start = a.get_center()
    end = b.get_center()
    direction = end - start
    norm = np.linalg.norm(direction)
    if norm < 1e-6:
        raise ValueError("connect() needs two mobjects at different positions")
    unit = direction / norm
    return glow_arrow(
        a.get_boundary_point(unit) + unit * 0.06,
        b.get_boundary_point(-unit) - unit * 0.06,
        color=color, width=width, buff=0.0,
    )


def text_rows(*mobs: Mobject, buff: float | None = None, align=LEFT) -> VGroup:
    """
    Stack label rows with a gap the crowding check will accept.

    Writing `arrange(DOWN, buff=MIN_TEXT_GAP)` looks exactly right and fails:
    the rows land at precisely the threshold, and the gate reads the same
    distance back as 0.15999. Rows built through here clear the bar instead of
    balancing on it.
    """
    if buff is None:
        buff = MIN_TEXT_GAP + PLACEMENT_MARGIN
    return VGroup(*mobs).arrange(DOWN, buff=buff, aligned_edge=align)


def cursor_for(mob: Mobject, color: str = GOLD, width: float = 4.0,
               pad: float = 0.22) -> Circle:
    """
    A ring that actually goes round the thing it marks.

    A fixed-radius circle marks a one-word node and cuts straight through a
    longer one — "traversal" spent fifteen seconds with a gold line through the
    middle of it. Size the ring from the node, not from a constant.
    """
    r = max(mob.width, mob.height) / 2 + pad
    ring = Circle(radius=r, color=color, stroke_width=width)
    ring.move_to(mob.get_center())
    return ring


def allow_overlap(mob: Mobject, *others: Mobject, reason: str = ""):
    """
    Declare that `mob` is *meant* to sit over `others`.

    A stamp landing across a quote is a deliberate composition, not a layout bug.
    Declaring it keeps the overlap checker strict everywhere else instead of
    forcing the tolerance up globally, which is how these checks stop working.
    """
    def texts(m):
        return [str(getattr(s, "text", "")) for s in m.get_family()
                if getattr(s, "text", None)]

    mine = texts(mob)
    theirs = [t for o in others for t in texts(o)]
    for sub in mob.get_family():
        if getattr(sub, "text", None):
            sub.qa_allow_overlap = theirs
            sub.qa_allow_reason = reason
    for o in others:
        for sub in o.get_family():
            if getattr(sub, "text", None):
                sub.qa_allow_overlap = mine
                sub.qa_allow_reason = reason
    return mob


def strip_labels(*nodes: Mobject) -> None:
    """
    Remove the text from nodes, immediately and permanently.

    Deliberately not an animation. Two reasons, both learned the hard way:

    * `FadeOut` on a label is a no-op that then *restores* the opacity, because
      the label is a submobject the scene does not hold directly.
    * Returning `.animate` chains puts two animations on one family; the group's
      own `.animate.scale(...)` captured its target before the opacity changed,
      so it faithfully restored every label it was supposed to remove.

    Call this immediately before the play that moves or scales the node, so the
    text goes as the shape transforms. A label evaporating off a shape that then
    sits still reads as a rendering glitch — and the QA gate will say so.
    """
    for node in nodes:
        for sub in node.get_family():
            if getattr(sub, "text", None):
                sub.set_opacity(0)


def restroke(mob: Mobject, color: str, width: float = 3.0):
    """
    Change a mobject's stroke without touching any text inside it.

    `mob.animate.set_stroke(...)` reaches every submobject, so calling it on a
    node group strokes the label as well and thickens the letterforms until they
    are hard to read. Use this anywhere a group might contain text.
    """
    targets = [s for s in mob.get_family()
               if not _is_text_like(s) and len(getattr(s, "points", []))]
    if not targets:
        return [mob.animate.set_color(color)]
    return [s.animate.set_stroke(color, width=width) for s in targets]


# ------------------------------------------------------------ this video ---
def claim_footer(kind: str, source: str = "") -> VGroup:
    """
    A dot in the claim kind's colour, then one line: the kind word in that
    colour, a middle dot, the short source name in grey.

    One Text, not a chip plus a label: the caption lane holds one thing at a
    time (the gate's caption_stack). No pill round the word: any outline round
    part of a Text runs through the Text's box (outline_over_text). Set at the
    caption size: at 17 and 22 the word gaps of a source name merged.
    """
    color = CLAIM_KINDS[kind]
    word = "Levi's view" if kind == "levi" else kind
    # Single spaces only: the gate finds word gaps by counting spaces.
    text = f"{word} · {source}" if source else word
    line = _stamp(Text(text, color=MUTED, font_size=TYPE["caption"]), text)
    VGroup(*line[:len(word.replace(" ", ""))]).set_color(color if kind in ("measured", "guess") else WHITE)
    dot = RoundedRectangle(corner_radius=0.06, width=0.24, height=0.24)
    dot.set_fill(color, opacity=1.0).set_stroke(width=0)
    return VGroup(dot, line).arrange(RIGHT, buff=0.22)


def tile(width: float, height: float, color: str, opacity: float = 0.18) -> Rectangle:
    """A bar or panel filled in its own colour, never a bare outline."""
    r = Rectangle(width=width, height=height, color=color)
    r.set_fill(color, opacity=opacity).set_stroke(color, width=2.2)
    return r


def strike(mob: Mobject, color: str = RED, width: float = 5.0) -> Line:
    """A red line through a claim that did not survive. The shape stays what it was."""
    line = Line(mob.get_corner(DL) + LEFT * 0.08, mob.get_corner(UR) + RIGHT * 0.08,
                color=color, stroke_width=width)
    return line


# ------------------------------------------------------------- episode 004 ---
def baseline(t: Text) -> float:
    """Where a line of text sits: the median of its glyphs' bottoms, which descenders (p, g, y) do not move."""
    import numpy as _np
    return float(_np.median([g.get_bottom()[1] for g in t.submobjects if len(g.get_all_points())]))


def sit(t: Text, y: float) -> Text:
    """Move a text up or down so its baseline is at y."""
    return t.shift(UP * (y - baseline(t)))


def card(width: float, height: float, color: str = MUTED, radius: float = 0.1, dashed: bool = False) -> VMobject:
    """A page, step or panel filled in its own colour over the panel, never a bare outline; dashed, unfilled, when
    it is a gap or an illustration, not a thing."""
    box = RoundedRectangle(corner_radius=radius, width=width, height=height, color=color)
    if dashed:
        return DashedVMobject(box.set_stroke(color, width=2.2), num_dashes=44)
    box.set_fill(interpolate_color(ManimColor(PANEL), ManimColor(color), 0.14), opacity=0.96)
    return box.set_stroke(color, width=2.2)


def band(width: float, height: float) -> RoundedRectangle:
    """A table's row behind its marks: faint, on the backdrop, so an empty table reads as one to fill."""
    row = RoundedRectangle(corner_radius=0.08, width=width, height=height, color=GRID)
    return row.set_fill(PANEL_HI, opacity=0.9).set_stroke(GRID, width=1.4).set_z_index(Z_BACKDROP)


def boxed(words: Mobject, color: str = MUTED, pad: tuple[float, float] = (0.5, 0.36)) -> VGroup:
    """Words centred on a card in their colour. VGroup(card, words)."""
    box = card(words.width + pad[0], words.height + pad[1], color)
    return VGroup(box, words.move_to(box))


def tick(color: str = WHITE, scale: float = 1.0, width: float = 5.0) -> VMobject:
    """A check mark: a step that worked, a source that measured it."""
    return VMobject(color=color, stroke_width=width).set_points_as_corners(
        [LEFT * 0.16 + UP * 0.02, DOWN * 0.13 + LEFT * 0.03, RIGHT * 0.19 + UP * 0.18]).scale(scale)


def page(body: Mobject, pad: tuple[float, float] = (0.5, 0.5)) -> VMobject:
    """A card framing `body`, centred on it, `pad` wider and taller than it."""
    return card(body.width + pad[0], body.height + pad[1]).move_to(body)


def person_page(name: str, via: str, when: str, words: Mobject) -> VGroup:
    """A person's message on a page, their circle, the channel and the time in its header. VGroup(page, head, words)."""
    head = VGroup(person(name, size=0.75), label_text(via), mono_text(when, color=MUTED)).arrange(RIGHT, buff=0.35)
    sit(head[2], baseline(head[1]))
    return VGroup(page(text_rows(head, words, buff=0.35), (0.8, 0.6)), head, words)


def underline(mob: Mobject, color: str = WHITE, width: float = 3.0, gap: float = 0.1) -> Line:
    """A line `gap` under some words: the phrase a beat is about (gold when it names the PIN route)."""
    return Line(mob.get_corner(DL) + DOWN * gap, mob.get_corner(DR) + DOWN * gap, color=color, stroke_width=width)


def end_mark(color: str, size: float = 0.26) -> RoundedRectangle:
    """A dumbbell's end: a small filled square (a dot would read as a run)."""
    sq = RoundedRectangle(corner_radius=0.04, width=size, height=size, color=color)
    return sq.set_fill(color, opacity=0.95).set_stroke(color, width=1.5)


def magnifier(radius: float = 0.14, handle: float = 0.12, handle_width: float = 3.0) -> VGroup:
    """A search: a white ring and its handle. VGroup(ring, handle)."""
    ring = Circle(radius=radius, color=WHITE, stroke_width=3)
    start = ring.point_at_angle(-PI / 4)
    return VGroup(ring, Line(start, start + DR * handle, color=WHITE, stroke_width=handle_width))


def ignore(mob: Mobject) -> Mobject:
    """A ghost in passing (a copy flying into a card): not part of the composition the gate judges."""
    for sub in mob.get_family():
        sub.qa_ignore = True
    return mob


def skill_card(name: str = "SKILL.md", width: float = 1.3, height: float = 1.7, route: bool = False,
               color: str = WHITE, rules: int = 5) -> VGroup:
    """A skill file: a portrait card, its name in monospace above ruled lines; with `route`, one rule is the gold
    PIN route. VGroup(card, lines, name); the gold line, if any, is lines[route_index] and also .route."""
    body = RoundedRectangle(corner_radius=0.08, width=width, height=height, color=color)
    body.set_fill(PANEL_HI, opacity=0.96).set_stroke(color, width=2.4)
    word = mono_text(name, color=color, size="tiny")
    if word.width > width * 0.86:
        word.scale_to_fit_width(width * 0.86)
    word.next_to(body.get_top(), DOWN, buff=0.14)
    top = word.get_bottom()[1] - 0.12
    rules = max(1, min(rules, int((top - body.get_bottom()[1]) / 0.2)))
    gap = (top - body.get_bottom()[1]) / (rules + 1)
    lines = VGroup()
    pick = rules // 2 if route else -1
    for i in range(rules):
        long = 0.32 if i % 3 else 0.14
        line = Line(LEFT * width * 0.32, RIGHT * width * long, stroke_width=4 if i == pick else 2,
                    color=FACT if i == pick else MUTED, stroke_opacity=1 if i == pick else 0.55)
        line.move_to([body.get_center()[0], top - gap * (i + 1), 0]).align_to(body.get_left() + RIGHT * width * 0.16, LEFT)
        lines.add(line)
    group = VGroup(body, lines, word)
    group.route = lines[pick] if route else None
    return group


def route_line(length: float = 0.8) -> Line:
    """The PIN route on its own (moving between cards, or in a brief): a short gold line."""
    return Line(LEFT * length / 2, RIGHT * length / 2, color=FACT, stroke_width=4)


def alpha(size: float = 0.9, name: str = "Alpha") -> VGroup:
    """Alpha, the agent and its chat model: a white hexagon with its name inside."""
    return node("model", name, size=size)


def person(name: str = "Levi", size: float = 0.8) -> VGroup:
    """A person: a white circle with the name inside."""
    return node("person", name, size=size)


def worker(size: float = 0.7, name: str = "worker") -> VGroup:
    """A worker Alpha hands a job to: a white square, its word below. VGroup(square, word)."""
    sq = Square(side_length=size, color=WHITE).set_stroke(WHITE, width=2.4).set_fill(PANEL_HI, opacity=0.96)
    word = label_text(name, size="tiny")
    word.next_to(sq, DOWN, buff=0.14)
    return VGroup(sq, word)


def brief_card(route: bool, width: float = 0.9, height: float = 0.6) -> VGroup:
    """A worker's brief: a small card; a gold line when it carries the route, grey lines when it does not."""
    body = card(width, height, MUTED, radius=0.06)
    lines = VGroup(*[Line(LEFT * width * 0.3, RIGHT * width * 0.3, stroke_width=3 if (route and i == 1) else 2,
                          color=FACT if (route and i == 1) else MUTED) for i in range(3)])
    lines.arrange(DOWN, buff=0.1).move_to(body)
    return VGroup(body, lines)


def door(height: float = 2.4, width: float = 1.3, label: bool = True) -> VGroup:
    """The runtime: a blue door, two posts and a lintel round an opening. VGroup(left, right, lintel[, word]);
    .opening is the opening's centre line (a Line from bottom to top) for a budget rule or a read to cross."""
    post = lambda: RoundedRectangle(corner_radius=0.04, width=0.16, height=height, color=RUNTIME) \
        .set_fill(RUNTIME, opacity=0.85).set_stroke(RUNTIME, width=2.0)
    left, right = post().shift(LEFT * width / 2), post().shift(RIGHT * width / 2)
    lintel = RoundedRectangle(corner_radius=0.04, width=width + 0.16, height=0.16, color=RUNTIME) \
        .set_fill(RUNTIME, opacity=0.85).set_stroke(RUNTIME, width=2.0).move_to(UP * (height / 2))
    group = VGroup(left, right, lintel)
    if label:
        word = label_text("runtime", color=RUNTIME, size="tiny")
        word.next_to(lintel, UP, buff=0.14)
        group.add(word)
    group.opening = Line(DOWN * height / 2, UP * (height / 2 - 0.1))
    return group


def budget_rule(width: float = 1.1, text: str = "16,000") -> VGroup:
    """The budget: a cyan rule with its size in characters beside it. VGroup(rule, word)."""
    rule = Line(LEFT * width / 2, RIGHT * width / 2, color=BUDGET, stroke_width=5)
    word = mono_text(text, color=BUDGET, size="tiny")
    word.next_to(rule, RIGHT, buff=0.14)
    return VGroup(rule, word)


def stop_bar(height: float = 0.7) -> RoundedRectangle:
    """Where a refused read stops: a short red bar across its path, at the door."""
    return RoundedRectangle(corner_radius=0.04, width=0.14, height=height, color=REFUSED) \
        .set_fill(REFUSED, opacity=0.9).set_stroke(REFUSED, width=2.0)


def read_path(start, end, served: bool, stop_at=None, width: float = 4.0) -> VGroup:
    """A read: from a skill to Alpha. Served: a green arrow from start to end. Refused: a red line from start to
    `stop_at` (the door), ending on a stop bar. VGroup(path[, bar])."""
    if served:
        return VGroup(Arrow(start, end, buff=0.12, color=SERVED, stroke_width=width,
                            max_tip_length_to_length_ratio=0.12).set_z_index(Z_EDGE))
    stop_at = end if stop_at is None else stop_at
    path = Line(start, stop_at, color=REFUSED, stroke_width=width).set_z_index(Z_EDGE)
    bar = stop_bar().move_to(stop_at)
    return VGroup(path, bar)


def index_list(names, lit: str | None = None, size: str = "tiny") -> VGroup:
    """The index in Alpha's prompt: one short monospace line per skill, grey; the `lit` one white with a gold mark
    beside it when it points at the route. VGroup of lines."""
    rows = VGroup(*[mono_text(f"- {n}", color=WHITE if n == lit else MUTED, size=size) for n in names])
    rows.arrange(DOWN, buff=0.14, aligned_edge=LEFT)
    return rows


def plate(text: str, color: str = MUTED) -> VGroup:
    """A setting from Alpha's configuration: a grey plate with its value in monospace. VGroup(card, words)."""
    return boxed(mono_text(text, color=WHITE, size="field"), color=color, pad=(0.5, 0.34))


def paper(name: str, width: float = 1.5, height: float = 1.9) -> VGroup:
    """A published source: a violet page card, its short name above ruled lines. VGroup(card, lines, name)."""
    body = RoundedRectangle(corner_radius=0.08, width=width, height=height, color=SOURCE)
    body.set_fill(interpolate_color(ManimColor(PANEL), ManimColor(SOURCE), 0.18), opacity=0.96)
    body.set_stroke(SOURCE, width=2.4)
    word = label_text(name, color=SOURCE, size="tiny")
    if word.width > width * 0.86:
        word.scale_to_fit_width(width * 0.86)
    word.next_to(body.get_top(), DOWN, buff=0.16)
    top = word.get_bottom()[1] - 0.16
    gap = (top - body.get_bottom()[1]) / 5
    lines = VGroup(*[Line(LEFT * width * 0.3, RIGHT * width * (0.3 if i % 3 else 0.1), color=SOURCE,
                          stroke_width=2, stroke_opacity=0.55)
                     .move_to([body.get_center()[0], top - gap * (i + 1), 0]) for i in range(4)])
    return VGroup(body, lines, word)


def run_dot(ok: bool, radius: float = 0.09) -> Dot:
    """One run of the test: green when the knowledge got through, red when it did not."""
    return Dot(radius=radius, color=SERVED if ok else REFUSED)


def run_grid(ok: int, bad: int, cols: int = 12, radius: float = 0.09, gap: float = 0.08) -> VGroup:
    """Runs as a block of dots you can count, green first then red, `cols` to a row, filled row by row."""
    dots = VGroup(*[run_dot(i < ok, radius) for i in range(ok + bad)])
    dots.arrange_in_grid(cols=cols, buff=gap, flow_order="rd")
    return dots


def model_mark(name: str) -> VGroup:
    """A model as a small white hexagon with its short name beside it, for rows and keys too tight for node()."""
    hexagon = RegularPolygon(n=6, radius=0.17, color=WHITE).set_stroke(WHITE, width=2.4)
    hexagon.set_fill(PANEL_HI, opacity=0.96)
    return VGroup(hexagon, label_text(name)).arrange(RIGHT, buff=0.16)


SPINE = (
    "Where did the knowledge go?",
    "How often does this happen?",
    "What would fix it?",
)


def spine(lit: int | None = None, answers: dict[int, str] | None = None, width: float = 10.0,
          rows_shown: int = 3) -> VGroup:
    """The episode's scorecard: one row per question in SPINE (0-based; the first `rows_shown`), its answer, if
    given, at the right; the row `lit` in white and the rest grey, or all white with none lit. VGroup of rows, each
    VGroup(number, question, answer slot), so a beat can light or fill one row."""
    answers = answers or {}
    rows = VGroup()
    for i, question in enumerate(SPINE[:rows_shown]):
        on = lit is None or lit == i
        color = WHITE if on else MUTED
        number = mono_text(f"{i + 1}", color=color, size="label")
        q = label_text(question, color=color)
        if i in answers:
            slot = label_text(answers[i], color=color)
        else:
            slot = DashedVMobject(RoundedRectangle(corner_radius=0.06, width=2.6, height=0.42, color=color)
                                  .set_stroke(color, width=1.6), num_dashes=22)
        row = VGroup(number, q, slot)
        number.move_to(LEFT * width / 2, aligned_edge=LEFT)
        sit(q.next_to(number, RIGHT, buff=0.4), baseline(number))
        slot.move_to(RIGHT * width / 2, aligned_edge=RIGHT)
        rows.add(row)
    rows.arrange(DOWN, buff=0.34, aligned_edge=LEFT)
    return rows
