#!/usr/bin/env python3
"""news-image-20261120 v3 — 'Friday 20 November 2026: The World in One Day'.

Builds a single 1024x1024 PNG news broadsheet: 46 genuine Friday
20 November 2026 stories (3 illustrated leads, 13 illustrated features,
30 briefs), a UTC timeline, verification tags on every story, a dark
world map with numbered pins, and an expanded DATE CHECK box.

All art is procedural (PIL only, DejaVu fonts). Output is byte-identical
across runs: no timestamps, no randomness, fixed font rendering.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
M = 10                      # outer margin
CW = W - 2 * M              # 1004 content width
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

# ---------------------------------------------------------------- palette
PAPER   = (247, 242, 231)
PAPER2  = (238, 231, 214)
INK     = (26, 26, 26)
MUTED   = (90, 86, 76)
RED     = (176, 30, 36)
RED_DK  = (140, 20, 26)
NAVY    = (20, 38, 74)
NAVY_DK = (13, 26, 52)
GOLD    = (200, 158, 60)
GREEN   = (34, 120, 70)
BLUE    = (30, 90, 160)
AMBER   = (190, 130, 20)
CARD    = (255, 252, 244)
LINE    = (180, 172, 150)
MAP_BG  = (27, 42, 68)
MAP_LAND= (201, 191, 165)

# ---------------------------------------------------------------- fonts
FD = "/usr/share/fonts/truetype/dejavu/"
def F(name, size):
    return ImageFont.truetype(FD + name, size)

SERIF_B = lambda s: F("DejaVuSerif-Bold.ttf", s)
SERIF   = lambda s: F("DejaVuSerif.ttf", s)
SERIF_I = lambda s: F("DejaVuSerif-Italic.ttf", s)
SANS    = lambda s: F("DejaVuSans.ttf", s)
SANS_B  = lambda s: F("DejaVuSans-Bold.ttf", s)
MONO    = lambda s: F("DejaVuSansMono.ttf", s)
MONO_B  = lambda s: F("DejaVuSansMono-Bold.ttf", s)

# ---------------------------------------------------------------- helpers
def tw(d, text, font):
    """Text width."""
    return d.textlength(text, font=font)

def wrap(d, text, font, max_w, max_lines=None):
    """Greedy word wrap. Returns list of lines, truncated with ellipsis."""
    words = text.split()
    lines, cur = [], ""
    for wd in words:
        trial = (cur + " " + wd).strip()
        if tw(d, trial, font) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = wd
            if max_lines and len(lines) >= max_lines:
                break
    if cur and (not max_lines or len(lines) < max_lines):
        lines.append(cur)
    if max_lines and len(lines) > max_lines:
        lines = lines[:max_lines]
    # ellipsis if text was cut
    if max_lines and len(" ".join(lines)) < len(text) - 1 and lines:
        last = lines[-1]
        while last and tw(d, last + "…", font) > max_w:
            last = last[:-1]
        lines[-1] = last.rstrip() + "…"
    return lines

def fit_line(d, text, font, max_w):
    """Single line, truncated with ellipsis to fit max_w."""
    if tw(d, text, font) <= max_w:
        return text
    while text and tw(d, text + "…", font) > max_w:
        text = text[:-1]
    return text.rstrip() + "…"

def pill(d, x, y, text, font, fill, fg=(255, 255, 255), pad_x=4, pad_y=1):
    """Small rounded tag; returns width used."""
    w = int(tw(d, text, font)) + 2 * pad_x
    h = font.size + 2 * pad_y + 2
    d.rounded_rectangle([x, y, x + w, y + h], radius=3, fill=fill)
    d.text((x + pad_x, y + pad_y), text, font=font, fill=fg)
    return w

def num_badge(d, x, y, n, size=13, fill=RED):
    """Numbered square badge; returns width."""
    s = str(n)
    font = SANS_B(10)
    w = max(size, int(tw(d, s, font)) + 6)
    d.rectangle([x, y, x + w, y + size], fill=fill)
    d.text((x + (w - tw(d, s, font)) / 2, y + 1), s, font=font, fill=(255, 255, 255))
    return w

STATUS = {
    "C": ("CONFIRMED", GREEN),
    "O": ("OFFICIAL", BLUE),
    "R": ("REPORTED", AMBER),
}
def status_pill(d, x, y, code, font=None):
    """Verification pill, right-aligned at x (x is right edge)."""
    font = font or SANS_B(8)
    label, color = STATUS[code]
    w = int(tw(d, label, font)) + 8
    d.rounded_rectangle([x - w, y, x, y + 11], radius=2, fill=color)
    d.text((x - w + 4, y + 1), label, font=font, fill=(255, 255, 255))
    return w

def hline(d, x0, x1, y, fill=INK, width=1):
    d.line([(x0, y), (x1, y)], fill=fill, width=width)

def card_frame(d, x, y, w, h, fill=CARD):
    d.rectangle([x, y, x + w, y + h], fill=fill, outline=LINE, width=1)

# ---------------------------------------------------------------- map data
# Simplified continent outlines in (lon, lat). Stylised, not surveyed.
CONTINENTS = [
    # North America
    [(-168,66),(-150,70),(-135,69),(-125,71),(-110,72),(-95,72),(-85,70),
     (-80,73),(-68,62),(-60,52),(-65,45),(-70,42),(-75,35),(-80,32),
     (-81,25),(-90,21),(-97,16),(-94,16),(-87,13),(-83,9),(-79,9),
     (-86,12),(-92,15),(-97,22),(-105,23),(-110,25),(-114,29),(-120,34),
     (-124,40),(-124,48),(-130,55),(-150,60),(-165,60)],
    # South America
    [(-79,9),(-75,11),(-72,12),(-64,10),(-55,6),(-50,0),(-44,-3),(-35,-8),
     (-38,-15),(-40,-22),(-48,-28),(-52,-33),(-58,-38),(-62,-41),(-65,-45),
     (-68,-50),(-69,-55),(-73,-53),(-74,-45),(-73,-37),(-71,-30),(-70,-20),
     (-75,-15),(-79,-8),(-81,-3),(-80,1)],
    # Europe
    [(-9,37),(-9,43),(-2,48),(2,51),(5,53),(8,57),(5,58),(5,61),(10,63),
     (13,66),(18,69),(25,71),(31,70),(28,65),(30,60),(27,58),(23,55),
     (21,54),(18,54),(13,54),(10,57),(7,54),(3,51),(-1,50),(-5,48),
     (-2,44),(-2,37),(0,36),(-6,36)],
    # Africa
    [(-6,35),(0,36),(10,37),(11,34),(20,32),(30,31),(32,31),(35,28),
     (37,22),(39,15),(43,12),(51,11),(51,10),(46,5),(41,0),(40,-5),
     (40,-10),(40,-15),(36,-18),(33,-22),(32,-26),(28,-30),(25,-34),
     (20,-35),(17,-32),(15,-27),(12,-18),(12,-12),(9,-1),(9,4),(4,6),
     (-8,5),(-13,8),(-17,15),(-16,20),(-15,25),(-10,31)],
    # Asia
    [(30,36),(35,42),(40,44),(45,47),(48,50),(50,55),(55,60),(60,65),
     (65,68),(70,72),(75,72),(80,73),(90,75),(100,77),(110,74),(120,73),
     (130,72),(140,72),(150,70),(160,70),(170,67),(178,65),(178,62),
     (170,60),(162,58),(158,52),(150,45),(142,42),(140,38),(135,35),
     (130,33),(127,35),(122,38),(120,35),(122,30),(118,25),(114,22),
     (110,20),(108,17),(105,9),(103,1),(100,7),(98,10),(97,16),(94,17),
     (92,21),(88,22),(86,20),(80,15),(80,7),(77,8),(75,12),(72,20),
     (68,23),(66,25),(61,25),(57,26),(54,27),(50,29),(48,30),(44,29),
     (42,30),(40,33),(36,36)],
    # Australia
    [(114,-22),(114,-28),(115,-33),(118,-35),(124,-33),(129,-32),(132,-32),
     (135,-35),(138,-35),(140,-38),(145,-38),(147,-38),(150,-37),(153,-31),
     (153,-27),(151,-24),(146,-19),(142,-15),(142,-11),(141,-13),(140,-18),
     (139,-17),(136,-15),(135,-12),(132,-11),(130,-13),(126,-14),(122,-17),
     (118,-20)],
    # UK
    [(-5,50),(-3,53),(-5,56),(-3,58),(-1,57),(0,53),(1,51)],
    # Japan
    [(130,31),(132,33),(135,34),(137,35),(139,35),(140,36),(141,39),
     (141,42),(142,44),(144,44),(145,43),(143,41),(141,38),(140,36),
     (139,34),(136,33),(133,34)],
    # New Zealand
    [(167,-45),(170,-43),(173,-39),(175,-38),(178,-38),(177,-40),
     (174,-42),(171,-43),(168,-46)],
    # Madagascar
    [(44,-16),(47,-15),(50,-16),(49,-20),(47,-24),(45,-25),(44,-21)],
    # Indonesia (Sumatra / Borneo / New Guinea blobs)
    [(95,5),(100,0),(104,-3),(106,-6),(103,-6),(99,-2),(96,2)],
    [(109,1),(113,3),(117,6),(119,1),(117,-3),(112,-3),(109,0)],
    [(131,-1),(136,-2),(141,-3),(146,-6),(150,-9),(147,-9),(141,-8),
     (136,-7),(132,-4)],
]

# ================================================================ art: leads
def art_kyiv(d, x, y, w, h):
    """Night Kyiv: skyline, Dnipro bridges, fires, missile trails."""
    d.rectangle([x, y, x + w, y + h], fill=(16, 26, 52))
    # stars
    for sx, sy in [(18,10),(52,22),(90,8),(130,16),(170,6),(205,20),(240,10),
                   (275,18),(305,8),(70,32),(150,30),(225,32),(295,30)]:
        d.ellipse([x+sx, y+sy, x+sx+2, y+sy+2], fill=(230, 230, 200))
    # moon
    d.ellipse([x+w-38, y+8, x+w-18, y+28], fill=(235, 230, 200))
    d.ellipse([x+w-34, y+6, x+w-16, y+26], fill=(16, 26, 52))
    # missile trails (dashed arcs)
    for x0, x1, y0 in [(20, 120, 14), (150, 240, 10), (230, 310, 16)]:
        for t in range(0, 11, 2):
            px = x + x0 + (x1 - x0) * t / 10
            py = y + y0 + 26 * (t / 10) ** 2
            d.ellipse([px-1, py-1, px+1, py+1], fill=(255, 200, 120))
        d.ellipse([x+x1-2, y+y0+24, x+x1+2, y+y0+28], fill=(255, 220, 150))
    # skyline blocks
    sky = [(0,58,34,86),(36,48,66,86),(68,62,96,86),(98,44,128,86),
           (130,56,158,86),(160,50,192,86),(194,60,224,86),(226,46,258,86),
           (260,58,292,86),(294,52,330,86)]
    for bx0, by0, bx1, by1 in sky:
        d.rectangle([x+bx0, y+by0, x+bx1, y+by1], fill=(10, 16, 34))
        for wy in range(by0+6, by1-4, 9):
            for wx in range(bx0+4, bx1-4, 9):
                if (wx * 7 + wy * 3) % 5 == 0:
                    d.rectangle([x+wx, y+wy, x+wx+3, y+wy+4], fill=(255, 210, 110))
    # river
    d.rectangle([x, y+86, x+w, y+h], fill=(24, 48, 88))
    for rx in range(6, w, 26):
        d.line([(x+rx, y+h-8), (x+rx+12, y+h-8)], fill=(70, 110, 170), width=1)
    # three bridges with fires
    for bx, bw in [(18, 78), (128, 78), (238, 78)]:
        d.rectangle([x+bx, y+78, x+bx+bw, y+84], fill=(60, 70, 90))
        d.line([(x+bx+6, y+78), (x+bx+bw//2, y+66), (x+bx+bw-6, y+78)],
               fill=(90, 100, 120), width=2)
        for px in (bx+10, bx+bw//2, bx+bw-10):
            d.line([(x+px, y+84), (x+px, y+94)], fill=(60, 70, 90), width=3)
    for fx in (52, 168, 272):
        d.polygon([(x+fx, y+58), (x+fx-7, y+74), (x+fx+7, y+74)], fill=(255, 140, 30))
        d.polygon([(x+fx, y+64), (x+fx-4, y+74), (x+fx+4, y+74)], fill=(255, 220, 90))
        d.ellipse([x+fx-10, y+52, x+fx+10, y+64], fill=(90, 90, 90))
    pill(d, x+6, y+6, "3 BRIDGES HIT", SANS_B(9), RED)
    pill(d, x+6, y+h-20, "111 MISSILES + 404 DRONES", SANS_B(8), (20, 20, 20))
    pill(d, x+w-118, y+h-20, "8–9 KILLED · KYIV", SANS_B(8), (20, 20, 20))

def art_akvan(d, x, y, w, h):
    """Map-style cyclone panel: coastline, spiral, landfall marker."""
    d.rectangle([x, y, x+w, y+h], fill=(28, 84, 130))
    # land (Odisha coast) top-left
    d.polygon([(x, y), (x+150, y), (x+128, y+34), (x+150, y+58), (x+118, y+80),
               (x+138, y+h), (x, y+h)], fill=(196, 178, 132))
    d.polygon([(x+150, y), (x+210, y), (x+190, y+22), (x+205, y+40),
               (x+180, y+44), (x+168, y+26)], fill=(196, 178, 132))
    d.text((x+14, y+8), "ODISHA", font=SANS_B(10), fill=(90, 70, 40))
    d.text((x+14, y+20), "INDIA", font=SANS_B(9), fill=(110, 90, 55))
    # sea texture
    for wy in range(12, h, 16):
        for wx in range(170, w-10, 34):
            d.arc([x+wx, y+wy, x+wx+14, y+wy+8], 200, 340, fill=(90, 150, 200), width=1)
    # cyclone spiral
    cx, cy = x + w - 78, y + h - 52
    for r in (44, 34, 25, 16, 8):
        d.arc([cx-r, cy-r, cx+r, cy+r], 20 + r*3, 300 + r*2,
              fill=(255, 255, 255), width=3)
    d.ellipse([cx-7, cy-7, cx+7, cy+7], fill=(255, 255, 255))
    d.ellipse([cx-4, cy-4, cx+4, cy+4], fill=(28, 84, 130))
    # track + landfall marker
    d.line([(cx-10, cy-8), (x+132, y+66)], fill=(255, 220, 120), width=2)
    for t in range(6):
        px = cx - 10 + (132 - (w-78-10)) * t / 5
        py = cy - 8 + (66 - (h-52-8)) * t / 5
        d.ellipse([px-2, py-2, px+2, py+2], fill=(255, 220, 120))
    d.ellipse([x+126, y+60, x+138, y+72], fill=RED)
    d.ellipse([x+129, y+63, x+135, y+69], fill=(255, 255, 255))
    pill(d, x+142, y+56, "LANDFALL · GOPALPUR", SANS_B(8), (20, 20, 20))
    # rain streaks
    for rx in range(150, w-6, 18):
        d.line([(x+rx, y+6), (x+rx-5, y+20)], fill=(180, 210, 235), width=2)
    pill(d, x+6, y+h-20, "300,000+ EVACUATED", SANS_B(8), RED)
    pill(d, x+w-92, y+6, "02:00 UTC", SANS_B(8), (20, 20, 20))

def art_aiselloff(d, x, y, w, h):
    """Asia AI sell-off: falling chart + closes table."""
    d.rectangle([x, y, x+w, y+h], fill=(24, 18, 30))
    # chart area left
    chart_w = w - 132
    d.rectangle([x+6, y+22, x+6+chart_w, y+h-8], fill=(38, 28, 44))
    for gy in range(0, 4):
        gyv = y + 30 + gy * ((h - 44) // 3)
        d.line([(x+8, gyv), (x+4+chart_w, gyv)], fill=(70, 55, 78), width=1)
    pts = [(x+12, y+30), (x+38, y+38), (x+64, y+34), (x+90, y+48),
           (x+116, y+44), (x+142, y+62), (x+168, y+78), (x+6+chart_w-8, y+h-16)]
    d.line(pts, fill=(255, 90, 80), width=3)
    d.polygon([(pts[-1][0]-8, pts[-1][1]-8), (pts[-1][0]+2, pts[-1][1]-2),
               (pts[-1][0]-10, pts[-1][1]+2)], fill=(255, 90, 80))
    d.text((x+8, y+6), "TAIEX · FRIDAY", font=SANS_B(9), fill=(255, 160, 150))
    # closes table right
    tx = x + w - 126
    d.rectangle([tx, y+6, x+w-6, y+h-8], fill=(12, 10, 16))
    d.text((tx+6, y+8), "FRIDAY CLOSE", font=SANS_B(8), fill=(180, 170, 190))
    rows = [("Taipei", "−6.2%"), ("Seoul", "−5.2%"), ("Tokyo", "−5.1%"),
            ("Hong Kong", "−1.9%"), ("SoftBank", "−16%")]
    for i, (city, val) in enumerate(rows):
        ry = y + 22 + i * 17
        d.text((tx+6, ry), city, font=SANS(9), fill=(220, 215, 230))
        d.text((x+w-6-tw(d, val, SANS_B(9)), ry), val, font=SANS_B(9),
               fill=(255, 100, 90))
    pill(d, x+6, y+h-20, "WORST WEEK SINCE 2020", SANS_B(8), RED)

# ============================================================ art: features
def art_ukeu(d, x, y, w, h):
    """UK–EU reset: two flags, handshake arrows, visa count."""
    d.rectangle([x, y, x+w, y+h], fill=(30, 60, 120))
    # Union Jack (simplified)
    ux, uy, uw, uh = x+6, y+8, 46, 30
    d.rectangle([ux, uy, ux+uw, uy+uh], fill=(20, 40, 110))
    d.line([(ux, uy), (ux+uw, uy+uh)], fill=(255, 255, 255), width=4)
    d.line([(ux+uw, uy), (ux, uy+uh)], fill=(255, 255, 255), width=4)
    d.line([(ux, uy), (ux+uw, uy+uh)], fill=(200, 30, 40), width=2)
    d.line([(ux+uw, uy), (ux, uy+uh)], fill=(200, 30, 40), width=2)
    d.rectangle([ux+uw//2-3, uy, ux+uw//2+3, uy+uh], fill=(255, 255, 255))
    d.rectangle([ux, uy+uh//2-3, ux+uw, uy+uh//2+3], fill=(255, 255, 255))
    d.rectangle([ux+uw//2-1, uy, ux+uw//2+1, uy+uh], fill=(200, 30, 40))
    d.rectangle([ux, uy+uh//2-1, ux+uw, uy+uh//2+1], fill=(200, 30, 40))
    # EU flag
    ex, ey = x+w-52, y+8
    d.rectangle([ex, ey, ex+46, ey+30], fill=(20, 40, 110))
    import math
    for k in range(12):
        a = 2 * math.pi * k / 12 - math.pi / 2
        sx = ex + 23 + int(11 * math.cos(a))
        sy = ey + 15 + int(11 * math.sin(a))
        d.ellipse([sx-1, sy-1, sx+1, sy+1], fill=(255, 220, 60))
    # arrows meeting
    d.line([(x+56, y+23), (x+w-56, y+23)], fill=(255, 220, 60), width=2)
    d.polygon([(x+w-58, y+19), (x+w-58, y+27), (x+w-52, y+23)], fill=(255, 220, 60))
    d.polygon([(x+58, y+19), (x+58, y+27), (x+52, y+23)], fill=(255, 220, 60))
    d.text((x+6, y+42), "100,000 VISAS / YR · AGREED", font=SANS_B(8),
           fill=(255, 255, 255))

def art_cop31(d, x, y, w, h):
    """COP31: globe, thermometer, clock, no-deal tag."""
    d.rectangle([x, y, x+w, y+h], fill=(18, 90, 70))
    # globe
    gx, gy, gr = x+24, y+24, 17
    d.ellipse([gx-gr, gy-gr, gx+gr, gy+gr], fill=(90, 160, 220))
    d.ellipse([gx-gr+5, gy-gr+3, gx+2, gy+4], fill=(120, 190, 110))
    d.ellipse([gx-2, gy+2, gx+gr-4, gy+gr-4], fill=(120, 190, 110))
    d.arc([gx-gr, gy-gr, gx+gr, gy+gr], 0, 360, fill=(255, 255, 255), width=1)
    # thermometer
    tx, ty = x+w-30, y+6
    d.rounded_rectangle([tx, ty, tx+8, ty+30], radius=4, fill=(255, 255, 255))
    d.ellipse([tx-3, ty+28, tx+11, ty+42], fill=(255, 255, 255))
    d.rectangle([tx+2, ty+14, tx+6, ty+30], fill=RED)
    d.ellipse([tx-1, ty+30, tx+9, ty+40], fill=RED)
    # clock
    cx, cy = x + w//2 + 8, y + 24
    d.ellipse([cx-12, cy-12, cx+12, cy+12], fill=(255, 255, 255))
    d.line([(cx, cy), (cx, cy-8)], fill=INK, width=2)
    d.line([(cx, cy), (cx+7, cy+2)], fill=INK, width=2)
    pill(d, x+6, y+42, "NO DEAL", SANS_B(9), RED)
    d.text((x+w-70, y+43), "$120BN GAP", font=SANS_B(9), fill=(255, 255, 255))

def art_japan(d, x, y, w, h):
    """Japan inflation: rising bars, yen, +2.3%."""
    d.rectangle([x, y, x+w, y+h], fill=(120, 30, 50))
    d.ellipse([x+10, y+8, x+34, y+32], fill=(255, 255, 255))
    d.ellipse([x+17, y+15, x+27, y+25], fill=(190, 30, 50))
    d.text((x+40, y+10), "+2.3%", font=SANS_B(20), fill=(255, 255, 255))
    d.text((x+40, y+32), "OCT CORE CPI", font=SANS_B(8), fill=(255, 200, 200))
    # rising bars
    base = y + h - 8
    vals = [8, 12, 11, 16, 15, 20, 24]
    bw = (w - 16) // len(vals)
    for i, v in enumerate(vals):
        bx = x + 8 + i * bw
        col = GOLD if i == len(vals) - 1 else (255, 255, 255)
        d.rectangle([bx, base - v, bx + bw - 3, base], fill=col)

def art_poland(d, x, y, w, h):
    """Kh-101 in a Polish field: green fields, missile, dotted track."""
    d.rectangle([x, y, x+w, y+h], fill=(110, 160, 90))
    d.rectangle([x, y, x+w, y+22], fill=(170, 210, 235))
    d.ellipse([x+w-30, y+4, x+w-14, y+20], fill=(255, 240, 160))
    # field strips
    for i, fy in enumerate((26, 36, 46)):
        d.rectangle([x, y+fy, x+w, y+fy+8],
                    fill=(130, 175, 100) if i % 2 else (95, 145, 80))
    # road
    d.polygon([(x+20, y+h), (x+44, y+26), (x+52, y+26), (x+34, y+h)],
              fill=(150, 140, 125))
    # dotted missile track from the east
    for t in range(8):
        px = x + w - 10 - t * 12
        py = y + 10 + t * 2
        d.ellipse([px-2, py-2, px+2, py+2], fill=(255, 255, 255))
    # missile in field
    mx, my = x + w//2 - 10, y + h - 26
    d.polygon([(mx+26, my), (mx+18, my-4), (mx-14, my-4), (mx-20, my),
               (mx-14, my+4), (mx+18, my+4)], fill=(210, 210, 200))
    d.polygon([(mx+26, my), (mx+18, my-4), (mx+18, my+4)], fill=RED)
    d.polygon([(mx-14, my-4), (mx-20, my-10), (mx-10, my-4)], fill=(120, 120, 110))
    d.polygon([(mx-14, my+4), (mx-20, my+10), (mx-10, my+4)], fill=(120, 120, 110))
    # impact crater + smoke
    d.ellipse([mx-24, my+2, mx+8, my+12], fill=(70, 55, 40))
    d.ellipse([mx+2, my-14, mx+12, my-6], fill=(200, 200, 200))
    d.ellipse([mx+8, my-20, mx+16, my-13], fill=(220, 220, 220))
    pill(d, x+6, y+4, "KH-101", SANS_B(8), (20, 20, 20))
    pill(d, x+6, y+h-16, "60 KM INSIDE BORDER", SANS_B(7), (20, 20, 20))

def art_italy(d, x, y, w, h):
    """Italy general strike: crowd, SCIOPERO banner, halted train."""
    d.rectangle([x, y, x+w, y+h], fill=(30, 110, 70))
    # tricolour stripe
    d.rectangle([x, y, x+w//3, y+6], fill=(40, 140, 70))
    d.rectangle([x+w//3, y, x+2*w//3, y+6], fill=(255, 255, 255))
    d.rectangle([x+2*w//3, y, x+w, y+6], fill=(200, 40, 50))
    # banner
    d.rectangle([x+8, y+12, x+w-8, y+28], fill=(255, 255, 255))
    d.text((x+12, y+14), "SCIOPERO", font=SANS_B(11), fill=RED)
    d.text((x+w-44, y+15), "24H", font=SANS_B(10), fill=INK)
    # crowd silhouettes
    for i, cx in enumerate(range(12, w-8, 16)):
        cy = y + h - 22 - (i % 2) * 4
        d.ellipse([x+cx, cy-8, x+cx+8, cy], fill=(20, 40, 30))
        d.rectangle([x+cx-2, cy, x+cx+10, cy+12], fill=(20, 40, 30))
    # placards
    d.rectangle([x+20, y+34, x+34, y+44], fill=(255, 220, 60))
    d.rectangle([x+w-36, y+32, x+w-22, y+42], fill=(255, 255, 255))
    pill(d, x+6, y+h-16, "REPORTED · REUTERS", SANS_B(7), (20, 20, 20))

def art_bukele(d, x, y, w, h):
    """Bukele third term: ballot box, 3rd tag, vote date."""
    d.rectangle([x, y, x+w, y+h], fill=(40, 90, 160))
    # ballot box
    bx, by = x+14, y+12
    d.rectangle([bx, by+10, bx+52, by+38], fill=(240, 240, 240))
    d.rectangle([bx-3, by+6, bx+55, by+12], fill=(200, 30, 40))
    d.rectangle([bx+18, by+7, bx+34, by+10], fill=(20, 20, 20))
    # ballot going in
    d.polygon([(bx+30, by-6), (bx+44, by-8), (bx+38, by+8), (bx+26, by+8)],
              fill=(255, 255, 255))
    d.line([(bx+30, by-2), (bx+40, by-3)], fill=RED, width=2)
    d.text((bx+6, by+16), "VOTO", font=SANS_B(11), fill=(40, 90, 160))
    # big 3rd
    d.text((x+w-56, y+6), "3rd", font=SERIF_B(26), fill=(255, 255, 255))
    d.text((x+w-56, y+34), "TERM BID", font=SANS_B(8), fill=(200, 220, 255))
    pill(d, x+6, y+h-16, "FILED · AP", SANS_B(7), (20, 20, 20))
    pill(d, x+w-72, y+h-16, "VOTE 28 FEB 27", SANS_B(7), (20, 20, 20))

def art_cricket(d, x, y, w, h):
    """Phillips 118: green pitch, bat, ball, scorecard tag."""
    d.rectangle([x, y, x+w, y+h], fill=(40, 130, 70))
    # pitch
    d.polygon([(x+w//2-16, y+8), (x+w//2+16, y+8), (x+w//2+26, y+h-6),
               (x+w//2-26, y+h-6)], fill=(220, 200, 150))
    d.line([(x+w//2-18, y+16), (x+w//2+18, y+16)], fill=(255, 255, 255), width=1)
    d.line([(x+w//2-22, y+h-14), (x+w//2+22, y+h-14)], fill=(255, 255, 255), width=1)
    # stumps
    for sx in (-6, 0, 6):
        d.rectangle([x+w//2+sx-1, y+10, x+w//2+sx+1, y+18], fill=(255, 220, 60))
    # bat
    d.polygon([(x+w//2+24, y+16), (x+w//2+34, y+20), (x+w//2+44, y+40),
               (x+w//2+36, y+44)], fill=(230, 210, 160))
    d.line([(x+w//2+36, y+44), (x+w//2+42, y+52)], fill=(120, 80, 40), width=3)
    # ball
    d.ellipse([x+w//2-38, y+20, x+w//2-28, y+30], fill=(200, 30, 40))
    # big score
    d.text((x+8, y+4), "118", font=SANS_B(19), fill=(255, 255, 255))
    d.text((x+8, y+26), "PHILLIPS", font=SANS_B(8), fill=(220, 255, 230))
    d.text((x+w-38, y+6), "175*", font=SANS_B(12), fill=(255, 220, 60))
    d.text((x+w-46, y+21), "NICHOLLS", font=SANS_B(7), fill=(220, 255, 230))
    pill(d, x+6, y+h-16, "SCORECARD · ICC", SANS_B(7), (20, 20, 20))

def art_bepi(d, x, y, w, h):
    """BepiColombo: black space, Mercury, spacecraft, orbit tag."""
    d.rectangle([x, y, x+w, y+h], fill=(8, 8, 18))
    for sx, sy in [(10,8),(30,20),(55,6),(80,16),(110,8),(125,26),(20,36),
                   (70,34),(100,40),(45,44)]:
        d.ellipse([x+sx, y+sy, x+sx+2, y+sy+2], fill=(220, 220, 220))
    # Mercury
    mx, my, mr = x+w-34, y+26, 18
    d.ellipse([mx-mr, my-mr, mx+mr, my+mr], fill=(170, 150, 130))
    d.ellipse([mx-8, my-6, mx-2, my+0], fill=(140, 120, 105))
    d.ellipse([mx+2, my+4, mx+8, my+10], fill=(140, 120, 105))
    d.ellipse([mx-2, my-12, mx+4, my-7], fill=(140, 120, 105))
    d.text((mx-16, my+mr+2), "MERCURY", font=SANS_B(7), fill=(220, 210, 190))
    # trajectory
    for t in range(9):
        px = x + 12 + t * 9
        py = y + h - 12 - t * 3
        d.ellipse([px-1, py-1, px+1, py+1], fill=(255, 220, 100))
    # spacecraft
    sx, sy = x + 92, y + h - 40
    d.rectangle([sx-8, sy-4, sx+8, sy+4], fill=(200, 200, 210))
    d.rectangle([sx-22, sy-2, sx-8, sy+2], fill=(80, 120, 200))
    d.rectangle([sx+8, sy-2, sx+22, sy+2], fill=(80, 120, 200))
    d.polygon([(sx, sy-10), (sx-4, sy-4), (sx+4, sy-4)], fill=(255, 220, 100))
    pill(d, x+6, y+4, "8-YEAR TRIP", SANS_B(8), (40, 40, 60))
    pill(d, x+6, y+h-16, "ORBIT INSERTION SAT", SANS_B(7), GOLD)

def art_china(d, x, y, w, h):
    """China holds LPR: bank facade + rate table."""
    d.rectangle([x, y, x+w, y+h], fill=(150, 30, 30))
    # bank facade
    bx, by = x+8, y+4
    d.polygon([(bx, by+12), (bx+26, by), (bx+52, by+12)], fill=(255, 255, 255))
    d.rectangle([bx+2, by+12, bx+50, by+36], fill=(255, 255, 255))
    for cx in range(bx+6, bx+46, 11):
        d.rectangle([cx, by+15, cx+5, by+30], fill=(150, 30, 30))
    d.rectangle([bx, by+36, bx+52, by+40], fill=(230, 230, 230))
    # rate table
    tx = x + w - 62
    d.rectangle([tx, y+6, x+w-6, y+42], fill=(20, 20, 20))
    d.text((tx+5, y+8), "1Y  3.00%", font=MONO_B(9), fill=(255, 255, 255))
    d.text((tx+5, y+20), "5Y  3.50%", font=MONO_B(9), fill=(255, 255, 255))
    d.text((tx+5, y+32), "HELD", font=SANS_B(8), fill=(120, 220, 140))
    d.text((x+8, y+46), "18TH MONTH UNCHANGED", font=SANS_B(8),
           fill=(255, 255, 255))

def art_hormuz(d, x, y, w, h):
    """Hormuz: tanker ablaze, Brent price, ships waiting."""
    d.rectangle([x, y, x+w, y+h], fill=(30, 70, 110))
    d.rectangle([x, y, x+w, y+18], fill=(200, 220, 240))
    d.ellipse([x+10, y+4, x+26, y+20], fill=(255, 240, 160))
    # sea
    for wy in (30, 44):
        for wx in range(4, w-8, 22):
            d.arc([x+wx, y+wy, x+wx+12, y+wy+6], 200, 340,
                  fill=(120, 180, 220), width=1)
    # tanker
    tx, ty = x+12, y+24
    d.polygon([(tx, ty+14), (tx+8, ty+22), (tx+92, ty+22), (tx+100, ty+14),
               (tx+100, ty+8), (tx, ty+8)], fill=(140, 40, 40))
    d.rectangle([tx+70, ty-2, tx+92, ty+8], fill=(230, 230, 230))
    d.rectangle([tx+78, ty-8, tx+84, ty-2], fill=(230, 230, 230))
    # flame + smoke
    d.polygon([(tx+44, ty-12), (tx+38, ty+6), (tx+50, ty+6)], fill=(255, 140, 30))
    d.polygon([(tx+44, ty-6), (tx+40, ty+6), (tx+48, ty+6)], fill=(255, 220, 90))
    d.ellipse([tx+38, ty-22, tx+52, ty-12], fill=(120, 120, 120))
    d.ellipse([tx+44, ty-28, tx+54, ty-20], fill=(150, 150, 150))
    # waiting ships (small silhouettes)
    for sx in (w-34, w-20):
        d.polygon([(x+sx, y+40), (x+sx+4, y+46), (x+sx+12, y+46),
                   (x+sx+14, y+40)], fill=(20, 40, 60))
    pill(d, x+6, y+h-16, "BRENT $92.50", SANS_B(8), (20, 20, 20))
    pill(d, x+w-78, y+h-16, "46 SHIPS WAIT", SANS_B(7), (20, 20, 20))

def art_seoul(d, x, y, w, h):
    """Seoul impeach: courthouse columns + gavel."""
    d.rectangle([x, y, x+w, y+h], fill=(60, 60, 90))
    # courthouse
    cx, cy = x+10, y+8
    d.polygon([(cx, cy+10), (cx+30, cy), (cx+60, cy+10)], fill=(230, 225, 200))
    d.rectangle([cx+2, cy+10, cx+58, cy+34], fill=(230, 225, 200))
    for px in range(cx+6, cx+54, 12):
        d.rectangle([px, cy+13, px+5, cy+29], fill=(60, 60, 90))
    d.rectangle([cx, cy+34, cx+60, cy+38], fill=(200, 195, 170))
    # gavel
    gx, gy = x + w - 40, y + 12
    d.line([(gx, gy+18), (gx+22, gy-2)], fill=(180, 140, 90), width=4)
    d.rectangle([gx+16, gy-8, gx+30, gy+2], fill=(140, 100, 60))
    d.rectangle([gx+2, gy+20, gx+20, gy+24], fill=(140, 100, 60))
    pill(d, x+6, y+h-16, "PARTY DECISION · YONHAP", SANS_B(7), (20, 20, 20))

def art_kenya(d, x, y, w, h):
    """Kenya first oil well: derrick at sunset, Turkana."""
    d.rectangle([x, y, x+w, y+h], fill=(230, 150, 60))
    d.ellipse([x+w-36, y+6, x+w-12, y+30], fill=(255, 230, 150))
    d.rectangle([x, y+h-16, x+w, y+h], fill=(120, 80, 40))
    # derrick
    dx, dy = x + w//2, y + 8
    d.polygon([(dx-14, y+h-16), (dx-4, dy), (dx+4, dy), (dx+14, y+h-16)],
              outline=(60, 40, 20), width=3)
    d.line([(dx-10, y+h-26), (dx+10, y+h-26)], fill=(60, 40, 20), width=2)
    d.line([(dx-7, y+h-36), (dx+7, y+h-36)], fill=(60, 40, 20), width=2)
    d.line([(dx-4, y+h-46), (dx+4, y+h-46)], fill=(60, 40, 20), width=2)
    d.line([(dx, dy), (dx, y+h-16)], fill=(60, 40, 20), width=2)
    # acacia tree
    d.line([(x+16, y+h-16), (x+16, y+h-34)], fill=(70, 50, 30), width=3)
    d.ellipse([x+4, y+h-44, x+28, y+h-32], fill=(80, 110, 50))
    d.text((x+6, y+6), "TURKANA", font=SANS_B(9), fill=(255, 255, 255))
    pill(d, x+6, y+h-16, "1ST WELL · DRILLING BEGUN", SANS_B(7), (20, 20, 20))

def art_nvidia(d, x, y, w, h):
    """Nvidia sinks 14%: chip + red down arrow + SEC probe tag."""
    d.rectangle([x, y, x+w, y+h], fill=(20, 60, 40))
    # chip
    cx, cy = x+12, y+10
    d.rectangle([cx, cy, cx+34, cy+34], fill=(30, 30, 30))
    d.rectangle([cx+8, cy+8, cx+26, cy+26], fill=(120, 200, 90))
    for px in range(cx+4, cx+32, 8):
        d.line([(px, cy-4), (px, cy)], fill=(180, 180, 180), width=2)
        d.line([(px, cy+34), (px, cy+38)], fill=(180, 180, 180), width=2)
    for py in range(cy+4, cy+32, 8):
        d.line([(cx-4, py), (cx, py)], fill=(180, 180, 180), width=2)
        d.line([(cx+34, py), (cx+38, py)], fill=(180, 180, 180), width=2)
    # red arrow down
    ax = x + w - 40
    d.polygon([(ax+14, y+8), (ax+26, y+8), (ax+26, y+28), (ax+34, y+28),
               (ax+20, y+46), (ax+6, y+28), (ax+14, y+28)], fill=(255, 70, 60))
    d.text((x+52, y+10), "−14%", font=SANS_B(20), fill=(255, 120, 110))
    d.text((x+52, y+32), "ON SEC PROBE", font=SANS_B(8), fill=(255, 255, 255))
    pill(d, x+6, y+h-16, "REPORTED · REUTERS", SANS_B(7), (20, 20, 20))

# ================================================================ story data
# status: C = CONFIRMED (2+ outlets), O = OFFICIAL (on the record),
#         R = REPORTED (one outlet)
LEADS = [
    dict(n=1, place="KYIV, UKRAINE", field="WAR", region="Europe", st="C",
         art=art_kyiv,
         head="Russian missiles hit three Kyiv bridges",
         body="An overnight barrage of about 110 missiles and 400 drones "
              "killed at least eight people across Ukraine and cut power "
              "and water in the capital. (Kyiv Independent, BBC)"),
    dict(n=2, place="ODISHA, INDIA", field="CYCLONE", region="Asia", st="O",
         art=art_akvan,
         head="Cyclone Akvan comes ashore in eastern India",
         body="The storm crossed the coast near Gopalpur from about 8 am "
              "after more than 300,000 people were moved to shelters. "
              "No deaths were reported. (IMD, Deccan Herald)"),
    dict(n=3, place="TAIPEI · SEOUL · TOKYO", field="MARKETS", region="Asia",
         st="C", art=art_aiselloff,
         head="AI sell-off sinks Asia's stock markets",
         body="Taiwan's index fell 6.2% to end its worst week since 1991. "
              "Seoul lost 5.2% and Tokyo 5.1% as chipmakers led the slide. "
              "(Al Jazeera, Anadolu)"),
]

FEATURES = [
    dict(n=4, place="BRUSSELS", field="DIPLOMACY", region="Europe", st="O",
         art=art_ukeu, head="UK and EU seal a “reset” deal",
         body="Food trade, youth visas, carbon link. (BBC)"),
    dict(n=5, place="ANTALYA", field="CLIMATE", region="Europe", st="C",
         art=art_cop31, head="COP31 reaches its last day with no deal",
         body="The draft text leaves out fossil fuels. (UN News)"),
    dict(n=6, place="TOKYO", field="ECONOMY", region="Asia", st="O",
         art=art_japan, head="Japan's inflation picks up to 2.3%",
         body="A December rate rise stays in view. (Reuters)"),
    dict(n=7, place="EASTERN POLAND", field="SECURITY", region="Europe",
         st="O", art=art_poland, head="Russian cruise missile lands in Poland",
         body="It fell in a field; two airports paused. (Reuters)"),
    dict(n=8, place="ITALY", field="LABOUR", region="Europe", st="C",
         art=art_italy, head="General strike over Italy's budget",
         body="Workers and students march. (AP)"),
    dict(n=9, place="SAN SALVADOR", field="POLITICS", region="Americas",
         st="O", art=art_bukele, head="Bukele files to run for a third term",
         body="The vote is on 28 February 2027. (AP)"),
    dict(n=10, place="WELLINGTON", field="CRICKET", region="Oceania", st="O",
         art=art_cricket, head="Phillips hits 118 against India",
         body="Hundreds v India in all three formats. (ICC)"),
    dict(n=11, place="MERCURY · SPACE", field="SPACE", region="Global", st="O",
         art=art_bepi, head="BepiColombo reaches Mercury",
         body="After 8 years in flight; orbit insertion Saturday. (ESA)"),
    dict(n=12, place="BEIJING", field="RATES", region="Asia", st="O",
         art=art_china, head="China holds lending rates for 18th month",
         body="1-year LPR at 3.0%, 5-year at 3.5%. (PBOC, Reuters)"),
    dict(n=13, place="HORMUZ", field="ENERGY", region="Middle East", st="R",
         art=art_hormuz, head="Tanker attacks lift Brent to $92.50",
         body="Attacks near Hormuz leave 46 ships waiting. (Reuters)"),
    dict(n=14, place="SEOUL", field="POLITICS", region="Asia", st="C",
         art=art_seoul, head="Korea's ruling party to impeach top judge",
         body="It follows an overturned conviction. (Yonhap)"),
    dict(n=15, place="TURKANA, KENYA", field="ENERGY", region="Africa", st="O",
         art=art_kenya, head="Kenya starts drilling its first oil well",
         body="First crude is due on 1 December. (KBC)"),
    dict(n=16, place="US · TECH", field="TECH", region="Americas", st="R",
         art=art_nvidia, head="Nvidia sinks 14% on SEC probe report",
         body="SEC staff are examining its accounting. (Reuters)"),
]

# (num, text with source, region, status) — one line each in the briefs panel
BRIEFS = [
    (17, "Iraq army enters Jurf al-Sakhar militia stronghold (AP)", "Middle East", "C"),
    (18, "Second US judge blocks Trump's 250-ft arch (AP)", "Americas", "C"),
    (19, "Argentina country risk jumps to 1,070 (JPM)", "Americas", "C"),
    (20, "Florida floods spread north after days of rain (AP)", "Americas", "C"),
    (21, "Trump threatens penalties for data centres (Reuters)", "Americas", "R"),
    (22, "Panama asks COP31 to cap world oil output (Anadolu)", "Americas", "C"),
    (23, "WFP appeals for $12bn to feed 91m people (UN News)", "Global", "O"),
    (24, "Voyager 1 reaches one light-day from Earth (NASA)", "Global", "O"),
    (25, "Malawi fuel crisis brings night-long queues (Al Jazeera)", "Africa", "C"),
    (26, "Senegal migrant boat capsizes; 4 dead (AP)", "Africa", "C"),
    (27, "Sudan drone strike kills 10 at gold mine (Reuters)", "Africa", "R"),
    (28, "F1 Las Vegas practice: Russell fastest in wet (AP)", "Americas", "O"),
    (29, "California probes Nvidia over China chip sales (Reuters)", "Americas", "R"),
    (30, "Pancreatic cancer pill: tumours shrink 60.7% (AP)", "Global", "R"),
    (31, "Tonga declares El Niño drought emergency (RNZ)", "Oceania", "O"),
    (32, "Xi and Albanese hail a turnaround in ties (Reuters)", "Asia", "C"),
    (33, "Estonia to shut its road border with Russia (Reuters)", "Europe", "O"),
    (34, "Lviv railway station strike kills 2 (BBC)", "Europe", "C"),
    (35, "Suneung exam: 111 caught cheating (Yonhap)", "Asia", "O"),
    (36, "Kospi trading curb triggered amid sell-off (Yonhap)", "Asia", "O"),
    (37, "EU calls COP31 draft unacceptable (RTE)", "Europe", "C"),
    (38, "ATP approves pay reforms worth $350m (Anadolu)", "Global", "O"),
    (39, "Nasdaq futures fall 1.6% before the bell (WSJ)", "Americas", "C"),
    (40, "St Johns River hits record 18.3 ft (AP)", "Americas", "O"),
    (41, "Myanmar calls World Court ruling 'unfair' (AP)", "Asia", "O"),
    (42, "Anthropic falls 8.6% on day two, still above $83 (Reuters)", "Americas", "C"),
    (43, "Hunger Games prequel takes $21.25m previews (AP)", "Americas", "C"),
    (44, "Mexico: Sheinbaum leads Revolution Day parade (AP)", "Americas", "O"),
    (45, "US Fed's Lisa Cook calls for rate hikes (Reuters)", "Americas", "O"),
    (46, "GTA VI sales top $2.3bn — Friday update (Reuters)", "Americas", "R"),
]

TIMELINE = [
    ("00:00", "Kyiv bridges hit"),
    ("02:00", "Akvan landfall"),
    ("05:30", "Taiwan ends −6.2%"),
    ("05:50", "Missile lands in Poland"),
    ("15:00", "COP31 runs past close"),
    ("19:10", "Report of Nvidia probe"),
    ("21:00", "S&P 500 ends −3.7%"),
]

STATS = [
    ("3", "Dnipro bridges damaged in Kyiv"),
    ("300,000+", "moved to shelters before Akvan"),
    ("−6.2%", "Taiwan's index, Friday's close"),
    ("100,000", "youth visas a year in UK–EU deal"),
    ("2.3%", "Japan inflation in October"),
    ("118", "runs by Phillips against India"),
]

REGION_COLORS = {
    "Europe": (30, 80, 160), "Asia": (176, 30, 36),
    "Middle East": (200, 140, 40), "Africa": (34, 120, 70),
    "Americas": (110, 60, 150), "Oceania": (20, 140, 160),
    "Global": (90, 90, 90),
}
REGION_ORDER = ["Europe", "Asia", "Middle East", "Africa", "Americas",
                "Oceania", "Global"]

DATE_CHECK = (
    "Left out on purpose, first reported Thursday 19 November: the ICJ Myanmar "
    "genocide ruling · the Shenzhen summit itself · Anthropic's $83 IPO pricing · "
    "the GTA VI midnight launch · the Crimean Bridge strike · the Riyadh tower "
    "attack · the Van Gogh $190.4m sale · the Senate 48–51 Iran vote · Denmark's "
    "Greenland–US pact.  NOT YET: BepiColombo's Mercury orbit entry (Sat 21) · "
    "COP31's next draft (Sat 21) · the ATP Finals final (Sun 22)."
)

# map pins: (story num, lon, lat, dx, dy) — dx/dy nudge crowded clusters
PINS = [
    (1, 30.5, 50.4, 4, -2), (2, 85.0, 19.3, 0, 0), (3, 121.6, 25.0, 0, 2),
    (4, 4.4, 50.9, -8, -6), (5, 30.7, 36.9, 6, 6), (6, 139.7, 35.7, 4, -6),
    (7, 19.0, 55.0, -8, -8), (8, 12.5, 41.9, -4, 6), (9, -89.2, 13.7, 0, 0),
    (10, 174.8, -41.3, 0, 0), (12, 116.4, 39.9, -6, -6), (13, 56.5, 27.0, 0, 0),
    (14, 127.0, 37.5, 6, 6), (15, 36.0, 3.0, 0, 0), (16, -122.0, 37.4, 0, 0),
]
# small unnumbered dots for brief locations (lon, lat)
DOTS = [(-17.0, 14.7), (33.8, -13.9), (30.0, 15.0), (-175.2, -21.1),
        (-81.7, 28.3), (-64.0, -34.0), (-99.1, 19.4), (24.0, 49.8),
        (24.7, 59.4), (-3.7, 40.4)]

def draw_map(d, x, y, w, h):
    """Dark world map with numbered pins for the drawn stories."""
    d.rectangle([x, y, x + w, y + h], fill=MAP_BG)
    # graticule
    for gx in range(1, 12):
        gx0 = x + gx * w // 12
        d.line([(gx0, y), (gx0, y + h)], fill=(40, 58, 88), width=1)
    for gy in range(1, 5):
        gy0 = y + gy * h // 5
        d.line([(x, gy0), (x + w, gy0)], fill=(40, 58, 88), width=1)

    def proj(lon, lat):
        px = x + (lon + 180.0) / 360.0 * w
        py = y + (85.0 - lat) / 145.0 * h
        return px, py

    for poly in CONTINENTS:
        pts = [proj(lon, lat) for lon, lat in poly]
        d.polygon(pts, fill=MAP_LAND)
    # equator hint
    _, eqy = proj(0, 0)
    d.line([(x, eqy), (x + w, eqy)], fill=(70, 90, 120), width=1)

    for lon, lat in DOTS:
        px, py = proj(lon, lat)
        d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=(90, 200, 220))

    font = SANS_B(8)
    for n, lon, lat, dx, dy in PINS:
        px, py = proj(lon, lat)
        px += dx
        py += dy
        d.ellipse([px - 6, py - 6, px + 6, py + 6], fill=RED,
                  outline=(255, 255, 255), width=1)
        s = str(n)
        d.text((px - tw(d, s, font) / 2, py - 5), s, font=font,
               fill=(255, 255, 255))
    # space marker
    pill(d, x + 6, y + h - 18, "SPACE · 11 BepiColombo · 24 Voyager 1",
         SANS_B(7), (10, 14, 26))
    pill(d, x + w - 118, y + 6, "PINS 1–16 = STORIES ABOVE", SANS_B(7),
         (10, 14, 26))

# ================================================================ compose
def compose():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    all_stories = LEADS + FEATURES
    n_total = len(all_stories) + len(BRIEFS)
    fields = sorted({s["field"] for s in all_stories})
    regions = {}
    for s in all_stories:
        regions[s["region"]] = regions.get(s["region"], 0) + 1
    for _, _, reg, _ in BRIEFS:
        regions[reg] = regions.get(reg, 0) + 1
    assert n_total == 46, n_total

    # ---- kicker ------------------------------------------------------
    y = 8
    d.text((M, y), "THE WORLD IN ONE DAY", font=SANS_B(11), fill=RED)
    rk = (f"{n_total} STORIES · {len(REGION_ORDER)} REGIONS · {len(fields)} "
          f"FIELDS · EVERY ONE DATED FRIDAY 20 NOVEMBER 2026")
    d.text((W - M - tw(d, rk, SANS_B(10)), y + 1), rk, font=SANS_B(10), fill=INK)
    hline(d, M, W - M, 24, fill=INK, width=2)

    # ---- masthead ----------------------------------------------------
    mast = "Friday 20 November 2026"
    mf = SERIF_B(54)
    d.text(((W - tw(d, mast, mf)) / 2, 28), mast, font=mf, fill=INK)

    # ---- subhead band ------------------------------------------------
    d.rectangle([M, 96, W - M, 114], fill=NAVY)
    sub = ("Russian missiles hit Kyiv’s bridges · Cyclone Akvan strikes India · "
           "An AI sell-off sinks Asia’s markets · UK and EU seal a deal")
    sf = SERIF(13)
    d.text(((W - tw(d, sub, sf)) / 2, 99), sub, font=sf, fill=(255, 255, 255))

    # ---- UTC timeline ------------------------------------------------
    ty, th = 118, 30
    d.rectangle([M, ty, W - M, ty + th], fill=CARD, outline=LINE, width=1)
    d.rectangle([M, ty, M + 92, ty + th], fill=RED)
    d.text((M + 8, ty + 3), "THE DAY", font=SANS_B(10), fill=(255, 255, 255))
    d.text((M + 8, ty + 15), "IN UTC", font=SANS_B(10), fill=(255, 255, 255))
    cell_w = (CW - 92) / len(TIMELINE)
    for i, (t, ev) in enumerate(TIMELINE):
        cx = M + 92 + i * cell_w
        d.text((cx + 6, ty + 2), t, font=MONO_B(11), fill=RED)
        d.text((cx + 6, ty + 15), fit_line(d, ev, SANS(9), cell_w - 10),
               font=SANS(9), fill=INK)
        if i:
            d.line([(cx, ty + 4), (cx, ty + th - 4)], fill=LINE, width=1)

    # ---- stat strip --------------------------------------------------
    sy, sh = 152, 30
    d.rectangle([M, sy, W - M, sy + sh], fill=PAPER2, outline=LINE, width=1)
    sw = CW / len(STATS)
    for i, (num, lab) in enumerate(STATS):
        cx = M + i * sw
        d.text((cx + 8, sy + 2), num, font=SANS_B(16), fill=RED)
        d.text((cx + 8, sy + 20),
               fit_line(d, lab, SANS(8), sw - 14), font=SANS(8), fill=MUTED)
        if i:
            d.line([(cx, sy + 4), (cx, sy + sh - 4)], fill=LINE, width=1)

    # ---- region strip ------------------------------------------------
    ry, rh = 186, 13
    rw = CW / len(REGION_ORDER)
    for i, reg in enumerate(REGION_ORDER):
        cx = M + i * rw
        wseg = rw if i < len(REGION_ORDER) - 1 else CW - i * rw
        d.rectangle([cx, ry, cx + wseg, ry + rh],
                    fill=REGION_COLORS[reg])
        lab = f"{reg.upper()} {regions.get(reg, 0)}"
        d.text((cx + (wseg - tw(d, lab, SANS_B(8))) / 2, ry + 2), lab,
               font=SANS_B(8), fill=(255, 255, 255))

    # ---- leads -------------------------------------------------------
    ly, lh = 203, 226
    lw = int((CW - 2 * 7) / 3)
    for i, s in enumerate(LEADS):
        cx = int(M + i * (lw + 7))
        card_frame(d, cx, ly, lw, lh)
        s["art"](d, cx + 1, ly + 1, lw - 2, 116)
        ky = ly + 121
        bw = num_badge(d, cx + 6, ky, s["n"], size=13)
        kick = f"{s['place']} · {s['field']}"
        d.text((cx + 6 + bw + 4, ky + 1),
               fit_line(d, kick, SANS_B(9), lw - bw - 76),
               font=SANS_B(9), fill=RED)
        status_pill(d, cx + lw - 6, ky, s["st"])
        hy = ly + 138
        for j, hl in enumerate(wrap(d, s["head"], SERIF_B(19), lw - 12,
                                    max_lines=2)):
            d.text((cx + 6, hy + j * 22), hl, font=SERIF_B(19), fill=INK)
        by = ly + 184
        for j, bl in enumerate(wrap(d, s["body"], SANS(11), lw - 12,
                                    max_lines=3)):
            d.text((cx + 6, by + j * 13), bl, font=SANS(11), fill=INK)

    # ---- features ----------------------------------------------------
    def feature_row(y0, h0, items, gap=6):
        cw = int((CW - gap * (len(items) - 1)) / len(items))
        for i, s in enumerate(items):
            cx = int(M + i * (cw + gap))
            card_frame(d, cx, y0, cw, h0)
            s["art"](d, cx + 1, y0 + 1, cw - 2, 58)
            ky = y0 + 62
            bw = num_badge(d, cx + 5, ky, s["n"], size=12)
            # letter chip for verification status
            _, col = STATUS[s["st"]]
            d.rectangle([cx + cw - 16, ky, cx + cw - 5, ky + 12], fill=col)
            d.text((cx + cw - 13, ky + 1), s["st"], font=SANS_B(8),
                   fill=(255, 255, 255))
            d.text((cx + 5 + bw + 3, ky + 1),
                   fit_line(d, s["place"], SANS_B(8), cw - bw - 26),
                   font=SANS_B(8), fill=RED)
            hy = y0 + 77
            for j, hl in enumerate(wrap(d, s["head"], SERIF_B(11), cw - 10,
                                        max_lines=3)):
                d.text((cx + 5, hy + j * 14), hl, font=SERIF_B(11), fill=INK)
            by = y0 + 77 + 3 * 14 + 1
            for j, bl in enumerate(wrap(d, s["body"], SANS(9), cw - 10,
                                        max_lines=2)):
                d.text((cx + 5, by + j * 11), bl, font=SANS(9), fill=INK)

    feature_row(433, 142, FEATURES[:7])
    feature_row(579, 142, FEATURES[7:])

    # ---- map + briefs ------------------------------------------------
    my, mh = 725, 176
    # map panel
    d.rectangle([M, my, M + 330, my + mh], fill=CARD, outline=LINE, width=1)
    d.text((M + 6, my + 4), "WHERE IT HAPPENED", font=SANS_B(10), fill=RED)
    draw_map(d, M + 6, my + 20, 318, mh - 40)
    d.text((M + 6, my + mh - 14),
           "Numbers match the stories above · dots mark brief locations",
           font=SANS(8), fill=MUTED)
    # briefs panel
    bx = M + 336
    bw = W - M - bx
    d.rectangle([bx, my, bx + bw, my + mh], fill=CARD, outline=LINE, width=1)
    d.text((bx + 6, my + 4),
           "ALSO ON FRIDAY 20 NOVEMBER — 30 MORE STORIES",
           font=SANS_B(10), fill=RED)
    col_w = (bw - 12 - 12) / 2
    bf = SANS(9)
    for idx, (n, text, _reg, st) in enumerate(BRIEFS):
        col = idx // 15
        row = idx % 15
        tx = bx + 6 + col * (col_w + 12)
        tyy = my + 20 + row * 10.4
        _, scol = STATUS[st]
        d.ellipse([tx, tyy + 2, tx + 6, tyy + 8], fill=scol)
        ns = f"{n} "
        d.text((tx + 9, tyy - 1), ns, font=SANS_B(9), fill=RED)
        nx = tx + 9 + tw(d, ns, SANS_B(9))
        d.text((nx, tyy - 1),
               fit_line(d, text, bf, col_w - (nx - tx)),
               font=bf, fill=INK)

    # ---- DATE CHECK --------------------------------------------------
    dy, dh = 905, 54
    d.rectangle([M, dy, W - M, dy + dh], fill=(255, 244, 240),
                outline=RED, width=1)
    d.rectangle([M, dy, M + 88, dy + dh], fill=RED)
    d.text((M + 8, dy + 12), "DATE", font=SANS_B(12), fill=(255, 255, 255))
    d.text((M + 8, dy + 27), "CHECK", font=SANS_B(12), fill=(255, 255, 255))
    dc_lines = wrap(d, DATE_CHECK, SANS(9), CW - 88 - 16, max_lines=4)
    for j, ll in enumerate(dc_lines):
        d.text((M + 96, dy + 4 + j * 12), ll, font=SANS(9), fill=INK)

    # ---- legend + footer ---------------------------------------------
    ly2 = 966
    lx = M
    for code in ("C", "O", "R"):
        label, col = STATUS[code]
        d.rectangle([lx, ly2, lx + 11, ly2 + 11], fill=col)
        d.text((lx + 2, ly2 + 1), code, font=SANS_B(8), fill=(255, 255, 255))
        expl = {"C": "CONFIRMED · 2+ outlets",
                "O": "OFFICIAL · on the record",
                "R": "REPORTED · one outlet"}[code]
        d.text((lx + 14, ly2 + 1), expl, font=SANS_B(8), fill=INK)
        lx += 14 + tw(d, expl, SANS_B(8)) + 18
    rn = "Sources named beside each story · All drawings original, procedural"
    d.text((W - M - tw(d, rn, SANS(8)), ly2 + 1), rn, font=SANS(8), fill=MUTED)

    foot = ("Every story here happened, or was first reported, on "
            "Friday 20 November 2026.")
    ff = SANS_B(11)
    d.text(((W - tw(d, foot, ff)) / 2, 984), foot, font=ff, fill=INK)
    hline(d, M, W - M, 1002, fill=INK, width=2)
    return img

def main():
    img = compose()
    img.save(OUT, format="PNG")
    print("wrote", OUT, os.path.getsize(OUT), "bytes")

if __name__ == "__main__":
    main()
