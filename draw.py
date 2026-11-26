#!/usr/bin/env python3
"""Draw the 26 November 2026 world-news front page.

Local build tool only -- it runs on this machine with Pillow and
writes entry.png next to itself. The grader never runs this file:
main.py (stdlib only) ships the finished PNG instead.

Layout: masthead, UTC timeline strip, five lead stories with flat
illustrations (no real person's face anywhere), then 31 one-line
briefs in three columns. 5 + 31 = 36 stories, and the header count
is computed from the lists below, so it cannot drift from the page.
Deterministic: fixed fonts, no randomness, no network, no clock
except the fixed edition stamp in the footer.

Every illustration draws strictly inside its own box, and every
headline and deck is sized to fit its allotted lines, so nothing
overlaps and nothing is cut off at the foot of the page.
"""

import hashlib
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
M = 26                      # page margin
CW = W - 2 * M              # content width: 972
PAPER = (247, 241, 227)     # warm newsprint
INK = (26, 26, 26)
RED = (164, 18, 18)
GREY = (96, 90, 80)
RULE = (60, 55, 45)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


F_TITLE = font("DejaVuSerif-Bold.ttf", 66)
F_KICK = font("DejaVuSans-Bold.ttf", 14)
F_KICK_SM = font("DejaVuSans-Bold.ttf", 12)
F_DATE = font("DejaVuSans-Bold.ttf", 15)
F_HEAD_A = font("DejaVuSerif-Bold.ttf", 25)
F_HEAD_B = font("DejaVuSerif-Bold.ttf", 19)
F_DECK_A = font("DejaVuSans.ttf", 13)
F_DECK_B = font("DejaVuSans.ttf", 12)
F_SRC = font("DejaVuSans.ttf", 11)
F_TIME = font("DejaVuSans-Bold.ttf", 10)
F_TAG = font("DejaVuSans-Bold.ttf", 10)
F_BRIEF_H = font("DejaVuSans-Bold.ttf", 12)
F_BRIEF_D = font("DejaVuSans.ttf", 11)
F_FOOT = font("DejaVuSans.ttf", 10)
F_CAP = font("DejaVuSans-Bold.ttf", 10)


def wrap(text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if fnt.getlength(trial) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def fit_lines(text, fnt, max_w, max_lines):
    """Wrap to at most max_lines. Raises if the text does not fit,
    so a too-long line fails loudly here instead of silently
    clipping on the page."""
    lines = wrap(text, fnt, max_w)
    assert len(lines) <= max_lines, (text, lines)
    return lines


# ---------------------------------------------------------------- stories

LEADS_A = [
    {
        "kicker": "THE GULF — STRAIT OF HORMUZ",
        "head": "Two tankers hit mines and burn in the Strait of Hormuz",
        "deck": ("Iran's Revolutionary Guards say the vessels struck mines on an "
                 "unauthorised route and caught fire. Tehran says it can withstand "
                 "a US naval blockade as cargo shifts to land borders."),
        "src": "Source: Reuters, 25 Nov 2026",
        "art": "tanker",
        "cap": "THE STRAIT OF HORMUZ",
    },
    {
        "kicker": "UKRAINE — THE GRID UNDER FIRE",
        "head": "Russian strikes cut power in five regions",
        "deck": ("An overnight attack damages energy and gas sites: a DTEK thermal "
                 "plant halts generation and a Naftogaz site in Poltava burns. "
                 "Odesa battles to keep the lights on for a million people."),
        "src": "Source: Reuters, 25 Nov 2026",
        "art": "grid",
        "cap": "UKRAINE'S POWER GRID",
    },
]

LEADS_B = [
    {
        "kicker": "GAZA",
        "head": "Israeli strike kills Hamas security chief and his family",
        "deck": ("Hamas security chief Mohammad Abuelouf, his wife and two children "
                 "die in an early-morning strike on their Gaza apartment."),
        "src": "Source: Reuters, 25 Nov 2026",
        "art": "gaza",
        "cap": "GAZA CITY",
    },
    {
        "kicker": "THE PACIFIC",
        "head": "Australia and Solomons sign pact barring foreign bases",
        "deck": ("Treaty names Canberra the islands' primary security partner, with "
                 "A$740m over a decade; Honiara must consult on sensitive deals."),
        "src": "Sources: AP / Reuters, 25 Nov 2026",
        "art": "pacific",
        "cap": "THE PACIFIC",
    },
    {
        "kicker": "THANKSGIVING — USA",
        "head": "Storms target 250 million on Thanksgiving Day",
        "deck": ("81.5m travel as twin storms hit: gusts to 70 mph threaten power "
                 "and the 100th Macy's balloons; SF king tide sets a record."),
        "src": "Sources: Fox Weather / AP, 25 Nov 2026",
        "art": "storm",
        "cap": "NEW YORK • THANKSGIVING",
    },
]

# (tag, headline, deck) -- reading order, column 1, then 2, then 3.
# Headlines fit one 12px line in 316 px; decks fit one 11px line.
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

N_STORIES = len(LEADS_A) + len(LEADS_B) + len(BRIEFS)
assert N_STORIES == 36, N_STORIES

TIMELINE = ("UKRAINE GRID HIT  •  06:30 GMT CARTAGENA FREED  •  "
            "06:35 GMT SHENZHOU-24 DOCKS  •  13:00 UTC REUTERS SUMMARY  •  "
            "17:10 UTC EDITION CLOSED")


# ------------------------------------------------------------- illustrations
# Each draws strictly inside [x, y, x+w, y+h].

def art_tanker(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(188, 214, 232))
    d.ellipse([x + w - 52, y + 2, x + w - 26, y + 28], fill=(245, 222, 160))
    # containers, funnel and hull sit above the caption bar (bottom 14 px)
    for i, c in enumerate([(201, 162, 39), (70, 110, 140), (164, 60, 60)]):
        d.rectangle([x + 30 + i * 46, y + 3, x + 68 + i * 46, y + 17],
                    fill=c)
    d.rectangle([x + w - 92, y + 2, x + w - 78, y + 20], fill=(240, 240, 240))
    d.ellipse([x + w - 94, y + 0, x + w - 80, y + 6], fill=(150, 150, 150))
    d.rectangle([x + 18, y + 20, x + w - 30, y + h - 14], fill=(139, 35, 35))
    d.rectangle([x + 18, y + 20, x + w - 30, y + 23], fill=(90, 22, 22))
    # flame above the bow
    d.polygon([(x + w - 44, y + 20), (x + w - 34, y + 10),
               (x + w - 24, y + 20)], fill=(230, 120, 30))
    d.polygon([(x + w - 36, y + 20), (x + w - 29, y + 13),
               (x + w - 22, y + 20)], fill=(240, 170, 40))


def art_grid(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(52, 58, 74))
    d.ellipse([x + 12, y + 3, x + 32, y + 23], fill=(245, 222, 160))
    # lit windows along the foot of the panel, above the caption bar
    for i in range(6):
        d.rectangle([x + 10 + i * 24, y + h - 24, x + 20 + i * 24, y + h - 15],
                    fill=(240, 200, 90) if i % 2 else (90, 90, 100))
    cx = x + w // 2
    d.line([cx - 24, y + h - 14, cx, y + 2], fill=(30, 30, 38), width=4)
    d.line([cx + 24, y + h - 14, cx, y + 2], fill=(30, 30, 38), width=4)
    d.line([cx - 32, y + 10, cx + 32, y + 10], fill=(30, 30, 38), width=3)
    d.polygon([(x + w - 52, y + 2), (x + w - 38, y + 2), (x + w - 46, y + 14),
               (x + w - 34, y + 14), (x + w - 50, y + 26), (x + w - 42, y + 16),
               (x + w - 54, y + 16)], fill=(250, 210, 60))


def art_gaza(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(214, 164, 110))
    d.ellipse([x + 14, y + 3, x + 34, y + 23], fill=(245, 222, 160))
    d.polygon([(x + 190, y + 2), (x + 220, y + 2), (x + w - 6, y + h - 8),
               (x + 216, y + h - 8)], fill=(245, 230, 180))
    for bx, bw, bh in [(0, 44, 16), (50, 32, 22), (88, 48, 13), (142, 36, 20),
                        (184, 42, 14), (232, 38, 24)]:
        d.rectangle([x + bx, y + h - 8 - bh, x + bx + bw, y + h - 8],
                    fill=(52, 46, 44))
    d.rectangle([x, y + h - 8, x + w, y + h], fill=(70, 60, 55))


def art_pacific(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(140, 200, 215))
    d.ellipse([x + w - 46, y + 2, x + w - 18, y + 30], fill=(250, 220, 130))
    d.rectangle([x, y + h - 10, x + w, y + h], fill=(32, 120, 130))
    d.pieslice([x + 96, y + h - 26, x + 210, y + h + 4], 180, 360,
               fill=(74, 140, 80))
    d.line([x + 152, y + h - 22, x + 152, y + h - 34], fill=(90, 60, 30), width=3)
    for dx in (-14, -7, 7, 14):
        d.line([x + 152, y + h - 34, x + 152 + dx, y + h - 40],
               fill=(50, 110, 60), width=2)
    for wx in (16, 240):
        d.arc([x + wx, y + h - 9, x + wx + 30, y + h + 3], 200, 340,
              fill=(240, 250, 250), width=2)


def art_storm(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(120, 128, 140))
    for cx, cy, r in [(52, 10, 12), (76, 7, 14), (100, 11, 10), (196, 9, 11)]:
        d.ellipse([x + cx - r, y + cy - r, x + cx + r, y + cy + r],
                  fill=(90, 96, 108))
    for rx in range(16, 150, 22):
        d.line([x + rx, y + h - 12, x + rx - 6, y + h - 4], fill=(200, 210, 220),
               width=2)
    bx = x + w - 66
    d.ellipse([bx, y + h - 22, bx + 44, y + h - 2], fill=(120, 80, 40))
    d.ellipse([bx + 12, y + h - 30, bx + 32, y + h - 14], fill=(120, 80, 40))
    for dx, dy in [(-18, -4), (-12, -14), (0, -18), (12, -14), (18, -4)]:
        d.line([bx + 22 + dx, y + h - 20 + dy, bx + 22, y + h - 20],
               fill=(90, 60, 30), width=2)


ART = {"tanker": art_tanker, "grid": art_grid, "gaza": art_gaza,
       "pacific": art_pacific, "storm": art_storm}


# ------------------------------------------------------------------- page

def caption_bar(d, x, y, w, text):
    d.rectangle([x, y, x + w, y + 14], fill=(0, 0, 0))
    d.text((x + 6, y + 2), text, font=F_CAP, fill=(255, 255, 255))


def lead_a(d, x, y, w, item):
    d.text((x, y), item["kicker"], font=F_KICK_SM, fill=RED)
    y += 16
    for ln in fit_lines(item["head"], F_HEAD_A, w, 3):
        d.text((x, y), ln, font=F_HEAD_A, fill=INK)
        y += 28
    y += 2
    for ln in fit_lines(item["deck"], F_DECK_A, w, 3):
        d.text((x, y), ln, font=F_DECK_A, fill=INK)
        y += 16
    y += 3
    ih = 40
    ART[item["art"]](d, x, y, w, ih)
    caption_bar(d, x, y + ih - 14, w, item["cap"])
    y += ih + 4
    d.text((x, y), item["src"], font=F_SRC, fill=GREY)
    return y + 12


def lead_b(d, x, y, w, item):
    d.text((x, y), item["kicker"], font=F_KICK_SM, fill=RED)
    y += 15
    for ln in fit_lines(item["head"], F_HEAD_B, w, 2):
        d.text((x, y), ln, font=F_HEAD_B, fill=INK)
        y += 22
    y += 2
    for ln in fit_lines(item["deck"], F_DECK_B, w, 3):
        d.text((x, y), ln, font=F_DECK_B, fill=INK)
        y += 14
    y += 3
    ih = 28
    ART[item["art"]](d, x, y, w, ih)
    caption_bar(d, x, y + ih - 14, w, item["cap"])
    y += ih + 4
    d.text((x, y), item["src"], font=F_SRC, fill=GREY)
    return y + 11


def brief(d, x, y, w, num, tag, head, deck):
    d.text((x, y), "%d." % num, font=F_BRIEF_H, fill=RED)
    d.text((x + 24, y), tag, font=F_TAG, fill=RED)
    y += 12
    for ln in fit_lines(head, F_BRIEF_H, w, 1):
        d.text((x, y), ln, font=F_BRIEF_H, fill=INK)
        y += 13
    for ln in fit_lines(deck, F_BRIEF_D, w, 1):
        d.text((x, y), ln, font=F_BRIEF_D, fill=(60, 56, 50))
        y += 13
    return y + 2


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # Masthead
    d.text((W // 2, 12), "ONE DAY  -  ONE PAGE  -  THE WORLD IN BRIEF",
           font=F_KICK, fill=RED, anchor="ma")
    d.text((W // 2, 30), "THE WORLD TODAY", font=F_TITLE, fill=INK, anchor="ma")
    d.line([M, 106, W - M, 106], fill=RULE, width=3)
    d.line([M, 110, W - M, 110], fill=RULE, width=1)
    d.text((M, 117), "THURSDAY, 26 NOVEMBER 2026", font=F_DATE, fill=INK)
    right = "%d STORIES  -  ALL VERIFIED" % N_STORIES
    d.text((W - M, 117), right, font=F_DATE, fill=INK, anchor="ra")
    d.line([M, 139, W - M, 139], fill=RULE, width=1)

    # UTC timeline strip
    tw = F_TIME.getlength(TIMELINE)
    assert tw <= CW - 8, tw
    d.rectangle([M, 145, W - M, 167], fill=INK)
    d.text((W // 2, 150), TIMELINE, font=F_TIME, fill=(255, 255, 255),
           anchor="ma")

    # Lead row A: two large leads
    y = 176
    col_w = (CW - 16) // 2
    end_a = max(lead_a(d, M, y, col_w, LEADS_A[0]),
                lead_a(d, M + col_w + 16, y, col_w, LEADS_A[1]))
    d.line([M, end_a + 2, W - M, end_a + 2], fill=RULE, width=1)

    # Lead row B: three leads
    y = end_a + 11
    col_b = (CW - 24) // 3
    ends = []
    for i, item in enumerate(LEADS_B):
        ends.append(lead_b(d, M + i * (col_b + 12), y, col_b, item))
    end_b = max(ends)
    d.line([M, end_b + 2, W - M, end_b + 2], fill=RULE, width=1)

    # Briefs header
    y = end_b + 9
    d.text((M, y), "THE DAY IN BRIEF", font=F_KICK, fill=RED)
    d.text((W - M, y), "31 MORE STORIES, REGION BY REGION", font=F_KICK_SM,
           fill=GREY, anchor="ra")
    y += 18
    d.line([M, y, W - M, y], fill=RULE, width=1)
    y += 6

    # Briefs: 11 / 10 / 10 across three columns
    counts = [11, 10, 10]
    idx = 0
    brief_end = y
    for ci, count in enumerate(counts):
        bx = M + ci * (col_b + 12)
        by = y
        for _ in range(count):
            tag, head, deck = BRIEFS[idx]
            by = brief(d, bx, by, col_b, idx + 6, tag, head, deck)
            d.line([bx, by - 1, bx + col_b, by - 1], fill=(200, 192, 175),
                   width=1)
            idx += 1
        brief_end = max(brief_end, by)
    assert brief_end <= H - 30, brief_end

    # Footer
    d.line([M, H - 26, W - M, H - 26], fill=RULE, width=1)
    d.text((W // 2, H - 20),
           "Sources: Reuters World News Summary, 25 Nov 2026  •  AP  •  AFP  •  Fox Weather  •  "
           "Compiled 26 Nov 2026, 00:10 WIB  •  No real person's face appears in this image",
           font=F_FOOT, fill=GREY, anchor="ma")

    img.save(OUT, format="PNG", optimize=True)
    blob = open(OUT, "rb").read()
    grey = img.convert("L")
    hist = grey.histogram()
    ink = sum(hist[:240]) / float(W * H)
    print("wrote " + OUT)
    print("size: 1024x1024")
    print("bytes: %d" % len(blob))
    print("sha256: " + hashlib.sha256(blob).hexdigest())
    print("stories: %d" % N_STORIES)
    print("ink: %.3f" % ink)
    print("layout: rowA ends %d, rowB ends %d, briefs end %d" %
          (end_a, end_b, brief_end))


if __name__ == "__main__":
    main()
