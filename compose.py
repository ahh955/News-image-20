#!/usr/bin/env python3
"""Build entry.png: one-page front page, Friday 20 November 2026 world news.
Deterministic: fixed palette, fixed fonts, no network, no randomness, no time.
Run: python3 compose.py  ->  entry.png (1024x1024, PNG, <1 MiB)
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
FD = "/usr/share/fonts/truetype/dejavu/"
def F(name, size):
    return ImageFont.truetype(FD + name, size)
SERIF_B = lambda s: F("DejaVuSerif-Bold.ttf", s)
SANS = lambda s: F("DejaVuSans.ttf", s)
SANS_B = lambda s: F("DejaVuSans-Bold.ttf", s)

INK = (18, 18, 18)
PAPER = (252, 250, 244)
NAVY = (16, 34, 64)
RED = (178, 24, 24)
GREY = (90, 90, 90)
LINE = (200, 196, 186)

def wrap(draw, text, font, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=font) <= width:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def center(draw, y, text, font, fill=INK, cx=W // 2):
    draw.text((cx - draw.textlength(text, font=font) / 2, y), text, font=font, fill=fill)

def art(draw, box, kind):
    """Flat procedural illustration for one story."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    pal = {
        "barrage": ((20, 26, 48), (255, 176, 32), (255, 90, 40)),
        "cyclone": ((14, 74, 110), (255, 255, 255), (140, 210, 240)),
        "market": ((122, 18, 18), (255, 255, 255), (255, 200, 60)),
        "deal": ((18, 60, 110), (255, 210, 40), (255, 255, 255)),
        "climate": ((24, 96, 60), (255, 220, 60), (255, 255, 255)),
        "inflation": ((90, 30, 90), (255, 255, 255), (255, 190, 60)),
        "missile": ((70, 90, 60), (220, 220, 220), (255, 120, 40)),
        "strike": ((160, 40, 40), (255, 255, 255), (30, 30, 30)),
        "election": ((20, 80, 140), (255, 255, 255), (255, 200, 40)),
        "cricket": ((30, 110, 50), (255, 255, 255), (255, 220, 80)),
        "space": ((10, 10, 40), (200, 200, 220), (255, 150, 60)),
        "tanker": ((10, 60, 90), (255, 255, 255), (255, 140, 40)),
        "oilwell": ((120, 80, 20), (255, 255, 255), (40, 40, 40)),
    }
    bg, c1, c2 = pal[kind]
    draw.rectangle(box, fill=bg)
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    if kind == "barrage":
        for i, bh in enumerate((34, 52, 40, 60, 30)):
            bx = x0 + 8 + i * (w // 5)
            draw.rectangle([bx, y1 - 8 - bh, bx + w // 6, y1 - 8], fill=(50, 55, 80))
            draw.rectangle([bx + 4, y1 - 8 - bh - 6, bx + 8, y1 - 8 - bh], fill=c1)
        for px, py, r in ((cx - 30, y0 + 14, 9), (cx + 34, y0 + 22, 7), (cx + 6, y0 + 34, 6)):
            draw.ellipse([px - r, py - r, px + r, py + r], fill=c1, outline=c2, width=2)
            for dx, dy in ((-14, 0), (14, 0), (0, -12), (0, 12)):
                draw.line([px, py, px + dx, py + dy], fill=c2, width=2)
        draw.line([x0 + 10, y1 - 8, x1 - 10, y1 - 8], fill=c1, width=3)
    elif kind == "cyclone":
        for r in range(34, 6, -7):
            draw.arc([cx - r, cy - r + 4, cx + r, cy + r + 4], start=200 + r * 6,
                     end=200 + r * 6 + 240, fill=c1 if r % 14 else c2, width=4)
        draw.ellipse([cx - 6, cy - 2, cx + 6, cy + 10], fill=c2)
        for i in range(6):
            lx = x0 + 8 + i * (w // 6)
            draw.line([lx, y0 + 6, lx - 4, y0 + 16], fill=c2, width=2)
        draw.rectangle([x0, y1 - 10, x1, y1], fill=(8, 50, 80))
    elif kind == "market":
        draw.line([x0 + 10, y1 - 14, x1 - 8, y1 - 14], fill=c1, width=2)
        draw.line([x0 + 10, y0 + 8, x0 + 10, y1 - 14], fill=c1, width=2)
        pts = [(x0 + 14, y0 + 12), (x0 + w // 3, y0 + 26), (x0 + w // 2, y0 + 20),
               (x0 + 2 * w // 3, y0 + 44), (x1 - 12, y0 + h - 24)]
        draw.line(pts, fill=c2, width=4, joint="curve")
        draw.polygon([(x1 - 12, y0 + h - 24), (x1 - 24, y0 + h - 30), (x1 - 20, y0 + h - 16)], fill=c2)
        for i, bh in enumerate((26, 20, 14, 9)):
            bx = x0 + 22 + i * 16
            draw.rectangle([bx, y1 - 16 - bh, bx + 10, y1 - 16], fill=c1)
    elif kind == "deal":
        draw.rectangle([x0 + 12, y0 + 10, x0 + w // 2 - 4, y1 - 12], fill=(30, 70, 160))
        draw.rectangle([x0 + w // 2 + 4, y0 + 10, x1 - 12, y1 - 12], fill=(20, 40, 120))
        draw.line([x0 + 12, y0 + 10, x0 + w // 2 - 4, y1 - 12], fill=c1, width=3)
        draw.line([x0 + w // 2 - 4, y0 + 10, x0 + 12, y1 - 12], fill=c1, width=3)
        for i in range(8):
            import math
            a = i * 3.14159 / 4
            px = x0 + 3 * w // 4 + int(16 * math.cos(a))
            py = cy + int(14 * math.sin(a))
            draw.ellipse([px - 2, py - 2, px + 2, py + 2], fill=c1)
        draw.ellipse([cx - 12, cy - 12, cx + 12, cy + 12], fill=c1, outline=INK, width=2)
        draw.text((cx - 5, cy - 8), "\u2713", font=SANS_B(14), fill=INK)
    elif kind == "climate":
        draw.ellipse([x0 + 14, y0 + 10, x0 + 54, y0 + 50], fill=c1)
        draw.ellipse([x1 - 62, y0 + 12, x1 - 14, y0 + 60], fill=(60, 160, 220))
        draw.arc([x1 - 62, y0 + 12, x1 - 14, y0 + 60], 20, 160, fill=(40, 120, 60), width=6)
        for i in range(5):
            draw.line([x0 + 20 + i * 10, y1 - 12, x0 + 20 + i * 10, y1 - 12 - (8 + i * 4)],
                      fill=c1, width=5)
    elif kind == "inflation":
        pts = [(x0 + 14, y1 - 20), (x0 + w // 3, y1 - 34), (x0 + w // 2, y1 - 28),
               (x0 + 2 * w // 3, y1 - 48), (x1 - 14, y1 - 56)]
        draw.line(pts, fill=c2, width=4, joint="curve")
        draw.polygon([(x1 - 14, y1 - 56), (x1 - 26, y1 - 52), (x1 - 18, y1 - 44)], fill=c2)
        draw.text((x0 + 36, y0 + 6), "2.3%", font=SANS_B(18), fill=c1)
        draw.text((x0 + 36, y0 + 28), "OCT CPI", font=SANS_B(8), fill=c1)
    elif kind == "missile":
        draw.rectangle([x0, y1 - 18, x1, y1], fill=(50, 70, 40))
        draw.polygon([(cx - 8, y1 - 18), (cx + 8, y1 - 18), (cx + 4, y0 + 14), (cx, y0 + 6),
                      (cx - 4, y0 + 14)], fill=c1)
        for dx in (-26, 26):
            draw.line([cx + dx, y0 + 12, cx + dx - 6, y0 + 30], fill=c2, width=3)
        draw.ellipse([cx - 16, y1 - 26, cx + 16, y1 - 12], fill=c2)
        draw.text((x1 - 52, y0 + 6), "60 km", font=SANS_B(10), fill=c1)
    elif kind == "strike":
        for i in range(4):
            px = x0 + 36 + i * ((w - 48) // 4)
            draw.ellipse([px, y0 + 12, px + 12, y0 + 24], fill=c1)
            draw.rectangle([px + 2, y0 + 26, px + 10, y1 - 16], fill=c1)
        draw.rectangle([x0 + 10, y1 - 22, x1 - 10, y1 - 10], fill=INK)
        draw.text((x0 + 14, y1 - 21), "24H STOP", font=SANS_B(9), fill=c1)
    elif kind == "election":
        draw.rectangle([cx - 26, y0 + 12, cx + 26, y1 - 14], fill=c1)
        draw.rectangle([cx - 18, y0 + 6, cx + 18, y0 + 14], fill=c2)
        draw.text((cx - 8, y0 + 20), "3rd", font=SANS_B(16), fill=INK)
        draw.text((cx - 14, y0 + 40), "TERM", font=SANS_B(8), fill=INK)
        draw.line([x0 + 10, y1 - 10, x1 - 10, y1 - 10], fill=c2, width=3)
    elif kind == "cricket":
        draw.rectangle([x0, y1 - 16, x1, y1], fill=(20, 80, 40))
        draw.line([cx - 30, y1 - 16, cx + 30, y1 - 16], fill=c1, width=3)
        for dx in (-14, 0, 14):
            draw.line([cx + dx, y0 + 34, cx + dx, y1 - 18], fill=c2, width=4)
        draw.ellipse([x1 - 30, y0 + 10, x1 - 14, y0 + 26], fill=RED)
        draw.text((x0 + 34, y0 + 8), "118", font=SANS_B(20), fill=c1)
    elif kind == "space":
        for sx, sy in ((20, 12), (60, 8), (110, 16), (40, 40), (90, 44)):
            draw.ellipse([x0 + sx, y0 + sy, x0 + sx + 3, y0 + sy + 3], fill=c1)
        draw.ellipse([x1 - 52, y0 + 8, x1 - 12, y0 + 48], fill=(180, 160, 140))
        draw.ellipse([x1 - 44, y0 + 16, x1 - 32, y0 + 28], fill=(140, 120, 100))
        draw.rectangle([x0 + 14, cy - 6, x0 + 34, cy + 6], fill=c1)
        draw.polygon([(x0 + 34, cy - 6), (x0 + 46, cy), (x0 + 34, cy + 6)], fill=c2)
        draw.line([x0 + 8, cy - 14, x0 + 8, cy + 14], fill=c2, width=3)
    elif kind == "tanker":
        draw.rectangle([x0, y1 - 20, x1, y1], fill=(20, 90, 140))
        draw.polygon([(x0 + 16, y1 - 20), (x1 - 16, y1 - 20), (x1 - 30, y1 - 38),
                      (x0 + 30, y1 - 38)], fill=(40, 40, 40))
        draw.rectangle([x0 + 44, y1 - 52, x0 + 66, y1 - 38], fill=c1)
        draw.ellipse([x1 - 34, y0 + 8, x1 - 14, y0 + 28], fill=c2)
        draw.text((x0 + 34, y0 + 6), "$92.50", font=SANS_B(13), fill=c1)
    elif kind == "oilwell":
        draw.polygon([(cx - 26, y1 - 12), (cx - 6, y0 + 10), (cx + 6, y0 + 10), (cx + 26, y1 - 12)],
                     outline=c1, width=3)
        draw.line([cx - 30, y0 + 16, cx + 30, y0 + 16], fill=c1, width=4)
        draw.ellipse([cx - 5, y1 - 22, cx + 5, y1 - 8], fill=INK)
        draw.text((x0 + 34, y0 + 6), "1st WELL", font=SANS_B(9), fill=c1)

def story_block(draw, box, num, tag, headline, deck, source, art_kind, head_size=13):
    x0, y0, x1, y1 = box
    draw.rectangle(box, outline=LINE, width=1)
    ah = 88 if head_size >= 14 else 46
    art(draw, (x0 + 1, y0 + 1, x1 - 1, y0 + ah), art_kind)
    draw.rectangle([x0 + 1, y0 + 1, x0 + 30, y0 + 18], fill=RED)
    draw.text((x0 + 6, y0 + 3), str(num), font=SANS_B(11), fill=(255, 255, 255))
    ty = y0 + ah + 4
    draw.text((x0 + 6, ty), tag, font=SANS_B(8), fill=RED)
    ty += 12
    for ln in wrap(draw, headline, SANS_B(head_size), x1 - x0 - 12)[:2]:
        draw.text((x0 + 6, ty), ln, font=SANS_B(head_size), fill=INK)
        ty += head_size + 3
    ty += 1
    for ln in wrap(draw, deck + " (" + source + ")", SANS(8), x1 - x0 - 12)[:3]:
        draw.text((x0 + 6, ty), ln, font=SANS(8), fill=(40, 40, 40))
        ty += 11

def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, 6], fill=INK)
    # --- masthead ---
    center(d, 12, "THE WORLD IN ONE DAY  \u00b7  33 STORIES  \u00b7  7 REGIONS",
           SANS_B(10), fill=RED)
    center(d, 30, "Friday 20 November 2026", SERIF_B(38))
    d.line([14, 76, 300, 76], fill=INK, width=2)
    d.line([724, 76, 1010, 76], fill=INK, width=2)
    center(d, 80, "ONE DAY \u00b7 ONE PAGE \u00b7 EVERY STORY DATED FRIDAY", SANS_B(9), fill=GREY)
    # --- subhead strip ---
    d.rectangle([14, 98, 1010, 120], fill=NAVY)
    center(d, 103, "Kyiv barrage  \u00b7  Akvan makes landfall  \u00b7  Asia markets plunge  \u00b7  UK\u2013EU reset sealed",
           SANS_B(11), fill=(255, 255, 255))
    # --- stat strip ---
    stats = [("300,000+", "EVACUATED, ODISHA"), ("\u22126.2%", "TAIEX IN A DAY"),
             ("100,000", "UK YOUTH VISAS / YR"), ("118", "PHILLIPS v INDIA"),
             ("3", "DNIPRO BRIDGES HIT"), ("$120bn", "COP31 ADAPTATION GAP")]
    sw = (1010 - 14) // 6
    for i, (num, lab) in enumerate(stats):
        x0 = 14 + i * sw
        d.rectangle([x0 + 1, 124, x0 + sw - 1, 152], fill=(235, 232, 222))
        center(d, 127, num, SANS_B(15), fill=RED, cx=x0 + sw // 2)
        center(d, 143, lab, SANS_B(7), fill=GREY, cx=x0 + sw // 2)
    # --- region strip ---
    regions = [("EUROPE", 7, (30, 70, 160)), ("ASIA", 10, (178, 24, 24)),
               ("MIDDLE EAST", 3, (120, 80, 20)), ("AFRICA", 5, (24, 96, 60)),
               ("AMERICAS", 4, (90, 30, 90)), ("OCEANIA", 3, (14, 74, 110)),
               ("GLOBAL", 1, (80, 80, 80))]
    rx, total = 14, sum(n for _, n, _ in regions)
    for ri, (name, n, col) in enumerate(regions):
        rw = int((1010 - 14) * n / total)
        if ri == len(regions) - 1:
            rw = 1010 - rx
        d.rectangle([rx, 156, rx + rw - 1, 172], fill=col)
        lbl = "%s %d" % (name, n)
        lx = rx + 4
        if ri == len(regions) - 1:
            lx = 1010 - d.textlength(lbl, font=SANS_B(8)) - 4
        d.text((lx, 159), lbl, font=SANS_B(8), fill=(255, 255, 255))
        rx += rw
    # --- leads ---
    leads = [
        (1, "KYIV \u00b7 WAR", "barrage",
         "Overnight barrage batters Kyiv as bridges burn",
         "About 110 missiles and 400+ drones strike overnight; three Dnipro bridges hit, 8 killed, power and water cut across the capital.", "Reuters"),
        (2, "ODISHA \u00b7 WEATHER", "cyclone",
         "Cyclone Akvan makes landfall at dawn",
         "Akvan comes ashore near Gopalpur around 8 am with 110 km/h gusts; 300,000+ evacuated, shelters full, no deaths reported.", "IMD"),
        (3, "TAIPEI \u00b7 MARKETS", "market",
         "AI sell-off sweeps Asia in worst week in years",
         "Taiex falls 6.2%, Kospi 5.2% and Nikkei 4.8%; SoftBank drops 16% as AI valuations face their sharpest test since 2020.", "Reuters"),
    ]
    lw = (1010 - 14 - 12) // 3
    for i, (num, tag, kind, head, deck, src) in enumerate(leads):
        x0 = 14 + i * (lw + 6)
        story_block(d, (x0, 178, x0 + lw, 372), num, tag, head, deck, src, kind, 14)
    # --- features ---
    d.rectangle([14, 378, 1010, 394], fill=INK)
    d.text((20, 381), "TEN MORE FROM FRIDAY  \u00b7  STORIES 4\u201313", font=SANS_B(10), fill=(255, 255, 255))
    feats = [
        (4, "LONDON \u00b7 DIPLOMACY", "deal", "UK and EU seal reset deal",
         "Youth mobility of 100,000 visas a year, plus food trade and a carbon link.", "BBC"),
        (5, "ANTALYA \u00b7 CLIMATE", "climate", "COP31 ends with no deal",
         "Final day closes without agreement; draft omits fossil fuels; $120bn gap stands.", "Reuters"),
        (6, "TOKYO \u00b7 ECONOMY", "inflation", "Japan inflation at 2.3%",
         "October core inflation is the fastest this year, keeping rate pressure on.", "Reuters"),
        (7, "WARSAW \u00b7 SECURITY", "missile", "Russian missile lands in Poland",
         "A Kh-101 comes down in a field 60 km inside the border.", "AP"),
        (8, "ROME \u00b7 LABOUR", "strike", "Italy stops for 24-hour strike",
         "CGIL general strike halts trains and schools in a protest over pay and budgets.", "AP"),
        (9, "SAN SALVADOR \u00b7 POLITICS", "election", "Bukele files for third term",
         "President files re-election papers ahead of the vote on 28 February 2027.", "AP"),
        (10, "WELLINGTON \u00b7 SPORT", "cricket", "Phillips smashes 118 v India",
         "First New Zealander with centuries in all 3 formats in one year.", "AP"),
        (11, "MERCURY \u00b7 SPACE", "space", "BepiColombo reaches Mercury",
         "After eight years in flight, the ESA\u2013JAXA probe arrives at the innermost planet.", "ESA"),
        (12, "HORMUZ \u00b7 ENERGY", "tanker", "Tanker attacks lift Brent to $92.50",
         "Attacks near Hormuz leave 46 ships waiting as oil prices climb again.", "Reuters"),
        (13, "TURKANA \u00b7 ENERGY", "oilwell", "Kenya drills its first oil well",
         "Drilling begins in Turkana, a first step for the country's long-planned oil sector.", "Reuters"),
    ]
    fw = (1010 - 14 - 24) // 5
    for i, (num, tag, kind, head, deck, src) in enumerate(feats):
        col, row = i % 5, i // 5
        x0 = 14 + col * (fw + 6)
        y0 = 398 + row * 112
        story_block(d, (x0, y0, x0 + fw, y0 + 108), num, tag, head, deck, src, kind, 11)
    # --- map ---
    d.rectangle([14, 626, 1010, 642], fill=INK)
    d.text((20, 629), "WHERE IT HAPPENED  \u00b7  PINS 1\u201313 MATCH THE STORIES ABOVE", font=SANS_B(10), fill=(255, 255, 255))
    mx0, my0, mx1, my1 = 14, 646, 1010, 730
    d.rectangle([mx0, my0, mx1, my1], fill=(205, 225, 240), outline=LINE)
    def mxy(lon, lat):
        # crop latitude to 75N..-60S so continents fill the short map band
        return (mx0 + (lon + 180) / 360 * (mx1 - mx0),
                my0 + (75 - lat) / 135 * (my1 - my0))
    # rough continent blobs (lon/lat polygons)
    continents = [
        [(-168, 66), (-140, 70), (-110, 68), (-95, 70), (-75, 62), (-60, 50), (-75, 38),
         (-80, 26), (-97, 26), (-105, 22), (-118, 33), (-125, 48), (-150, 60)],
        [(-78, 8), (-60, 5), (-50, -5), (-35, -8), (-40, -22), (-55, -35), (-70, -52),
         (-73, -30), (-77, -12)],
        [(-10, 36), (-9, 43), (-2, 48), (3, 51), (10, 57), (18, 56), (24, 58), (30, 60),
         (32, 50), (28, 45), (20, 40), (12, 44), (3, 43)],
        [(-17, 15), (-10, 30), (10, 37), (30, 31), (43, 12), (51, 11), (40, -5), (35, -20),
         (20, -35), (15, -25), (12, -5), (-8, 5)],
        [(30, 36), (45, 30), (58, 26), (66, 25), (77, 8), (88, 22), (92, 16), (100, 8),
         (105, 10), (110, 20), (122, 30), (130, 33), (140, 36), (142, 50), (160, 60),
         (170, 66), (150, 70), (110, 73), (70, 72), (40, 68), (30, 55)],
        [(114, -22), (122, -14), (132, -12), (142, -11), (150, -23), (153, -28),
         (147, -38), (138, -35), (129, -32), (118, -35)],
    ]
    for poly in continents:
        d.polygon([mxy(lon, lat) for lon, lat in poly], fill=(168, 196, 150),
                  outline=(120, 150, 110))
    pins = [(1, 31, 50), (2, 85, 20), (3, 127, 37), (4, 0, 51), (5, 30, 36),
            (6, 139, 35), (7, 19, 52), (8, 12, 41), (9, -89, 13), (10, 174, -41),
            (11, 8, 49), (12, 56, 26), (13, 36, 3)]
    for num, lon, lat in pins:
        px, py = mxy(lon, lat)
        d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=RED, outline=(255, 255, 255), width=1)
        t = str(num)
        d.text((px - d.textlength(t, font=SANS_B(8)) / 2, py - 6), t,
               font=SANS_B(8), fill=(255, 255, 255))
    # --- briefs ---
    d.rectangle([14, 736, 1010, 752], fill=INK)
    d.text((20, 739), "ALSO ON FRIDAY 20 NOVEMBER  \u00b7  20 MORE STORIES (14\u201333)",
           font=SANS_B(10), fill=(255, 255, 255))
    briefs = [
        "China holds lending rates steady, LPR at 3.0% and 3.5%. (Reuters)",
        "Seoul ruling party moves to impeach the chief justice. (Yonhap)",
        "111 caught cheating in South Korea's Suneung exam. (Yonhap)",
        "Iraqi army enters Jurf al-Sakhar as militia deadline nears. (AP)",
        "Malawi fuel crisis deepens; drivers queue through the night. (Reuters)",
        "Migrant boat capsizes off Yenne, Senegal; 4 dead. (AP)",
        "Sudan drone strike kills 10 at a gold mine. (Reuters)",
        "F1 Las Vegas practice: Russell fastest in the wet. (AP)",
        "California probes Nvidia over China chip sales. (Reuters)",
        "Pancreatic cancer pill shrinks tumours 60.7% in early trial. (AP)",
        "Tonga declares an El Ni\u00f1o drought emergency. (RNZ)",
        "Xi and Albanese hail a turnaround in ties. (Reuters)",
        "Estonia to shut its road border with Russia. (Reuters)",
        "GTA VI sales top $2.3bn \u2014 Friday sales update. (Reuters)",
        "Rohingya camps react to Thursday's ICJ ruling. (AP)",
        "Leaders publish joint declaration after trilateral. (Reuters)",
        "Kospi trading curb triggered amid the sell-off. (Yonhap)",
        "Poland summons Russian envoy over the missile. (Reuters)",
        "Italy strike disrupts trains and flights nationwide. (AP)",
        "Kyiv power crews race to restore light and water. (Reuters)",
    ]
    for i, b in enumerate(briefs):
        col, row = i % 2, i // 2
        x0 = 14 + col * 500
        y = 756 + row * 18
        d.text((x0, y), "%d." % (14 + i), font=SANS_B(9), fill=RED)
        d.text((x0 + 24, y), b, font=SANS(9), fill=INK)
    # --- date check ---
    d.rectangle([14, 940, 1010, 982], outline=RED, width=2)
    d.text((20, 944), "DATE CHECK \u2014 EXCLUDED AS THURSDAY 19 NOVEMBER NEWS:",
           font=SANS_B(9), fill=RED)
    d.text((20, 957), "ICJ Myanmar genocide ruling \u00b7 Trump\u2013Xi\u2013Putin Shenzhen summit itself \u00b7 Anthropic $83 IPO pricing \u00b7",
           font=SANS(8), fill=INK)
    d.text((20, 968), "GTA VI midnight launch \u00b7 Crimean Bridge strike \u00b7 Riyadh tower attack \u00b7 Van Gogh $190.4m sale \u00b7 Senate Iran vote",
           font=SANS(8), fill=INK)
    # --- footer ---
    d.line([14, 990, 1010, 990], fill=INK, width=1)
    center(d, 994, "Every story here happened, or was first reported, on Friday 20 November 2026.",
           SANS_B(9))
    center(d, 1007, "Sources: Reuters \u00b7 AP \u00b7 BBC \u00b7 IMD \u00b7 PTI \u00b7 Yonhap \u00b7 RNZ \u00b7 ESA  \u00b7  All drawings original, made procedurally.",
           SANS(8), fill=GREY)
    img.save("entry.png", optimize=True)

if __name__ == "__main__":
    main()
