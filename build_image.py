#!/usr/bin/env python3
"""Render one newspaper front page summing up Saturday 21 November 2026.

Everything here is authored in this session: the story list was researched
from public reporting on the morning of 21 Nov 2026 (03:30 UTC), and the
drawing code is an original, data-driven layout. Output is deterministic:
no clock, no randomness, fixed palette and fonts, so re-running the script
reproduces the same PNG bytes.
"""

from __future__ import annotations

import os
import textwrap

from PIL import Image, ImageDraw, ImageFont

# ---------------------------------------------------------------- canvas ---
CANVAS_W = 1024
CANVAS_H = 1024
EDGE = 20                      # outer margin
INNER_W = CANVAS_W - 2 * EDGE  # 984

PAPER = (247, 243, 234)
INK = (22, 22, 22)
SOFT_INK = (74, 74, 74)
FAINT = (148, 140, 126)
RULE = (22, 22, 22)
ACCENT = (172, 32, 28)        # deep red
OCEAN = (28, 62, 112)         # deep blue
SAND = (232, 224, 205)
CARD = (255, 253, 247)
GOLD = (176, 128, 28)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def typeface(path: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(path, size)


# -------------------------------------------------------------- the news ---
# Headlines and decks are paraphrased from public reporting checked on
# 21 Nov 2026. Each item: (section, place, headline, deck).
LEAD_ITEMS = [
    (
        "DISASTER",
        "Junin, Peru",
        "A 6.8 quake shakes Peru",
        "The tremor struck the Andes at 19:09 local time on Friday, "
        "129 km deep, and was felt 320 km away in Lima, where crowds "
        "poured into the streets. No casualties were reported at once.",
    ),
    (
        "MARKETS",
        "New York",
        "Wall Street slides into correction",
        "The Nasdaq fell 5.28% and the S&P 500 dropped 3.7%, "
        "its seventh straight loss, as Nvidia sank 14% after "
        "reports of an SEC accounting review.",
    ),
    (
        "CONFLICT",
        "South-east Poland",
        "Russian missiles come down in Poland",
        "Two cruise missiles and a suspected drone crashed on Polish "
        "soil; Warsaw called it a provocation, NATO a grave violation.",
    ),
]

GRID_ITEMS = [
    ("WAR", "Kryvyi Rih, Ukraine", "Missiles kill a child and a paramedic",
     "A double-tap ballistic strike killed 2 and hurt 42, four of them children."),
    ("DIPLOMACY", "Shenzhen, China", "Trump, Xi and Putin meet, few results",
     "The first three-way summit ended with warm words, a pledge on human control of military AI, and little concrete."),
    ("JUSTICE", "The Hague", "World Court: Myanmar committed genocide",
     "The ICJ ruled state forces committed genocide against the Rohingya."),
    ("EUROPE", "Brussels", "UK and EU sign food, carbon and youth deals",
     "Three agreements were signed at a Brussels summit led by PM Andy Burnham."),
    ("GAZA", "Gaza", "Four nations demand aid reach flooded Gaza",
     "Australia, Canada, Italy and the UK called for immediate, unrestricted access."),
    ("ESPIONAGE", "Copenhagen", "Denmark expels Russian diplomat",
     "Police say they foiled a plot to kill Ukrainian rapper Kyivstoner before a concert."),
    ("BORDERS", "Tallinn", "Estonia shuts its crossings to Russia",
     "The shutdown followed suspected arson sabotage at a drone maker."),
    ("AID", "Brussels", "EU approves EUR 1bn in arms aid for Kyiv",
     "The UK also pledged 1,000-plus drones in a GBP 260m package."),
    ("WASHINGTON", "Washington", "Senate rejects Iran war-powers curb, 51-48",
     "The vote leaves the president free as he weighs renewed strikes on Iran."),
    ("SANCTIONS", "Washington", "US blacklists four Iranians over oil cash",
     "Treasury also sanctioned the Comancheros and the 'Ndrangheta."),
    ("GULF", "Riyadh", "Houthi missiles over Riyadh intercepted",
     "The Saudi-led coalition said it downed three missiles and struck Hodeidah."),
    ("CLIMATE", "Antalya", "COP31 ends its final day with no deal",
     "Talks ran overnight toward a third draft after fossil-fuel wording was cut."),
    ("INDIA", "Mumbai", "Foreign cash floods Indian shares: record",
     "A net Rs 1.22 lakh crore flowed in between 2 and 20 November, an all-time high."),
    ("NEPAL", "New Delhi", "Nepal's PM begins first trip abroad in Delhi",
     "Balendra Shah arrived for a two-day state visit, his first since March."),
    ("NEW YORK", "New York", "Mamdani sets 2032 to close Rikers Island",
     "The mayor's plan replaces the 2027 legal deadline with a 2032 target."),
    ("CRICKET", "Wellington", "Rahul completes the SENA century set",
     "His 100 off 207 balls made him the first Indian opener with Test tons in all four SENA lands."),
    ("FOOTBALL", "Munich", "Kane tears ankle ligament, out for months",
     "Bayern's striker was hurt in Friday's 1-1 draw with Cologne."),
    ("NFL", "Houston", "Texans flatten the Colts, 26-3",
     "A dominant defence kept Houston's playoff hopes alive on Thursday night."),
    ("BASEBALL", "Washington", "Trump pardons Pete Rose posthumously",
     "The late baseball star was pardoned by the president on Friday."),
    ("LAW", "Los Angeles", "Man convicted of starting Palisades Fire",
     "A jury found Jonathan Rinderknecht guilty of igniting the blaze."),
    ("ENERGY", "Washington", "US details $12bn in Venezuelan oil revenue",
     "A 53-page State Department report tracks the money, nearly a year after Maduro's capture."),
    ("ISRAEL", "Jerusalem", "Eisenkot tapped to form next government",
     "President Herzog chose the ex-army chief over PM Netanyahu."),
    ("FRANCE", "Paris", "Fourth weekend of cost-of-living protests",
     "Demonstrations spread across France over rising prices."),
    ("SHIPPING", "Strait of Hormuz", "Tanker struck and on fire off Oman",
     "UKMTO reported the incident eight nautical miles north of Khasab."),
    ("TECH", "Washington", "US warns tech firms over offshore data centres",
     "US tech firms building abroad face 'tremendous penalties', he warned."),
    ("ASIA", "Pyongyang", "Satellites show N. Korea uranium plant growing",
     "Imagery points to an expansion of the enrichment site."),
    ("ARGENTINA", "Buenos Aires", "Senate backs disability law, 71-0",
     "The permanent framework passed unanimously on 20 November."),
]

# (utc time, label) — times approximate, UTC.
DAY_TIMELINE = [
    ("00:09", "Peru quake strikes Junin, felt in Lima"),
    ("01:30", "Russian missiles confirmed down in Poland"),
    ("07:00", "Rahul reaches his hundred in Wellington"),
    ("12:00", "UK-EU deals signed in Brussels"),
    ("16:00", "ICJ genocide ruling read in The Hague"),
    ("21:00", "Wall Street closes; COP31 talks run on"),
]

MARKET_ROWS = [
    ("NASDAQ", "22,617.73", "-5.28%", -5.28),
    ("S&P 500", "6,910.39", "-3.70%", -3.70),
    ("DOW", "48,147.33", "-1.93%", -1.93),
    ("NVIDIA", "$125.53", "-14%", -14.0),
    ("GOLD", "$3,537.77", "-2.41%", -2.41),
    ("WTI OIL", "$83.70", "+1.53%", 1.53),
]

STAT_CELLS = [
    ("30", "verified stories"),
    ("6.8", "Peru quake magnitude"),
    ("-5.28%", "Nasdaq, Friday"),
    ("51-48", "Senate Iran vote"),
    ("2 dead, 42 hurt", "Kryvyi Rih strike"),
]

# Numbered pins on the schematic map: (x, y, number, label).
MAP_PINS = [
    (120, 50, "1", "Lima"),
    (205, 28, "2", "New York"),
    (425, 20, "3", ""),
    (412, 38, "4", ""),
    (520, 34, "5", "Shenzhen"),
    (400, 52, "6", ""),
    (455, 60, "7", "Riyadh"),
    (575, 70, "8", "Wellington"),
]

LEFT_OFF = [
    "Homo erectus fossils in China (Nature papers, 18 Nov) - older than today.",
    "Crimean Bridge strikes of 19 Nov - superseded by the 20 Nov strikes.",
    "Anthropic's IPO debut (19-20 Nov) - folded into the markets story.",
]


# ------------------------------------------------------------ text tools ---
class Typesetter:
    """Font cache plus wrapping measured with the real renderer."""

    def __init__(self, canvas: ImageDraw.ImageDraw):
        self.canvas = canvas
        self._cache: dict[tuple[str, int], ImageFont.FreeTypeFont] = {}

    def font(self, path: str, size: int) -> ImageFont.FreeTypeFont:
        key = (path, size)
        if key not in self._cache:
            self._cache[key] = typeface(path, size)
        return self._cache[key]

    def width(self, text: str, path: str, size: int) -> float:
        return self.canvas.textlength(text, font=self.font(path, size))

    def wrap(self, text: str, path: str, size: int, max_w: int) -> list[str]:
        words = text.split()
        lines: list[str] = []
        current = ""
        for word in words:
            trial = f"{current} {word}".strip()
            if self.width(trial, path, size) <= max_w or not current:
                current = trial
            else:
                lines.append(current)
                current = word
        if current:
            lines.append(current)
        return lines

    def fit_one_line(self, text: str, path: str, size: int, max_w: int) -> str:
        if self.width(text, path, size) <= max_w:
            return text
        trimmed = text
        while trimmed and self.width(trimmed + "...", path, size) > max_w:
            trimmed = trimmed[:-1].rstrip()
        return trimmed + "..."


def draw_rule(canvas: ImageDraw.ImageDraw, x0: int, y: int, x1: int,
               weight: int = 2, colour=INK) -> None:
    canvas.line([(x0, y), (x1, y)], fill=colour, width=weight)


# ------------------------------------------------------------- the page ----
class FrontPage:
    """Owns the sheet, lays out each band top to bottom, then saves."""

    def __init__(self):
        self.sheet = Image.new("RGB", (CANVAS_W, CANVAS_H), PAPER)
        self.pen = ImageDraw.Draw(self.sheet)
        self.set = Typesetter(self.pen)

    # -- masthead ------------------------------------------------------
    def paint_masthead(self) -> None:
        pen, set_ = self.pen, self.set
        top = 16
        eyebrow = "THE WORLD IN ONE IMAGE  |  ONE DAY, EVERYWHERE  |  No. 325"
        pen.text((EDGE, top), eyebrow,
                 font=set_.font(SANS_BOLD, 12), fill=ACCENT)
        pen.text((CANVAS_W - EDGE - set_.width("PRICE: ONE READ", SANS_BOLD, 12),
                  top), "PRICE: ONE READ", font=set_.font(SANS_BOLD, 12),
                 fill=SOFT_INK)
        draw_rule(pen, EDGE, top + 22, CANVAS_W - EDGE, 3)
        draw_rule(pen, EDGE, top + 27, CANVAS_W - EDGE, 1)

        headline = "Saturday 21 November 2026"
        pen.text((EDGE, top + 36), headline,
                 font=set_.font(SERIF_BOLD, 46), fill=INK)
        sub = "Thirty verified stories from overnight and Friday - quake, correction, missiles and a court ruling that made history."
        for i, line in enumerate(set_.wrap(sub, SANS, 13, INNER_W)):
            pen.text((EDGE, top + 96 + i * 17), line,
                     font=set_.font(SANS, 13), fill=SOFT_INK)
        draw_rule(pen, EDGE, top + 112, CANVAS_W - EDGE, 3)

    # -- stat band -----------------------------------------------------
    def paint_statband(self, y: int) -> int:
        pen, set_ = self.pen, self.set
        cell_w = INNER_W // len(STAT_CELLS)
        for idx, (big, small) in enumerate(STAT_CELLS):
            x = EDGE + idx * cell_w
            pen.rectangle([x + 2, y, x + cell_w - 2, y + 40], fill=CARD,
                          outline=FAINT)
            pen.text((x + 10, y + 5), big, font=set_.font(SERIF_BOLD, 17),
                     fill=ACCENT if idx % 2 == 0 else OCEAN)
            pen.text((x + 10, y + 24), small, font=set_.font(SANS, 10),
                     fill=SOFT_INK)
        return y + 48

    # -- lead stories --------------------------------------------------
    def paint_leads(self, y: int) -> int:
        pen, set_ = self.pen, self.set
        left_w = 640
        right_w = INNER_W - left_w - 12
        rx = EDGE + left_w + 12

        section, place, head, deck = LEAD_ITEMS[0]
        pen.rectangle([EDGE, y, EDGE + left_w, y + 118], fill=CARD,
                      outline=RULE)
        pen.rectangle([EDGE, y, EDGE + 8, y + 118], fill=ACCENT)
        pen.text((EDGE + 18, y + 8), f"{section}  -  {place.upper()}",
                 font=set_.font(SANS_BOLD, 11), fill=ACCENT)
        pen.text((EDGE + 18, y + 26), head,
                 font=set_.font(SERIF_BOLD, 24), fill=INK)
        for i, line in enumerate(set_.wrap(deck, SANS, 12, left_w - 36)):
            pen.text((EDGE + 18, y + 60 + i * 16), line,
                     font=set_.font(SANS, 12), fill=SOFT_INK)

        for slot, (section, place, head, deck) in enumerate(LEAD_ITEMS[1:]):
            sy = y + slot * 59
            pen.rectangle([rx, sy, rx + right_w, sy + 57], fill=CARD,
                          outline=FAINT)
            pen.rectangle([rx, sy, rx + 6, sy + 57],
                          fill=OCEAN if slot == 0 else ACCENT)
            pen.text((rx + 14, sy + 4), f"{section}  -  {place.upper()}",
                     font=set_.font(SANS_BOLD, 9), fill=OCEAN)
            pen.text((rx + 14, sy + 16), head,
                     font=set_.font(SERIF_BOLD, 14), fill=INK)
            deck_lines = set_.wrap(deck, SANS, 9, right_w - 28)
            for j, line in enumerate(deck_lines[:2]):
                pen.text((rx + 14, sy + 35 + j * 11), line,
                         font=set_.font(SANS, 9), fill=SOFT_INK)
        return y + 118

    # -- timeline ------------------------------------------------------
    def paint_timeline(self, y: int) -> int:
        pen, set_ = self.pen, self.set
        pen.text((EDGE, y), "THE DAY, HOUR BY HOUR  (UTC, approximate)",
                 font=set_.font(SANS_BOLD, 11), fill=INK)
        line_y = y + 38
        draw_rule(pen, EDGE, line_y, CANVAS_W - EDGE, 2, FAINT)
        slot_w = INNER_W // len(DAY_TIMELINE)
        for idx, (clock, label) in enumerate(DAY_TIMELINE):
            cx = EDGE + idx * slot_w + slot_w // 2
            pen.ellipse([cx - 5, line_y - 5, cx + 5, line_y + 5],
                        fill=ACCENT, outline=PAPER)
            pen.text((cx - set_.width(clock, SANS_BOLD, 11) / 2, line_y - 20),
                     clock, font=set_.font(SANS_BOLD, 11), fill=INK)
            label_lines = set_.wrap(label, SANS, 9, slot_w - 12)
            for j, line in enumerate(label_lines[:2]):
                pen.text((cx - slot_w // 2 + 6, line_y + 10 + j * 12), line,
                         font=set_.font(SANS, 9), fill=SOFT_INK)
        return y + 76

    # -- story grid ----------------------------------------------------
    def paint_grid(self, y: int) -> int:
        pen, set_ = self.pen, self.set
        cols = 3
        gap = 10
        card_w = (INNER_W - gap * (cols - 1)) // cols
        row_h = 42
        rows = (len(GRID_ITEMS) + cols - 1) // cols
        colours = [ACCENT, OCEAN, GOLD, (46, 110, 58), (110, 46, 96),
                   (150, 90, 20)]
        for idx, (section, place, head, deck) in enumerate(GRID_ITEMS):
            row, col = divmod(idx, cols)
            x = EDGE + col * (card_w + gap)
            cy = y + row * (row_h + 3)
            pen.rectangle([x, cy, x + card_w, cy + row_h], fill=CARD,
                          outline=FAINT)
            pen.rectangle([x, cy, x + 4, cy + row_h],
                          fill=colours[idx % len(colours)])
            title = set_.fit_one_line(head, SANS_BOLD, 11, card_w - 16)
            pen.text((x + 12, cy + 4), title,
                     font=set_.font(SANS_BOLD, 11), fill=INK)
            body = f"{section} - {place} - {deck}"
            body_lines = set_.wrap(body, SANS, 9, card_w - 16)
            for j, line in enumerate(body_lines[:2]):
                pen.text((x + 12, cy + 19 + j * 11), line,
                         font=set_.font(SANS, 9), fill=SOFT_INK)
        return y + rows * (row_h + 3) - 3

    # -- schematic map + verdict ---------------------------------------
    def paint_map_and_verdict(self, y: int) -> int:
        pen, set_ = self.pen, self.set
        map_w = 620
        map_h = 88
        pen.rectangle([EDGE, y, EDGE + map_w, y + map_h], fill=CARD,
                      outline=RULE)
        pen.text((EDGE + 10, y + 6), "WHERE IT HAPPENED - SCHEMATIC, NOT TO SCALE",
                 font=set_.font(SANS_BOLD, 10), fill=OCEAN)
        blobs = [
            (28, 18, 120, 42), (150, 48, 90, 24), (300, 10, 130, 30),
            (330, 46, 80, 26), (440, 14, 130, 40), (560, 54, 44, 20),
        ]
        for (bx, by, bw, bh) in blobs:
            pen.ellipse([EDGE + bx, y + by, EDGE + bx + bw, y + by + bh],
                        fill=SAND, outline=FAINT)
        for (px, py, num, label) in MAP_PINS:
            pen.ellipse([EDGE + px - 8, y + py - 8, EDGE + px + 8, y + py + 8],
                        fill=ACCENT, outline=PAPER)
            pen.text((EDGE + px - 3, y + py - 6), num,
                     font=set_.font(SANS_BOLD, 10), fill=(255, 255, 255))
            if not label:
                continue
            label_w = set_.width(label, SANS_BOLD, 9)
            lx = EDGE + px + 11
            if lx + label_w > EDGE + map_w - 6:
                lx = EDGE + px - 11 - label_w
            pen.text((lx, y + py - 5), label,
                     font=set_.font(SANS_BOLD, 9), fill=INK)
        key = "1 Lima  2 New York  3 Kyiv  4 Warsaw  5 Shenzhen  6 The Hague  7 Riyadh  8 Wellington"
        pen.text((EDGE + 10, y + map_h - 14), key,
                 font=set_.font(SANS, 9), fill=SOFT_INK)

        vx = EDGE + map_w + 12
        vw = INNER_W - map_w - 12
        pen.rectangle([vx, y, vx + vw, y + map_h], fill=(22, 22, 22))
        pen.text((vx + 12, y + 8), "THE DAY IN ONE LINE",
                 font=set_.font(SANS_BOLD, 10), fill=(232, 200, 120))
        verdict = ("A trembling earth, a tumbling market and missiles over "
                   "a NATO border - one Friday that shook three continents.")
        for i, line in enumerate(set_.wrap(verdict, SERIF, 12, vw - 24)):
            pen.text((vx + 12, y + 26 + i * 16), line,
                     font=set_.font(SERIF, 12), fill=(247, 243, 234))
        pen.text((vx + 12, y + map_h - 18),
                 "Watch tomorrow: COP31 draft, Poland-NATO talks, Wall St open.",
                 font=set_.font(SANS, 9), fill=(200, 200, 200))
        return y + map_h + 10

    # -- markets -------------------------------------------------------
    def paint_markets(self, y: int) -> int:
        pen, set_ = self.pen, self.set
        pen.text((EDGE, y), "MARKETS  -  FRIDAY'S CLOSE",
                 font=set_.font(SANS_BOLD, 11), fill=INK)
        cell_w = INNER_W // len(MARKET_ROWS)
        for idx, (name, value, change, delta) in enumerate(MARKET_ROWS):
            x = EDGE + idx * cell_w
            pen.rectangle([x + 2, y + 16, x + cell_w - 2, y + 52], fill=CARD,
                          outline=FAINT)
            pen.text((x + 10, y + 21), name,
                     font=set_.font(SANS_BOLD, 10), fill=SOFT_INK)
            pen.text((x + 10, y + 34), f"{value}  {change}",
                     font=set_.font(SANS_BOLD, 11),
                     fill=ACCENT if delta < 0 else (46, 110, 58))
        return y + 58

    # -- date check + sources ------------------------------------------
    def paint_datecheck(self, y: int) -> int:
        pen, set_ = self.pen, self.set
        pen.rectangle([EDGE, y, CANVAS_W - EDGE, y + 46], fill=SAND,
                      outline=FAINT)
        pen.text((EDGE + 10, y + 6), "DATE CHECK - LEFT OFF ON PURPOSE",
                 font=set_.font(SANS_BOLD, 10), fill=ACCENT)
        for i, item in enumerate(LEFT_OFF):
            pen.text((EDGE + 10, y + 20 + i * 9), "- " + item,
                     font=set_.font(SANS, 9), fill=SOFT_INK)
        return y + 54

    def paint_footer(self, y: int) -> None:
        pen, set_ = self.pen, self.set
        draw_rule(pen, EDGE, y, CANVAS_W - EDGE, 2)
        foot = ("Sources, 21 Nov 2026 03:30 UTC: Reuters, AP, IANS, "
                "InvestingLive, USGS / Peru IGP, ICJ, EU Council, UKMTO. "
                "30 stories. One image, one day.")
        pen.text((EDGE, y + 6), foot, font=set_.font(SANS, 9),
                 fill=SOFT_INK)

    # -- assemble ------------------------------------------------------
    def build(self) -> Image.Image:
        self.paint_masthead()
        y = self.paint_statband(140)
        y = self.paint_leads(y)
        y = self.paint_timeline(y + 4)
        y = self.paint_grid(y + 4)
        y = self.paint_map_and_verdict(y + 6)
        y = self.paint_markets(y)
        y = self.paint_datecheck(y)
        self.paint_footer(y)
        return self.sheet


def main() -> None:
    here = os.path.dirname(os.path.abspath(__file__))
    target = os.path.join(here, "entry.png")
    page = FrontPage()
    image = page.build()
    image.save(target, format="PNG", optimize=True)
    print(f"wrote {target} ({image.size[0]}x{image.size[1]})")


if __name__ == "__main__":
    main()
