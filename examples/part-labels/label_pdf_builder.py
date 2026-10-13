"""Lay a build report out into a PDF and render it. Nothing here talks to PreForm.

Each build gets a summary page for billing, then its bag labels for the sorters.
"""

from dataclasses import dataclass
from itertools import groupby
from pathlib import Path

import pymupdf

# Page Formatting
INCH = 72.0
PAGE_W, PAGE_H = 8.5, 11.0
LABEL_W, LABEL_H = 4.0, 3.333
COLS, ROWS = 2, 3
MARGIN_X, MARGIN_Y = 0.16, 0.5
PICTURE_SHARE = 0.47  # how much of the label's width the picture takes
PER_PAGE = COLS * ROWS

ORDER_PT, PART_PT, QTY_PT, FOOTER_PT = 20.0, 15.0, 15.0, 11.0
LINE = 1.35  # height of one printed line, as a multiple of the type size
HEADROOM = 0.4  # extra room insert_textbox needs above the first line of a box
PART_LINES = 1  # lines allowed for the part name; raise to 2 to let long names wrap
GAP_PT = 10.0  # blank space between the quantity and the footer
REGULAR, BOLD = "helv", "hebo"

# Summary page: a table of every part, grouped by order, with the material it used.
SUMMARY_MARGIN = 0.6  # inches, on every side
TITLE_PT, FACT_PT, TABLE_PT = 22.0, 11.0, 9.0
ROW_PT = 16.0  # height of one table row
# (heading, width in points, alignment): 0 is left, 2 is right. The widths fill the text column.
COLUMNS = [("Order", 68, 0), ("Customer", 108, 0), ("Part", 150, 0), ("Qty", 30, 2),
           ("Part mL", 55, 2), ("Supports mL", 65, 2), ("Total mL", 50, 2)]


@dataclass
class Label:
    """Everything printed on a single bag label, and its row in the summary."""

    order: str
    customer: str
    part: str
    quantity: int
    model_ml: float  # the parts alone
    material_ml: float  # the parts with their supports and share of the raft
    image: Path


@dataclass
class Build:
    """One build volume: what it was printed in, and a label for every distinct part."""

    name: str
    material: str
    layer_thickness_mm: float
    material_ml: float
    date: str
    labels: list[Label]


def label_rect(index: int) -> pymupdf.Rect:
    """The box for the index'th label on a page, spread evenly inside the margins."""
    col, row = index % COLS, index // COLS
    gap_x = (PAGE_W - 2 * MARGIN_X - COLS * LABEL_W) / max(COLS - 1, 1)
    gap_y = (PAGE_H - 2 * MARGIN_Y - ROWS * LABEL_H) / max(ROWS - 1, 1)
    x = MARGIN_X + col * (LABEL_W + gap_x)
    y = MARGIN_Y + row * (LABEL_H + gap_y)
    return pymupdf.Rect(x * INCH, y * INCH, (x + LABEL_W) * INCH, (y + LABEL_H) * INCH)


def fit_text(
    page: pymupdf.Page, box: pymupdf.Rect, text: str, size: float, font: str, min_size: float = 6.0, align: int = 0
) -> float:
    """Draw text at the largest size up to `size` that fits box, and return the height it used.

    insert_textbox wraps on the box's width by itself, so text only shrinks once it needs more
    lines than the box has room for. It draws nothing and returns a negative number when the
    text does not fit; otherwise it returns the height left over.

    Raises ValueError if the text will not fit even at min_size. A label that silently lost its
    part name would still look like a valid label on the bag.
    """
    while True:
        leftover = page.insert_textbox(box, text, fontsize=size, fontname=font, align=align)
        if leftover >= 0:
            return box.height - leftover
        if size <= min_size:
            raise ValueError(f"{text!r} does not fit its label, even at {min_size}pt")
        size -= 0.5


def draw_label(
    page: pymupdf.Page, box: pymupdf.Rect, label: Label, build: Build
) -> None:
    """Picture on the left; order, customer, part, quantity, and footer on the right."""
    pad = 0.08 * INCH
    inner = pymupdf.Rect(box.x0 + pad, box.y0 + pad, box.x1 - pad, box.y1 - pad)
    split = inner.x0 + inner.width * PICTURE_SHARE
    page.insert_image(
        pymupdf.Rect(inner.x0, inner.y0, split - pad, inner.y1),
        filename=str(label.image),
        keep_proportion=True,
    )

    footer = [f"{label.material_ml:.1f} mL {build.material}", build.date]
    # Centre the text block against the picture, then fill it in from the top down.
    text_pt = ORDER_PT + FOOTER_PT + PART_PT * PART_LINES + QTY_PT
    block = (text_pt + len(footer) * FOOTER_PT) * LINE + GAP_PT
    y = inner.y0 + max(0.0, (inner.height - block) / 2)

    def draw_row(y: float, text: str, size: float, font: str, lines: int = 1) -> float:
        """Draw one row of text at y, and return the y the next row starts at."""
        box = pymupdf.Rect(split, y, inner.x1, y + size * (LINE * lines + HEADROOM))
        return y + fit_text(page, box, text, size, font)

    # The order number leads: it is what a sorter matches the bag to.
    y = draw_row(y, label.order, ORDER_PT, BOLD)
    y = draw_row(y, label.customer, FOOTER_PT, REGULAR)
    y = draw_row(y, label.part, PART_PT, REGULAR, lines=PART_LINES)
    y = draw_row(y, f"Qty: {label.quantity}", QTY_PT, BOLD) + GAP_PT
    for entry in footer:
        y = draw_row(y, entry, FOOTER_PT, REGULAR)


def draw_summary(doc: pymupdf.Document, build: Build) -> None:
    """One or more pages listing every part by order, with subtotals billing can charge."""
    left, top = SUMMARY_MARGIN * INCH, SUMMARY_MARGIN * INCH
    bottom = (PAGE_H - SUMMARY_MARGIN) * INCH

    def new_page() -> tuple[pymupdf.Page, float]:
        page = doc.new_page(width=PAGE_W * INCH, height=PAGE_H * INCH)
        return page, top

    def row(page: pymupdf.Page, y: float, cells: list[str], font: str = REGULAR) -> float:
        x = left
        for text, (_heading, width, align) in zip(cells, COLUMNS):
            box = pymupdf.Rect(x, y, x + width - 4, y + TABLE_PT * (LINE + HEADROOM))
            fit_text(page, box, text, TABLE_PT, font, align=align)
            x += width
        return y + ROW_PT

    def rule(page: pymupdf.Page, y: float) -> None:
        page.draw_line((left, y - 3), (left + sum(width for _, width, _ in COLUMNS), y - 3), width=0.5)

    page, y = new_page()
    page.insert_text((left, y + TITLE_PT), "Build report", fontsize=TITLE_PT, fontname=BOLD)
    y += TITLE_PT * LINE + 6
    supports_ml = build.material_ml - sum(label.model_ml for label in build.labels)
    for fact in [
        build.name,
        f"{build.material}, {build.layer_thickness_mm} mm layers, {build.date}",
        f"Material used: {build.material_ml:.1f} mL, of which {supports_ml:.1f} mL is supports and raft",
    ]:
        page.insert_text((left, y + FACT_PT), fact, fontsize=FACT_PT, fontname=REGULAR)
        y += FACT_PT * LINE
    y += 14

    header = [heading for heading, _, _ in COLUMNS]
    y = row(page, y, header, BOLD)
    for order, group in groupby(build.labels, key=lambda label: label.order):
        labels = list(group)
        if y + ROW_PT * (len(labels) + 2) > bottom:  # keep an order and its subtotal on one page
            page, y = new_page()
            y = row(page, y, header, BOLD)
        rule(page, y)
        for label in labels:
            y = row(page, y, [
                label.order, label.customer, label.part, str(label.quantity),
                f"{label.model_ml:.2f}", f"{label.material_ml - label.model_ml:.2f}", f"{label.material_ml:.2f}",
            ])
        subtotal = sum(label.material_ml for label in labels)
        y = row(page, y, [f"{order} total", "", "", "", "", "", f"{subtotal:.2f}"], BOLD)
    rule(page, y)
    row(page, y, ["Build total", "", "", "", "", "", f"{build.material_ml:.2f}"], BOLD)


def render_pdf(builds: list[Build], out: Path) -> None:
    """Write each build's summary and then its labels, PER_PAGE labels to a page, to a PDF at out."""
    if not any(build.labels for build in builds):
        raise ValueError("no labels to render")
    doc = pymupdf.open()
    for build in builds:
        draw_summary(doc, build)
        for index, label in enumerate(build.labels):
            if index % PER_PAGE == 0:
                page = doc.new_page(width=PAGE_W * INCH, height=PAGE_H * INCH)
            draw_label(page, label_rect(index % PER_PAGE), label, build)
    doc.save(str(out))
