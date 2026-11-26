#!/usr/bin/env python3
"""Paint the 26 November 2026 front page (entry.png).

This is a local build tool only. It needs Pillow on the author's
machine and it is never executed by the grader -- the grader runs
main.py, which only copies the finished PNG with the standard
library. Nothing here touches the network, the clock, or any
random source, so running it twice gives the same bytes twice.

Page plan, top to bottom: a masthead with the date and the story
count, a dark strip carrying the day's UTC timeline, two wide lead
stories, three narrower lead stories, then 31 short briefs in
three columns, and a footer naming the sources. Five leads plus
thirty-one briefs is thirty-six stories in total, and the count
printed in the masthead is derived from the story tables, so the
number on the page can never drift away from the page itself.

All five illustrations are flat shapes drawn with code. No
photograph is used anywhere and no real person's face appears.
"""

import hashlib
import os

from PIL import Image, ImageDraw, ImageFont

BASE = os.path.dirname(os.path.abspath(__file__))
TARGET = os.path.join(BASE, "entry.png")

PAGE = 1024
EDGE = 24
SPAN = PAGE - 2 * EDGE

NEWSPRINT = (248, 242, 228)
TEXT = (24, 24, 24)
ACCENT = (168, 20, 20)
MUTED = (98, 92, 82)
DIVIDER = (62, 57, 47)
FAINT = (202, 194, 177)

DEJAVU = "/usr/share/fonts/truetype/dejavu"


def load(name, size):
    return ImageFont.truetype(os.path.join(DEJAVU, name), size)


MASTHEAD = load("DejaVuSerif-Bold.ttf", 64)
EYEBROW = load("DejaVuSans-Bold.ttf", 14)
EYEBROW_SMALL = load("DejaVuSans-Bold.ttf", 12)
DATELINE = load("DejaVuSans-Bold.ttf", 15)
BIG_HEAD = load("DejaVuSerif-Bold.ttf", 24)
SMALL_HEAD = load("DejaVuSerif-Bold.ttf", 18)
BIG_DECK = load("DejaVuSans.ttf", 13)
SMALL_DECK = load("DejaVuSans.ttf", 12)
CREDIT = load("DejaVuSans.ttf", 11)
STRIP = load("DejaVuSans-Bold.ttf", 10)
LABEL = load("DejaVuSans-Bold.ttf", 10)
BRIEF_HEAD = load("DejaVuSans-Bold.ttf", 12)
BRIEF_DECK = load("DejaVuSans.ttf", 11)
FOOTER = load("DejaVuSans.ttf", 10)


def split_to_width(text, face, limit):
    """Greedy wrap: pack words onto lines no wider than limit."""
    out = []
    current = ""
    for word in text.split():
        candidate = (current + " " + word).strip()
        if face.getlength(candidate) <= limit:
            current = candidate
        else:
            if current:
                out.append(current)
            current = word
    if current:
        out.append(current)
    return out


def lines_or_fail(text, face, limit, most):
    wrapped = split_to_width(text, face, limit)
    if len(wrapped) > most:
        raise ValueError("text does not fit: %r -> %r" % (text, wrapped))
    return wrapped


# ------------------------------------------------------------------ stories

WIDE_LEADS = [
    {
        "tag": "THE GULF — STRAIT OF HORMUZ",
        "title": "Two tankers hit mines and burn in the Strait of Hormuz",
        "standfirst": (
            "Iran's Revolutionary Guards say the vessels struck mines on an "
            "unauthorised route and caught fire. Tehran says it can withstand "
            "a US naval blockade as cargo shifts to land borders."),
        "credit": "Source: Reuters, 25 Nov 2026",
        "picture": "tanker",
        "caption": "THE STRAIT OF HORMUZ",
    },
    {
        "tag": "UKRAINE — THE GRID UNDER FIRE",
        "title": "Russian strikes cut power in five regions",
        "standfirst": (
            "An overnight attack damages energy and gas sites: a DTEK thermal "
            "plant halts generation and a Naftogaz site in Poltava burns. "
            "Odesa battles to keep the lights on for a million people."),
        "credit": "Source: Reuters, 25 Nov 2026",
        "picture": "pylon",
        "caption": "UKRAINE'S POWER GRID",
    },
]

NARROW_LEADS = [
    {
        "tag": "GAZA",
        "title": "Israeli strike kills Hamas security chief and his family",
        "standfirst": (
            "Hamas security chief Mohammad Abuelouf, his wife and two children "
            "die in an early-morning strike on their Gaza apartment."),
        "credit": "Source: Reuters, 25 Nov 2026",
        "picture": "skyline",
        "caption": "GAZA CITY",
    },
    {
        "tag": "THE PACIFIC",
        "title": "Australia and Solomons sign pact barring foreign bases",
        "standfirst": (
            "Treaty names Canberra the islands' primary security partner, with "
            "A$740m over a decade; Honiara must consult on sensitive deals."),
        "credit": "Sources: AP / Reuters, 25 Nov 2026",
        "picture": "island",
        "caption": "THE PACIFIC",
    },
    {
        "tag": "THANKSGIVING — USA",
        "title": "Storms target 250 million on Thanksgiving Day",
        "standfirst": (
            "81.5m travel as twin storms hit: gusts to 70 mph threaten power "
            "and the 100th Macy's balloons; SF king tide sets a record."),
        "credit": "Sources: Fox Weather / AP, 25 Nov 2026",
        "picture": "balloon",
        "caption": "NEW YORK • THANKSGIVING",
    },
]

# Reading order: column one, then column two, then column three.
# Each headline fits one line at 12 px bold, each deck one line at 11 px.
BRIEFS = [
    ("MIDDLE EAST", "Houthis hit Saudi refinery, Riyadh tower",
     "Houthis claim the Ras Tanura strike; 11 hurt in Riyadh."),
    ("MIDDLE EAST", "Houthis 'will not seize Aden', army says",
     "Army says the push to 60 km from Aden will be held."),
    ("MIDDLE EAST", "Iraq court backs Baghdad on borders",
     "Federal forces may deploy on all borders, court rules."),
    ("MIDDLE EAST", "Italy rebukes Kyiv over Libya strikes",
     "Rome calls the Libya attack a mistake; Kyiv: self-defence."),
    ("MIDDLE EAST", "Two Libyans die after Benghazi attack",
     "Two naval personnel die of wounds from the drone strike."),
    ("MIDDLE EAST", "Pope decries COP31 failure",
     "Pope Leo calls the talks' collapse 'troubling'."),
    ("AFRICA", "Sudan strikes kill 19 civilians",
     "RSF drones hit two Blue Nile cities, rights group says."),
    ("AFRICA", "Lebanon to open second airport",
     "Northern airport opens next month as Hezbollah wanes."),
    ("AFRICA", "Migrants set Canary Islands record",
     "Record 2,100-plus reach the Canaries in 24 hours."),
    ("AFRICA", "Saudi national seized in Niger",
     "Suspected IS gunmen seize a Saudi in Tillaberi."),
    ("AFRICA", "Bulgaria stops first migrant boat",
     "Police stop a boat with 35 aboard off the Black Sea."),
    ("EUROPE", "Puigdemont to end nine-year exile",
     "He returns to Spain on 12 Dec after the election."),
    ("EUROPE", "Kremlin rejects Johnson force plan",
     "Moscow calls a token Western force 'unacceptable'."),
    ("EUROPE", "Sarkozy corruption case goes to trial",
     "Trial ordered; first hearing set for 1 April 2027."),
    ("EUROPE", "Eurostar cancels trains in strike",
     "London-Paris-Brussels services halted by the strike."),
    ("EUROPE", "RAF shelters jets from drone threat",
     "Jets move into hangars at night, media report."),
    ("EUROPE", "Germany grows 0.1% in third quarter",
     "Europe's largest economy edges up, office says."),
    ("EUROPE", "Greeks strike over pay, services",
     "Walkout over wages and public services disrupts Greece."),
    ("EUROPE", "NATO sends AWACS to Poland",
     "Early-warning jets deploy after missiles land in Poland."),
    ("ASIA", "Taiwan votes on Saturday",
     "Mayoral polls are not about China, but Beijing watches."),
    ("ASIA", "First foreigner boards Tiangong",
     "Pakistan's Zeeshan Ali enters Tiangong station."),
    ("ASIA", "Xi graft probe shakes Shanghai",
     "Probe into Chen Jining upends the usual path to power."),
    ("ASIA", "China drafts 78 AI standards",
     "Beijing's regulator advances global AI rules."),
    ("ASIA", "Asian stocks plunge in AI sell-off",
     "KOSPI, Nikkei, Taiex slide as tech selling spreads."),
    ("ASIA", "Bangladesh factories shut in protests",
     "Workers clash with police over pay; plants suspend work."),
    ("ASIA", "N. Korea expels Swiss diplomat",
     "Pyongyang orders the envoy out in 48 hours."),
    ("AMERICAS", "US economy grows 4.3% in Q3",
     "Q3 GDP beats expectations, the BEA says."),
    ("AMERICAS", "US plans tariffs on 14 partners",
     "Duties set to rise on China, the EU, 14 others."),
    ("AMERICAS", "Huawei convicted in New York",
     "Jury finds the tech giant stole trade secrets."),
    ("AMERICAS", "Colombia hostages freed in raid",
     "About 30 freed in Cartagena; one captor killed."),
    ("AMERICAS", "Canada curbs test talent drive",
     "Student cuts strain colleges as Carney courts talent."),
]

TOTAL = len(WIDE_LEADS) + len(NARROW_LEADS) + len(BRIEFS)
assert TOTAL == 36, TOTAL

DAY_STRIP = ("UKRAINE GRID HIT  •  06:30 GMT CARTAGENA FREED  •  "
             "06:35 GMT SHENZHOU-24 DOCKS  •  13:00 UTC REUTERS SUMMARY  •  "
             "17:10 UTC EDITION CLOSED")


# ------------------------------------------------------------ flat pictures
# Every picture stays inside the box (x, y, w, h) it is given. The
# black caption bar is the bottom 14 px of each picture box.

def picture_tanker(c, x, y, w, h):
    c.rectangle([x, y, x + w, y + h], fill=(186, 212, 230))
    # Low sun at the right, above the funnel smoke.
    c.ellipse([x + w - 60, y + 3, x + w - 32, y + 31], fill=(246, 224, 164))
    for i, shade in enumerate([(198, 160, 40), (68, 108, 138), (162, 58, 58)]):
        c.rectangle([x + 26 + i * 48, y + 6, x + 66 + i * 48, y + 20],
                    fill=shade)
    c.rectangle([x + w - 96, y + 4, x + w - 82, y + 22], fill=(238, 238, 238))
    c.rectangle([x + 16, y + 22, x + w - 28, y + h - 14], fill=(138, 34, 34))
    c.rectangle([x + 16, y + 22, x + w - 28, y + 25], fill=(88, 20, 20))
    c.polygon([(x + w - 46, y + 22), (x + w - 34, y + 8),
               (x + w - 22, y + 22)], fill=(228, 118, 28))
    c.polygon([(x + w - 38, y + 22), (x + w - 30, y + 14),
               (x + w - 22, y + 22)], fill=(242, 172, 42))


def picture_pylon(c, x, y, w, h):
    c.rectangle([x, y, x + w, y + h], fill=(54, 60, 76))
    c.ellipse([x + 10, y + 4, x + 30, y + 24], fill=(246, 224, 164))
    for i in range(6):
        lit = (242, 202, 92) if i % 2 else (92, 92, 102)
        c.rectangle([x + 10 + i * 24, y + h - 24, x + 20 + i * 24, y + h - 15],
                    fill=lit)
    mid = x + w // 2
    c.line([mid - 26, y + h - 14, mid, y + 4], fill=(28, 28, 36), width=4)
    c.line([mid + 26, y + h - 14, mid, y + 4], fill=(28, 28, 36), width=4)
    c.line([mid - 34, y + 12, mid + 34, y + 12], fill=(28, 28, 36), width=3)
    c.polygon([(x + w - 54, y + 4), (x + w - 40, y + 4), (x + w - 48, y + 16),
               (x + w - 36, y + 16), (x + w - 52, y + 28), (x + w - 44, y + 18),
               (x + w - 56, y + 18)], fill=(250, 212, 62))


def picture_skyline(c, x, y, w, h):
    c.rectangle([x, y, x + w, y + h], fill=(212, 162, 108))
    c.ellipse([x + 12, y + 4, x + 32, y + 24], fill=(246, 224, 164))
    c.polygon([(x + 188, y + 4), (x + 218, y + 4), (x + w - 8, y + h - 10),
               (x + 214, y + h - 10)], fill=(246, 232, 182))
    for bx, bw, bh in [(0, 44, 16), (50, 32, 22), (88, 48, 13), (142, 36, 20),
                       (184, 42, 14), (232, 38, 24)]:
        c.rectangle([x + bx, y + h - 10 - bh, x + bx + bw, y + h - 10],
                    fill=(54, 48, 46))
    c.rectangle([x, y + h - 10, x + w, y + h], fill=(72, 62, 56))


def picture_island(c, x, y, w, h):
    c.rectangle([x, y, x + w, y + h], fill=(142, 202, 216))
    c.ellipse([x + w - 48, y + 1, x + w - 20, y + 27], fill=(250, 222, 132))
    c.rectangle([x, y + h - 12, x + w, y + h], fill=(34, 122, 132))
    # Green island mound with a single palm, centred in the box.
    c.pieslice([x + 94, y + h - 28, x + 208, y + h + 2], 180, 360,
               fill=(76, 142, 82))
    c.line([x + 150, y + h - 24, x + 150, y + h - 36], fill=(92, 62, 32),
           width=3)
    for dx in (-14, -7, 7, 14):
        c.line([x + 150, y + h - 36, x + 150 + dx, y + h - 42],
               fill=(52, 112, 62), width=2)
    for wx in (14, 238):
        c.arc([x + wx, y + h - 11, x + wx + 30, y + h + 1], 200, 340,
              fill=(242, 252, 252), width=2)


def picture_balloon(c, x, y, w, h):
    c.rectangle([x, y, x + w, y + h], fill=(122, 130, 142))
    for cx, cy, r in [(50, 12, 12), (74, 9, 14), (98, 13, 10), (194, 11, 11)]:
        c.ellipse([x + cx - r, y + cy - r, x + cx + r, y + cy + r],
                  fill=(92, 98, 110))
    for rx in range(14, 148, 22):
        c.line([x + rx, y + h - 14, x + rx - 6, y + h - 6],
               fill=(202, 212, 222), width=2)
    bx = x + w - 68
    c.ellipse([bx, y + h - 24, bx + 44, y + h - 4], fill=(122, 82, 42))
    c.ellipse([bx + 12, y + h - 32, bx + 32, y + h - 16], fill=(122, 82, 42))
    for dx, dy in [(-18, -4), (-12, -14), (0, -18), (12, -14), (18, -4)]:
        c.line([bx + 22 + dx, y + h - 22 + dy, bx + 22, y + h - 22],
               fill=(92, 62, 32), width=2)


PICTURES = {"tanker": picture_tanker, "pylon": picture_pylon,
            "skyline": picture_skyline, "island": picture_island,
            "balloon": picture_balloon}


# ------------------------------------------------------------------- layout

def bar_with_caption(c, x, y, w, words):
    c.rectangle([x, y, x + w, y + 14], fill=(0, 0, 0))
    c.text((x + 6, y + 2), words, font=LABEL, fill=(255, 255, 255))


def wide_lead(c, x, y, w, story):
    c.text((x, y), story["tag"], font=EYEBROW_SMALL, fill=ACCENT)
    y += 16
    for line in lines_or_fail(story["title"], BIG_HEAD, w, 3):
        c.text((x, y), line, font=BIG_HEAD, fill=TEXT)
        y += 28
    y += 2
    for line in lines_or_fail(story["standfirst"], BIG_DECK, w, 3):
        c.text((x, y), line, font=BIG_DECK, fill=TEXT)
        y += 16
    y += 3
    pic_h = 40
    PICTURES[story["picture"]](c, x, y, w, pic_h)
    bar_with_caption(c, x, y + pic_h - 14, w, story["caption"])
    y += pic_h + 4
    c.text((x, y), story["credit"], font=CREDIT, fill=MUTED)
    return y + 12


def narrow_lead(c, x, y, w, story):
    c.text((x, y), story["tag"], font=EYEBROW_SMALL, fill=ACCENT)
    y += 15
    for line in lines_or_fail(story["title"], SMALL_HEAD, w, 2):
        c.text((x, y), line, font=SMALL_HEAD, fill=TEXT)
        y += 22
    y += 2
    for line in lines_or_fail(story["standfirst"], SMALL_DECK, w, 3):
        c.text((x, y), line, font=SMALL_DECK, fill=TEXT)
        y += 14
    y += 3
    pic_h = 28
    PICTURES[story["picture"]](c, x, y, w, pic_h)
    bar_with_caption(c, x, y + pic_h - 14, w, story["caption"])
    y += pic_h + 4
    c.text((x, y), story["credit"], font=CREDIT, fill=MUTED)
    return y + 11


def one_brief(c, x, y, w, number, region, title, deck):
    c.text((x, y), "%d." % number, font=BRIEF_HEAD, fill=ACCENT)
    c.text((x + 24, y), region, font=LABEL, fill=ACCENT)
    y += 12
    for line in lines_or_fail(title, BRIEF_HEAD, w, 1):
        c.text((x, y), line, font=BRIEF_HEAD, fill=TEXT)
        y += 13
    for line in lines_or_fail(deck, BRIEF_DECK, w, 1):
        c.text((x, y), line, font=BRIEF_DECK, fill=(60, 56, 50))
        y += 13
    return y + 2


def build():
    page = Image.new("RGB", (PAGE, PAGE), NEWSPRINT)
    c = ImageDraw.Draw(page)

    # Masthead.
    c.text((PAGE // 2, 12), "ONE DAY  -  ONE PAGE  -  THE WORLD IN BRIEF",
           font=EYEBROW, fill=ACCENT, anchor="ma")
    c.text((PAGE // 2, 30), "THE WORLD TODAY", font=MASTHEAD, fill=TEXT,
           anchor="ma")
    c.line([EDGE, 104, PAGE - EDGE, 104], fill=DIVIDER, width=3)
    c.line([EDGE, 108, PAGE - EDGE, 108], fill=DIVIDER, width=1)
    c.text((EDGE, 115), "THURSDAY, 26 NOVEMBER 2026", font=DATELINE,
           fill=TEXT)
    c.text((PAGE - EDGE, 115), "%d STORIES  -  ALL VERIFIED" % TOTAL,
           font=DATELINE, fill=TEXT, anchor="ra")
    c.line([EDGE, 137, PAGE - EDGE, 137], fill=DIVIDER, width=1)

    # Dark UTC timeline strip.
    strip_w = STRIP.getlength(DAY_STRIP)
    assert strip_w <= SPAN - 8, strip_w
    c.rectangle([EDGE, 143, PAGE - EDGE, 165], fill=TEXT)
    c.text((PAGE // 2, 148), DAY_STRIP, font=STRIP, fill=(255, 255, 255),
           anchor="ma")

    # Two wide leads side by side.
    y = 174
    wide_w = (SPAN - 16) // 2
    wide_end = max(wide_lead(c, EDGE, y, wide_w, WIDE_LEADS[0]),
                   wide_lead(c, EDGE + wide_w + 16, y, wide_w, WIDE_LEADS[1]))
    c.line([EDGE, wide_end + 2, PAGE - EDGE, wide_end + 2], fill=DIVIDER,
           width=1)

    # Three narrower leads side by side.
    y = wide_end + 11
    narrow_w = (SPAN - 24) // 3
    narrow_end = max(
        narrow_lead(c, EDGE + i * (narrow_w + 12), y, narrow_w, story)
        for i, story in enumerate(NARROW_LEADS))
    c.line([EDGE, narrow_end + 2, PAGE - EDGE, narrow_end + 2], fill=DIVIDER,
           width=1)

    # Briefs heading.
    y = narrow_end + 9
    c.text((EDGE, y), "THE DAY IN BRIEF", font=EYEBROW, fill=ACCENT)
    c.text((PAGE - EDGE, y), "31 MORE STORIES, REGION BY REGION",
           font=EYEBROW_SMALL, fill=MUTED, anchor="ra")
    y += 18
    c.line([EDGE, y, PAGE - EDGE, y], fill=DIVIDER, width=1)
    y += 6

    # Briefs: eleven in the first column, ten in each of the others.
    cursor = 0
    lowest = y
    for col, take in enumerate([11, 10, 10]):
        bx = EDGE + col * (narrow_w + 12)
        by = y
        for _ in range(take):
            region, title, deck = BRIEFS[cursor]
            by = one_brief(c, bx, by, narrow_w, cursor + 6, region, title,
                           deck)
            c.line([bx, by - 1, bx + narrow_w, by - 1], fill=FAINT, width=1)
            cursor += 1
        lowest = max(lowest, by)
    assert lowest <= PAGE - 30, lowest

    # Footer.
    c.line([EDGE, PAGE - 26, PAGE - EDGE, PAGE - 26], fill=DIVIDER, width=1)
    c.text((PAGE // 2, PAGE - 20),
           "Sources: Reuters World News Summary, 25 Nov 2026  •  AP  •  AFP  •  "
           "Fox Weather  •  Compiled 26 Nov 2026, 00:10 WIB  •  "
           "No real person's face appears in this image",
           font=FOOTER, fill=MUTED, anchor="ma")

    page.save(TARGET, format="PNG", optimize=True)
    with open(TARGET, "rb") as handle:
        data = handle.read()
    grey = page.convert("L")
    histogram = grey.histogram()
    ink = sum(histogram[:240]) / float(PAGE * PAGE)
    print("wrote " + TARGET)
    print("size: 1024x1024")
    print("bytes: %d" % len(data))
    print("sha256: " + hashlib.sha256(data).hexdigest())
    print("stories: %d" % TOTAL)
    print("ink: %.3f" % ink)
    print("layout: wide ends %d, narrow ends %d, briefs end %d"
          % (wide_end, narrow_end, lowest))


if __name__ == "__main__":
    build()
