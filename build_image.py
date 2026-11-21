#!/usr/bin/env python3
"""Draw "The World in One Day" -- Saturday 21 November 2026.

A one-page newspaper front page summing up the day's world news in a
single 1024x1024 image. Deterministic: same bytes on every run, no
network, no timestamps, no randomness. Run: python3 build_image.py
writes entry.png next to this file.
"""
import math
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

PAPER = (253, 252, 248)
INK = (17, 17, 17)
MUTED = (90, 88, 82)
RED = (178, 28, 28)
NAVY = (26, 48, 80)
TEAL = (14, 94, 98)
GOLD = (168, 124, 18)
LINE = (200, 196, 188)
CARD_BG = (255, 255, 255)
TAG_BG = (238, 234, 226)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


F_SERIF = lambda s: font("DejaVuSerif-Bold.ttf", s)  # noqa: E731
F_SANS = lambda s: font("DejaVuSans.ttf", s)  # noqa: E731
F_BOLD = lambda s: font("DejaVuSans-Bold.ttf", s)  # noqa: E731


def wrap(draw, text, fnt, width):
    """Greedy word wrap by pixel width; returns list of lines."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, fnt, width, fill=INK, leading=None):
    """Draw wrapped paragraph; returns y after the last line."""
    lh = leading or int(fnt.size * 1.28)
    for line in wrap(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += lh
    return y


def tag(draw, x, y, label):
    """Small REPORTED / CLAIM / FORECAST tag; returns width used."""
    fnt = F_BOLD(8)
    tw = draw.textlength(label, font=fnt)
    pad = 4
    draw.rounded_rectangle([x, y, x + tw + pad * 2, y + 12], radius=2,
                           fill=TAG_BG, outline=LINE)
    draw.text((x + pad, y + 2), label, font=fnt, fill=MUTED)
    return int(tw + pad * 2 + 5)


# ---------------------------------------------------------------- stories
# (kicker, headline, body, tag, region)
HEROES = [
    ("POLAND - NATO",
     "Russian missiles land in Poland",
     "Two missiles and a suspected drone came down in Poland as Russia "
     "bombed Ukraine. Tusk calls it an intentional provocation; NATO "
     "calls it a grave violation. No one was hurt.",
     "REPORTED", "EUROPE"),
    ("MARKETS - THE ROUT",
     "Wall Street enters correction as AI rout deepens",
     "S&P 500 -3.7% to 6,910.39, Nasdaq -5.28%. Nvidia -14% as Reuters "
     "reports the SEC is examining its accounting; Anthropic -10% a day "
     "after its debut.",
     "REPORTED", "WORLDWIDE"),
    ("ODISHA - CYCLONE AKVAN",
     "Cyclone Akvan crosses the Odisha coast",
     "Landfall near Gopalpur with winds of 70-80 km/h. 300,000+ "
     "evacuated; no major damage or deaths so far. The storm weakens to "
     "a deep depression.",
     "REPORTED", "ASIA-PACIFIC"),
]

CARDS = [
    ("KYIV", "Eight killed as Russia pounds Kyiv overnight",
     "Zelenskyy says eight died in the overnight bombardment; a strike "
     "on Kryvyi Rih kills 2 and hurts 42.",
     "REPORTED", "EUROPE"),
    ("WASHINGTON - UKRAINE", "Trump wants a Ukraine deal by January",
     "The FT reports the White House told Kyiv and Europe it wants a "
     "peace deal by early January, before Democrats take Congress. Trump "
     "calls the Poland strike a 'mistake'.",
     "REPORTED", "EUROPE"),
    ("GAMES", "GTA 6 banks $3.79bn in its first day",
     "Rockstar says the game took $3.79bn in retail sales in 24 hours, "
     "the biggest entertainment launch ever.",
     "REPORTED", "WORLDWIDE"),
    ("CYBER - BANKS", "JPMorgan, Visa, Mastercard hit in vendor breach",
     "An extortion gang claims customer data from third-party vendors; "
     "16,000+ JPMorgan emails in files Reuters reviewed. No payment "
     "data exposed, the firms say.",
     "REPORTED", "AMERICAS"),
    ("INDIA - MARKETS", "NSE now the world's 5th-largest listed exchange",
     "At $59.7bn, India's NSE overtakes Nasdaq and Hong Kong's HKEX by "
     "market value.",
     "REPORTED", "ASIA-PACIFIC"),
    ("WELLINGTON - CRICKET", "India fight back after Nicholls' 175 not out",
     "New Zealand make 368; India reply with 159/1 at stumps on Day 2. "
     "Jaiswal 85, Rahul 52 not out; a first century opening stand in 17 "
     "Tests.",
     "REPORTED", "ASIA-PACIFIC"),
    ("US - BIG TECH", "YouTube nears a $3bn settlement with schools",
     "An agreement in principle would pay thousands of US school "
     "districts that sued over addictive design. A court must still "
     "approve it.",
     "REPORTED", "AMERICAS"),
    ("INDONESIA - FIRES", "Indonesia's fires may cost $30bn",
     "Research puts the economic losses from this year's fires near "
     "$30bn; the EU's Copernicus service calls the emissions the "
     "third-highest on record.",
     "REPORTED", "ASIA-PACIFIC"),
    ("BRUSSELS", "EU adopts EUR 1bn in military aid for Ukraine",
     "The Council backs joint equipment buying through the European "
     "Peace Facility, with delivery by the end of 2027.",
     "REPORTED", "EUROPE"),
    ("LONDON", "UK pledges 1,000+ drones for Ukraine",
     "Britain pledges more than 1,000 drones for Ukraine in a GBP 260m "
     "package.",
     "REPORTED", "EUROPE"),
    ("STRAIT OF HORMUZ", "Tankers hit mines near Hormuz; two catch fire",
     "Iran's army says two oil tankers caught fire after hitting naval "
     "mines east of the strait. A UK warning reports a tanker strike "
     "and fire off Khasab.",
     "CLAIM", "MIDDLE EAST"),
    ("TURIN - TENNIS", "Medvedev beats Tiafoe at the ATP Finals",
     "Daniil Medvedev wins 6-3, 6-4 in Turin.",
     "REPORTED", "EUROPE"),
]

TIMELINE = [
    ("02:30 UTC", "Akvan landfall begins near Gopalpur", "IMD"),
    ("05:30 UTC", "Russian missile crosses into Poland", "Poland"),
    ("08:54 UTC", "Akvan weakens to deep depression", "IMD"),
    ("13:49 UTC", "Tusk: Poland strike was 'intentional provocation'", "Poland PM"),
    ("16:36 UTC", "FT: White House wants Ukraine deal by January", "FT"),
    ("21:00 UTC", "Wall Street closes: S&P -3.7%, Nasdaq -5.28%", "Markets"),
    ("23:00 local", "Kryvyi Rih strike: 2 dead, 42 hurt", "Vilkul"),
]

STATS = [
    ("-3.70%", "S&P 500 on Friday"),
    ("-5.28%", "Nasdaq on Friday"),
    ("-14%", "Nvidia, on SEC probe report"),
    ("$3.79bn", "GTA 6 in 24 hours"),
    ("300,000+", "evacuated ahead of Akvan"),
    ("209 mm", "rain at Patrapur, 24h"),
    ("$59.7bn", "NSE market value"),
    ("16,000+", "JPMorgan emails leaked"),
]

ALSO = [
    ("NEPAL", "PM Balendra Shah to visit India Nov 22-23.", "REPORTED", "ASIA-PACIFIC"),
    ("FRANCE", "Fourth weekend of cost-of-living protests.", "REPORTED", "EUROPE"),
    ("COP31", "Climate talks enter their final stage in Turkey.", "REPORTED", "WORLDWIDE"),
    ("WASHINGTON", "US adds four Iranians to OFAC sanctions list.", "REPORTED", "AMERICAS"),
    ("RIYADH", "Saudi coalition intercepts Houthi drones over Riyadh.", "REPORTED", "MIDDLE EAST"),
    ("WASHINGTON", "Trump: nuclear arms limits with China, Russia 'very hard'.", "REPORTED", "AMERICAS"),
    ("KERCH", "Kerch Bridge roadway severed, satellite images show.", "REPORTED", "EUROPE"),
    ("WASHINGTON", "SEC proposes direct control of market surveillance.", "REPORTED", "AMERICAS"),
    ("NEW JERSEY", "Ford, Honda, Stellantis, VW sue over state law.", "REPORTED", "AMERICAS"),
    ("TECH", "Databricks in talks to raise billions.", "REPORTED", "AMERICAS"),
    ("WASHINGTON", "White House fires cyber chief Cairncross.", "REPORTED", "AMERICAS"),
    ("NEW YORK", "Indian man jailed 19 years over Sikh murder plot.", "REPORTED", "AMERICAS"),
    ("TECH", "Anthropic IPO closes: 1.127bn shares at $83.", "REPORTED", "AMERICAS"),
    ("LOS ANGELES", "Hyundai unveils the 2027 Elantra at the auto show.", "REPORTED", "AMERICAS"),
    ("MUMBAI", "Sensex rallies nearly 898 points.", "REPORTED", "ASIA-PACIFIC"),
    ("KUNO", "Cheetah gives birth to four cubs at Kuno.", "REPORTED", "ASIA-PACIFIC"),
    ("DELHI", "Pakistan climate minister arrives for SCO forum.", "REPORTED", "ASIA-PACIFIC"),
    ("KUALA LUMPUR", "Malaysia plans to resettle 10,000 Rohingya in Turkiye.", "REPORTED", "ASIA-PACIFIC"),
]

# ---------------------------------------------------------------- drawing
def draw_icon(draw, x, y, kind, color):
    """52x52 pictogram tile; simple geometric glyphs, no text art."""
    draw.rounded_rectangle([x, y, x + 52, y + 52], radius=6, fill=color)
    cx, cy = x + 26, y + 26
    white = (255, 255, 255)
    if kind == "blast":
        for ang in range(0, 360, 45):
            r2 = 20
            a = math.radians(ang)
            draw.line([cx, cy, cx + r2 * math.cos(a), cy + r2 * math.sin(a)],
                      fill=white, width=3)
        draw.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=white)
    elif kind == "talks":
        draw.ellipse([x + 10, y + 14, x + 28, y + 30], outline=white, width=3)
        draw.ellipse([x + 26, y + 22, x + 44, y + 38], outline=white, width=3)
    elif kind == "star":  # GTA VI
        draw.text((x + 13, y + 12), "VI", font=F_BOLD(22), fill=white)
        draw.polygon([(cx, y + 38), (cx + 3, y + 44), (cx - 3, y + 44)], fill=white)
    elif kind == "lock":  # data breach
        draw.arc([x + 17, y + 12, x + 35, y + 28], 180, 360, fill=white, width=3)
        draw.rounded_rectangle([x + 12, y + 24, x + 40, y + 42], radius=3,
                               outline=white, width=3)
        draw.ellipse([cx - 3, cy + 2, cx + 3, cy + 8], fill=white)
    elif kind == "chart":  # NSE
        for bx, bh in ((12, 12), (22, 20), (32, 30)):
            draw.rectangle([x + bx, y + 42 - bh, x + bx + 7, y + 42],
                           fill=white)
        draw.line([x + 10, y + 14, x + 42, y + 12], fill=white, width=2)
    elif kind == "cricket":
        draw.line([x + 12, y + 40, x + 30, y + 14], fill=white, width=4)
        draw.ellipse([x + 34, y + 12, x + 44, y + 22], fill=white)
        for bx in (14, 24, 34):
            draw.line([x + bx, y + 38, x + bx, y + 46], fill=white, width=2)
    elif kind == "play":  # YouTube
        draw.rounded_rectangle([x + 9, y + 14, x + 43, y + 38], radius=5,
                               outline=white, width=3)
        draw.polygon([(x + 21, y + 20), (x + 21, y + 32), (x + 34, y + 26)],
                     fill=white)
    elif kind == "flame":  # Indonesia fires
        draw.polygon([(cx, y + 10), (x + 36, y + 26), (x + 40, y + 36),
                      (cx, y + 44), (x + 12, y + 36), (x + 16, y + 26)],
                     fill=white)
        draw.ellipse([cx - 5, cy + 4, cx + 5, cy + 14], fill=color)
    elif kind == "deal":  # EU aid
        draw.arc([x + 10, y + 16, x + 30, y + 36], 90, 270, fill=white, width=3)
        draw.arc([x + 22, y + 16, x + 42, y + 36], 270, 90, fill=white, width=3)
        draw.line([x + 14, y + 38, x + 38, y + 38], fill=white, width=2)
    elif kind == "drone":
        for px, py in ((14, 14), (38, 14), (14, 38), (38, 38)):
            draw.ellipse([x + px - 5, y + py - 5, x + px + 5, y + py + 5],
                         outline=white, width=2)
        draw.line([x + 14, y + 14, x + 38, y + 38], fill=white, width=2)
        draw.line([x + 38, y + 14, x + 14, y + 38], fill=white, width=2)
        draw.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=white)
    elif kind == "ship":  # Hormuz tanker
        draw.polygon([(x + 8, y + 28), (x + 44, y + 28), (x + 38, y + 40),
                      (x + 14, y + 40)], fill=white)
        draw.rectangle([x + 30, y + 14, x + 38, y + 28], fill=white)
        draw.line([x + 8, y + 45, x + 44, y + 45], fill=white, width=2)
    elif kind == "ball":  # tennis
        draw.ellipse([cx - 13, cy - 13, cx + 13, cy + 13], outline=white, width=3)
        draw.arc([cx - 13, cy - 13, cx + 13, cy + 13], 300, 60, fill=white, width=2)
        draw.arc([cx - 13, cy - 13, cx + 13, cy + 13], 120, 240, fill=white, width=2)
    else:  # "ai" fallback
        draw.text((x + 11, y + 13), "AI", font=F_BOLD(22), fill=white)


ICON_KIND = ["blast", "talks", "star", "lock", "chart", "cricket",
             "play", "flame", "deal", "drone", "ship", "ball"]
ICON_COLORS = [RED, NAVY, (90, 40, 90), NAVY, (30, 90, 40), (20, 90, 120),
               RED, (180, 60, 10), NAVY, (40, 40, 90), (20, 90, 120), TEAL]


def draw_hero_art(draw, x, y, w, h, which):
    """Flat illustration panel for a hero story."""
    if which == 0:  # Russian missiles land in Poland
        draw.rectangle([x, y, x + w, y + h], fill=NAVY)
        draw.ellipse([x + 18, y + 14, x + 62, y + 58], fill=RED,
                     outline=(255, 255, 255), width=2)
        draw.text((x + 30, y + 24), "!", font=F_BOLD(26), fill=(255, 255, 255))
        draw.text((x + 74, y + 16), "KH-101", font=F_BOLD(30),
                  fill=(255, 255, 255))
        draw.text((x + 74, y + 48), "3 OBJECTS CROSSED", font=F_BOLD(12),
                  fill=(255, 214, 130))
        draw.line([x + 16, y + 74, x + w - 16, y + 74], fill=(120, 140, 170), width=1)
        draw.text((x + 16, y + 80), "NO ONE HURT  ·  NATO: GRAVE VIOLATION",
                  font=F_BOLD(10), fill=(200, 215, 235))
    elif which == 1:  # Wall Street correction
        draw.rectangle([x, y, x + w, y + h], fill=(40, 22, 22))
        pts = [(x + 16, y + 22), (x + 70, y + 30), (x + 120, y + 26),
               (x + 175, y + 52), (x + 230, y + 48), (x + 290, y + 80)]
        draw.line(pts, fill=(255, 90, 90), width=4, joint="curve")
        draw.polygon([(x + 290, y + 80), (x + 272, y + 72), (x + 284, y + 60)],
                     fill=(255, 90, 90))
        draw.text((x + 16, y + 84), "S&P -3.7%  ·  NASDAQ -5.28%  ·  NVIDIA -14%",
                  font=F_BOLD(10), fill=(255, 200, 200))
    else:  # Cyclone Akvan
        draw.rectangle([x, y, x + w, y + h], fill=TEAL)
        cx, cy = x + 70, y + 48
        for r in (12, 22, 32):
            draw.arc([cx - r, cy - r, cx + r, cy + r], 20, 300,
                     fill=(255, 255, 255), width=4)
        draw.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=(255, 255, 255))
        for i, yy in enumerate((26, 42, 58)):
            x0 = x + 168 + i * 6
            draw.line([(x0, y + yy), (x0 + 26, y + yy - 6), (x0 + 52, y + yy)],
                      fill=(180, 225, 225), width=3, joint="curve")
        draw.text((x + 168, y + 66), "70-80 KM/H", font=F_BOLD(15),
                  fill=(255, 255, 255))
        draw.text((x + 16, y + 84), "LANDFALL NEAR GOPALPUR, ODISHA",
                  font=F_BOLD(10), fill=(200, 235, 235))


# Coarse continent outlines (lon, lat), schematic map only.
CONTINENTS = [
    [(-168, 66), (-140, 70), (-125, 72), (-110, 73), (-95, 80), (-85, 70),
     (-75, 62), (-65, 60), (-55, 52), (-60, 47), (-70, 44), (-75, 38),
     (-80, 32), (-85, 28), (-90, 21), (-97, 16), (-105, 20), (-115, 28),
     (-125, 40), (-125, 49), (-140, 60), (-155, 58), (-165, 60)],
    [(-80, 10), (-75, 11), (-62, 10), (-52, 5), (-50, -5), (-35, -8),
     (-40, -20), (-48, -28), (-58, -38), (-65, -45), (-70, -52), (-73, -45),
     (-72, -30), (-78, -15), (-80, -5)],
    [(-18, 15), (-10, 30), (0, 36), (10, 37), (20, 32), (30, 31), (35, 28),
     (43, 12), (51, 11), (48, 0), (40, -10), (35, -20), (30, -30), (20, -35),
     (15, -27), (12, -18), (12, -5), (8, 4), (-8, 5), (-15, 11)],
    [(-10, 36), (-9, 43), (-2, 48), (0, 50), (5, 53), (8, 57), (10, 59),
     (18, 56), (21, 55), (24, 59), (30, 60), (28, 65), (25, 70), (18, 70),
     (12, 65), (5, 60), (-5, 50), (-9, 43)],
    [(30, 60), (40, 68), (55, 70), (70, 72), (90, 75), (110, 76), (130, 72),
     (150, 70), (170, 66), (178, 65), (170, 60), (160, 55), (142, 50),
     (140, 40), (130, 33), (122, 30), (110, 20), (105, 10), (100, 5),
     (95, 15), (90, 22), (85, 20), (80, 8), (75, 12), (70, 20), (60, 25),
     (52, 28), (45, 30), (40, 36), (35, 36), (30, 42)],
    [(113, -22), (114, -30), (120, -34), (130, -32), (140, -38), (147, -39),
     (153, -32), (150, -22), (146, -19), (142, -11), (136, -12), (130, -13),
     (122, -14), (114, -21)],
]

PINS = [
    (1, 22.9, 50.3, "Nowy Lipowiec"),
    (2, 30.5, 50.4, "Kyiv"),
    (3, 84.9, 19.3, "Gopalpur"),
    (4, 33.4, 47.9, "Kryvyi Rih"),
    (5, 174.8, -41.3, "Wellington"),
    (6, 56.2, 26.2, "Khasab"),
]


def draw_map(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(232, 240, 244),
                   outline=LINE)
    for poly in CONTINENTS:
        pts = [(x + (lon + 180) / 360 * w, y + (90 - lat) / 180 * h)
               for lon, lat in poly]
        draw.polygon(pts, fill=(190, 200, 195), outline=(120, 130, 125))
    for num, lon, lat, name in PINS:
        px = x + (lon + 180) / 360 * w
        py = y + (90 - lat) / 180 * h
        draw.ellipse([px - 8, py - 8, px + 8, py + 8], fill=RED,
                     outline=(255, 255, 255), width=2)
        draw.text((px - 3, py - 6), str(num), font=F_BOLD(9),
                  fill=(255, 255, 255))
    return y + h

# ---------------------------------------------------------------- layout
def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 8  # margin

    # Top rule + date-forward masthead: the date IS the headline.
    d.rectangle([0, 0, W, 6], fill=INK)
    d.text((M, 10), "THE WORLD IN ONE DAY", font=F_SERIF(15), fill=RED)
    d.text((M, 30), "Saturday 21 November 2026", font=F_SERIF(44), fill=INK)
    d.rectangle([W - 218, 10, W - M, 72], outline=INK, width=2)
    d.text((W - 208, 13), "MAKE.FUN", font=F_BOLD(14), fill=RED)
    d.text((W - 208, 31), "NEWS-IMAGE-20261121", font=F_BOLD(11), fill=INK)
    d.text((W - 208, 47), "DAY 325 OF 2026", font=F_SANS(10), fill=MUTED)

    # Red subhead: the 3 biggest stories
    sub = ("RUSSIAN MISSILES LAND IN POLAND  ·  WALL STREET ENTERS "
           "CORRECTION  ·  CYCLONE AKVAN CROSSES ODISHA")
    d.text((M, 82), sub, font=F_BOLD(12), fill=RED)

    # Story-count banner
    regions = {}
    for _, _, _, _, reg in HEROES + CARDS:
        regions[reg] = regions.get(reg, 0) + 1
    for _, _, _, reg in ALSO:
        regions[reg] = regions.get(reg, 0) + 1
    total = 3 + 12 + len(ALSO)
    order = ["ASIA-PACIFIC", "EUROPE", "MIDDLE EAST", "AMERICAS",
             "AFRICA", "WORLDWIDE"]
    parts = [f"{r} {regions.get(r, 0)}" for r in order if regions.get(r, 0)]
    d.rectangle([M, 102, W - M, 124], fill=NAVY)
    d.text((M + 10, 108), f"{total} STORIES FROM {len(parts)} REGIONS",
           font=F_BOLD(13), fill=(255, 255, 255))
    d.text((W - M - 10 - d.textlength("  ·  ".join(parts), font=F_SANS(11)),
            109), "  ·  ".join(parts), font=F_SANS(11), fill=(200, 215, 235))

    # Stat strip: 8 numbers
    y0, y1 = 130, 174
    bw = (W - 2 * M - 7 * 6) / 8
    for i, (num, label) in enumerate(STATS):
        bx = M + i * (bw + 6)
        d.rectangle([bx, y0, bx + bw, y1], outline=LINE, fill=CARD_BG)
        d.text((bx + 6, y0 + 5), num, font=F_BOLD(15), fill=RED)
        para(d, bx + 6, y0 + 24, label, F_SANS(8), bw - 12, fill=MUTED,
             leading=10)

    # Day by hours
    d.text((M, 180), "THE DAY BY HOURS", font=F_BOLD(12), fill=INK)
    d.line([M, 196, W - M, 196], fill=LINE, width=1)
    cw = (W - 2 * M) / 7
    for i, (t, what, src) in enumerate(TIMELINE):
        cx = M + i * cw
        d.text((cx + 2, 201), t, font=F_BOLD(9), fill=RED)
        para(d, cx + 2, 213, what, F_SANS(9), cw - 8, leading=11)
        if i:
            d.line([cx, 200, cx, 242], fill=LINE, width=1)
    d.line([M, 246, W - M, 246], fill=INK, width=2)

    # Heroes: 3 columns
    hy, hh = 254, 172
    hw = (W - 2 * M - 2 * 8) / 3
    for i, (kicker, head, body, tg, reg) in enumerate(HEROES):
        hx = M + i * (hw + 8)
        draw_hero_art(d, hx, hy, hw, 96, i)
        yy = hy + 104
        d.text((hx, yy), kicker, font=F_BOLD(9), fill=RED)
        tagw = tag(d, hx + hw - 66, yy - 1, tg)
        yy = para(d, hx, yy + 13, head, F_BOLD(14), hw, leading=15)
        para(d, hx, yy + 2, body, F_SANS(10), hw, leading=11)

    # Secondary cards: 3 cols x 4 rows
    cy0 = 438
    ch = 78
    for idx, (kicker, head, body, tg, reg) in enumerate(CARDS):
        row, col = divmod(idx, 3)
        cx = M + col * (hw + 8)
        cy = cy0 + row * (ch + 2)
        d.rectangle([cx, cy, cx + hw, cy + ch], outline=LINE, fill=CARD_BG)
        draw_icon(d, cx + 6, cy + 6, ICON_KIND[idx], ICON_COLORS[idx])
        tx = cx + 64
        d.text((tx, cy + 5), kicker, font=F_BOLD(8), fill=RED)
        yy = para(d, tx, cy + 17, head, F_BOLD(11), hw - 70, leading=13)
        para(d, tx, yy, body, F_SANS(9), hw - 70, leading=11)
        tag(d, cx + 6, cy + ch - 15, tg)

    # Bottom band
    by0 = 762
    d.line([M, by0 - 6, W - M, by0 - 6], fill=INK, width=2)

    # Map (left)
    mw = 296
    d.text((M, by0), "WHERE IT HAPPENED", font=F_BOLD(11), fill=INK)
    draw_map(d, M, by0 + 18, mw, 148)
    d.text((M, by0 + 170), "1 Nowy Lipowiec  2 Kyiv  3 Gopalpur",
           font=F_SANS(9), fill=MUTED)
    d.text((M, by0 + 182), "4 Kryvyi Rih  5 Wellington  6 Khasab",
           font=F_SANS(9), fill=MUTED)

    # Also on this page (middle, two columns)
    ax = M + mw + 12
    aw = 348
    d.text((ax, by0), "ALSO ON THIS PAGE", font=F_BOLD(11), fill=INK)
    col_w = (aw - 8) / 2
    for j, (kicker, text, tg, reg) in enumerate(ALSO):
        col, row = divmod(j, 9)
        xx = ax + col * (col_w + 8)
        yy = by0 + 16 + row * 21
        kfnt, tfnt = F_BOLD(8), F_SANS(8)
        prefix = f"{kicker} - "
        pw = d.textlength(prefix, font=kfnt)
        words = text.split()
        line1_words = []
        cur = ""
        for w_ in words:
            trial = (cur + " " + w_).strip()
            if d.textlength(trial, font=tfnt) <= col_w - pw or not cur:
                cur = trial
                line1_words.append(w_)
            else:
                break
        line1 = cur
        line2 = " ".join(words[len(line1_words):])
        if d.textlength(line2, font=tfnt) > col_w:
            while line2 and d.textlength(line2 + "...", font=tfnt) > col_w:
                line2 = line2.rsplit(" ", 1)[0]
            line2 += "..."
            print(f"WARNING truncated ALSO item: {kicker}")
        d.text((xx, yy), prefix, font=kfnt, fill=RED)
        d.text((xx + pw, yy), line1, font=tfnt, fill=INK)
        if line2:
            d.text((xx, yy + 9), line2, font=tfnt, fill=INK)

    # Verdict + markets (right)
    rx = ax + aw + 12
    rw = W - M - rx
    d.rectangle([rx, by0, rx + rw, by0 + 96], outline=INK, width=2,
                fill=(255, 248, 235))
    d.text((rx + 8, by0 + 6), "THE VERDICT", font=F_BOLD(11), fill=RED)
    para(d, rx + 8, by0 + 22,
         "Poland takes the day's top story: Russian missiles on NATO "
         "soil, called a provocation. Wall Street slides into correction "
         "as the AI trade unwinds; Akvan spares Odisha the worst.",
         F_SANS(10), rw - 16, leading=12)
    my = by0 + 104
    d.rectangle([rx, my, rx + rw, by0 + 196], outline=LINE, fill=CARD_BG)
    d.text((rx + 8, my + 6), "MARKETS & MONEY", font=F_BOLD(11), fill=INK)
    para(d, rx + 8, my + 22,
         "S&P 500 6,910.39 (-3.70%) - Nasdaq -5.28% - Dow in correction - "
         "Nvidia -14% - Anthropic -10% - Bitcoin under $60,000 - NSE "
         "$59.7bn, now 5th largest - Sensex +898",
         F_SANS(10), rw - 16, leading=12)

    # Footer: date check + sources
    fy = 968
    d.line([M, fy, W - M, fy], fill=INK, width=2)
    d.text((M, fy + 4), "DATE CHECK - LEFT OFF, NOT 21 NOVEMBER:",
           font=F_BOLD(9), fill=RED)
    para(d, M, fy + 16,
         "Eisenkot gets mandate to form Israel's government (7-8 Nov) - "
         "Four nations urge Israel on Gaza aid (15-16 Nov) - ICJ Myanmar "
         "genocide ruling (19 Nov) - Shenzhen trilateral summit, no deal "
         "(19 Nov) - Senate rejects Iran war-powers resolution 51-48 "
         "(19 Nov) - Anthropic IPO priced at $83 (18 Nov) - US-Venezuela "
         "military deal (18 Nov).",
         F_SANS(9), W - 2 * M, leading=10)
    d.text((M, 1006),
           "HOW SURE ARE WE?  REPORTED = confirmed by named sources  ·  "
           "CLAIM = one side says, unverified  ·  FORECAST = schedule or "
           "projection.",
           font=F_SANS(8), fill=MUTED)
    d.text((M, 1015),
           "Stories as reported by Saturday morning, 21 November 2026. "
           "Disputed claims are attributed, not stated as fact. Sources: "
           "Reuters, AP, FT, BBC, IMD, PTI, ANI, Cricbuzz, Bloomberg, "
           "Copernicus.",
           font=F_SANS(8), fill=MUTED)

    img.save(OUT, optimize=True)
    print(f"wrote {OUT} ({os.path.getsize(OUT)} bytes)")


if __name__ == "__main__":
    build()
