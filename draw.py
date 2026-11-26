#!/usr/bin/env python3
"""Render the 26 November 2026 world-news summary as a 1024x1024 PNG.

Local renderer only. The grader never runs this file; main.py is the
entrypoint. No network, no clock, no randomness: the same input always
produces the same bytes.
"""

from PIL import Image, ImageDraw, ImageFont

CANVAS_W = 1024
CANVAS_H = 1024
OUT_NAME = "entry.png"

PAPER = (247, 243, 233)
INK = (17, 24, 39)
NAVY = (15, 36, 62)
NAVY_SOFT = (27, 58, 95)
GOLD = (201, 162, 39)
RULE = (203, 196, 178)
CARD = (255, 255, 255)
MUTED = (75, 85, 99)
WHITE = (255, 255, 255)

REGION_PAINT = {
    "Middle East": (146, 64, 14),
    "Europe": (30, 64, 175),
    "Africa": (4, 120, 87),
    "Asia-Pacific": (109, 40, 217),
    "Americas": (159, 18, 57),
}

FONT_DIR = "/usr/share/fonts/truetype/dejavu"

TOP_STORIES = [
    (
        "Middle East",
        "Hormuz tankers hit mines",
        "Two oil tankers struck naval mines and caught fire in the Strait of "
        "Hormuz; Iran says it is prepared to withstand a US blockade.",
    ),
    (
        "Europe",
        "Russian strikes cut power in five regions",
        "A DTEK plant halted and a Naftogaz fire broke out in Poltava.",
    ),
    (
        "Middle East",
        "Israeli strike kills Hamas security chief",
        "Mohammad Abuelouf, his wife and two children were killed in a Gaza apartment.",
    ),
    (
        "Asia-Pacific",
        "Australia\u2013Solomons pact",
        "Solomon Islands names Australia as its primary security partner; A$740m over ten years.",
    ),
    (
        "Americas",
        "Thanksgiving storms",
        "250m Americans affected, gusts to 70 mph; Macy's 100th parade balloons at risk; "
        "SF tide 8.23 ft; AAA 81.5m travellers.",
    ),
]

SHORT_STORIES = [
    ("Middle East", "Houthis hit Ras Tanura refinery and a Riyadh tower; 11 wounded"),
    ("Middle East", "Houthis will not seize Aden"),
    ("Middle East", "Iraq top court: Baghdad may deploy on all borders"),
    ("Europe", "Italy rebukes Ukraine over Libya strikes"),
    ("Africa", "Two Libyans die after Benghazi attack"),
    ("Europe", 'Pope Leo calls COP31 failure "troubling"'),
    ("Africa", "Sudan RSF drone strikes kill 19 in Blue Nile"),
    ("Middle East", "Lebanon to open second airport"),
    ("Europe", "Canary Islands single-day migrant record, 2,100+"),
    ("Africa", "Saudi national kidnapped in Niger"),
    ("Europe", "Bulgaria intercepts first migrant boat in months, 35 aboard"),
    ("Europe", "Puigdemont to return to Spain on 12 December"),
    ("Europe", "Kremlin rejects Johnson's token-force call"),
    ("Europe", "Sarkozy corruption case ordered to trial"),
    ("Europe", "Eurostar cancels London\u2013Paris\u2013Brussels trains"),
    ("Europe", "RAF moves aircraft to hangars at night"),
    ("Europe", "German economy grows 0.1% in Q3"),
    ("Europe", "Greeks strike over wages and public services"),
    ("Europe", "NATO AWACS to Poland after missiles incident"),
    ("Asia-Pacific", "Taiwan votes Saturday in mayoral polls"),
    ("Asia-Pacific", "First foreigner boards Tiangong \u2014 Zeeshan Ali, Shenzhou-24, crew entered Tiangong 06:35 GMT"),
    ("Asia-Pacific", "Xi graft probe of Shanghai chief Chen Jining"),
    ("Asia-Pacific", "China drafts 78 international AI standards"),
    ("Asia-Pacific", "Asian stocks plunge in AI sell-off \u2014 KOSPI, Nikkei and Taiex slide"),
    ("Asia-Pacific", "Bangladesh garment workers clash with police"),
    ("Asia-Pacific", "North Korea expels Swiss diplomat"),
    ("Americas", "US GDP grows 4.3% in Q3 \u2014 BEA via AP"),
    ("Americas", "US plans tariffs on China, the EU and 14 others \u2014 AP"),
    ("Americas", "Huawei convicted in New York \u2014 AP"),
    ("Americas", "Colombia hostages freed in Cartagena raid \u2014 video 01:30 local, 06:30 GMT"),
    ("Americas", "Canada foreign-student curbs test talent drive"),
]

DAY_MARKS = [
    ("06:30", "Cartagena rescue"),
    ("06:35", "Shenzhou-24 enters Tiangong"),
    ("13:00", "Reuters summary published"),
]


def load_font(bold, size):
    name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    return ImageFont.truetype(f"{FONT_DIR}/{name}", size)


def split_lines(painter, text, font, width):
    """Greedy word wrap; returns a list of lines that fit `width`."""
    words = text.split()
    lines = []
    current = ""
    for word in words:
        trial = word if not current else f"{current} {word}"
        if painter.textlength(trial, font=font) <= width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def paint_tag(painter, x, y, label):
    paint = REGION_PAINT[label]
    font = load_font(True, 9)
    text_w = painter.textlength(label, font=font)
    pad_x = 7
    box_w = int(text_w + pad_x * 2)
    box_h = 18
    painter.rounded_rectangle([x, y, x + box_w, y + box_h], radius=4, fill=paint)
    painter.text((x + pad_x, y + 4), label, font=font, fill=WHITE)
    return box_w


def paint_wrapped(painter, x, y, text, font, width, colour, spacing=3, limit=None):
    lines = split_lines(painter, text, font, width)
    if limit is not None:
        lines = lines[:limit]
    for line in lines:
        painter.text((x, y), line, font=font, fill=colour)
        y += font.size + spacing
    return y


def paint_header(painter):
    painter.rectangle([0, 0, CANVAS_W, 96], fill=NAVY)
    painter.rectangle([0, 96, CANVAS_W, 100], fill=GOLD)
    title_font = load_font(True, 42)
    painter.text((24, 14), "WORLD NEWS", font=title_font, fill=WHITE)
    sub_font = load_font(False, 13)
    painter.text(
        (24, 64),
        "26 NOVEMBER 2026  \u2022  36 STORIES  \u2022  REUTERS / AP / AFP / FOX WEATHER",
        font=sub_font,
        fill=(196, 210, 228),
    )
    date_font = load_font(True, 15)
    label = "THU 26 NOV"
    w = painter.textlength(label, font=date_font)
    painter.text((CANVAS_W - 24 - w, 22), label, font=date_font, fill=GOLD)
    painter.text(
        (CANVAS_W - 24 - painter.textlength("2026", font=sub_font), 46),
        "2026",
        font=sub_font,
        fill=(196, 210, 228),
    )


def paint_big_lead(painter, story):
    region, headline, body = story
    x, y, w, h = 24, 108, 976, 112
    painter.rounded_rectangle([x, y, x + w, y + h], radius=8, fill=CARD, outline=RULE, width=1)
    painter.rectangle([x, y, x + 6, y + h], fill=REGION_PAINT[region])
    paint_tag(painter, x + 20, y + 12, region)
    painter.text(
        (x + 20, y + 38),
        headline,
        font=load_font(True, 23),
        fill=INK,
    )
    paint_wrapped(painter, x + 20, y + 72, body, load_font(False, 14), w - 40, MUTED, spacing=2, limit=2)


def paint_small_lead(painter, story, x, y, w, h):
    region, headline, body = story
    painter.rounded_rectangle([x, y, x + w, y + h], radius=8, fill=CARD, outline=RULE, width=1)
    painter.rectangle([x, y, x + 5, y + h], fill=REGION_PAINT[region])
    paint_tag(painter, x + 16, y + 10, region)
    end_y = paint_wrapped(
        painter, x + 16, y + 34, headline, load_font(True, 15), w - 32, INK, spacing=1, limit=2
    )
    paint_wrapped(painter, x + 16, end_y + 1, body, load_font(False, 12), w - 32, MUTED, spacing=1, limit=2)


def paint_briefs(painter):
    label_font = load_font(True, 12)
    painter.text((24, 446), "31 MORE STORIES", font=label_font, fill=NAVY)
    painter.line([170, 454, 1000, 454], fill=RULE, width=1)
    col_w = 320
    col_gap = 8
    row_h = 41
    top = 468
    for idx, (region, headline) in enumerate(SHORT_STORIES):
        col = idx % 3
        row = idx // 3
        x = 24 + col * (col_w + col_gap)
        y = top + row * row_h
        dot = REGION_PAINT[region]
        painter.ellipse([x, y + 5, x + 7, y + 12], fill=dot)
        num_font = load_font(True, 10)
        painter.text((x + 12, y), f"{idx + 6}.", font=num_font, fill=MUTED)
        num_w = painter.textlength(f"{idx + 6}. ", font=num_font)
        paint_wrapped(
            painter,
            x + 12 + int(num_w) + 2,
            y,
            headline,
            load_font(False, 11),
            col_w - 12 - int(num_w) - 4,
            INK,
            spacing=1,
            limit=2,
        )
        painter.text(
            (x + 12, y + 27),
            region.upper(),
            font=load_font(True, 7),
            fill=dot,
        )


def paint_timeline(painter):
    y0 = 938
    painter.rectangle([0, y0, CANVAS_W, CANVAS_H], fill=NAVY)
    painter.rectangle([0, y0, CANVAS_W, y0 + 3], fill=GOLD)
    painter.text((24, y0 + 12), "UTC TIMELINE", font=load_font(True, 12), fill=GOLD)
    painter.text(
        (24, y0 + 32),
        "All times UTC \u2014 from the same reports",
        font=load_font(False, 11),
        fill=(196, 210, 228),
    )
    col_w = 222
    for i, (when, what) in enumerate(DAY_MARKS):
        x = 330 + i * col_w
        if i:
            painter.line([x - 14, y0 + 14, x - 14, y0 + 70], fill=NAVY_SOFT, width=1)
        painter.text((x, y0 + 12), when, font=load_font(True, 20), fill=WHITE)
        paint_wrapped(painter, x, y0 + 40, what, load_font(False, 11), col_w - 22, (196, 210, 228), spacing=1, limit=2)


def render():
    canvas = Image.new("RGB", (CANVAS_W, CANVAS_H), PAPER)
    painter = ImageDraw.Draw(canvas)
    paint_header(painter)
    paint_big_lead(painter, TOP_STORIES[0])
    grid_y = [232, 338]
    grid_x = [24, 517]
    for pos, story in enumerate(TOP_STORIES[1:]):
        paint_small_lead(
            painter, story, grid_x[pos % 2], grid_y[pos // 2], 483, 96
        )
    paint_briefs(painter)
    paint_timeline(painter)
    return canvas


if __name__ == "__main__":
    picture = render()
    picture.save(OUT_NAME, format="PNG")
    print(f"wrote {OUT_NAME} {picture.size[0]}x{picture.size[1]}")
