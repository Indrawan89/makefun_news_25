#!/usr/bin/env python3
"""THE WORLD TODAY - Wednesday 25 November 2026.

A one-day world news poster for make.fun's news-image-20261125 bounty.
Pure Python standard library, no network. Draws a 1024x1024 newspaper
poster (masthead, lead story with a market bar panel, a war-at-sea strip,
and 32 dated stories in 8 region boxes) and writes output/entry.png.

Everything here was written fresh in this session: the 5x7 bitmap font,
the canvas, the PNG encoder (zlib + CRC32), and the layout. Deterministic:
two runs write byte-identical PNGs.
"""

import hashlib
import os
import struct
import zlib

# ---------------------------------------------------------------- font -----
# 5x7 bitmap font. Each glyph is 7 rows; each row is a 5-bit integer,
# bit 4 = leftmost pixel. Only the characters the poster needs.
FONT = {
    "A": (14, 17, 17, 31, 17, 17, 17),
    "B": (30, 17, 17, 30, 17, 17, 30),
    "C": (14, 17, 16, 16, 16, 17, 14),
    "D": (30, 17, 17, 17, 17, 17, 30),
    "E": (31, 16, 16, 30, 16, 16, 31),
    "F": (31, 16, 16, 30, 16, 16, 16),
    "G": (14, 17, 16, 23, 17, 17, 15),
    "H": (17, 17, 17, 31, 17, 17, 17),
    "I": (14, 4, 4, 4, 4, 4, 14),
    "J": (7, 2, 2, 2, 2, 18, 12),
    "K": (17, 18, 20, 24, 20, 18, 17),
    "L": (16, 16, 16, 16, 16, 16, 31),
    "M": (17, 27, 21, 21, 17, 17, 17),
    "N": (17, 25, 21, 19, 17, 17, 17),
    "O": (14, 17, 17, 17, 17, 17, 14),
    "P": (30, 17, 17, 30, 16, 16, 16),
    "Q": (14, 17, 17, 17, 21, 18, 13),
    "R": (30, 17, 17, 30, 20, 18, 17),
    "S": (15, 16, 16, 14, 1, 1, 30),
    "T": (31, 4, 4, 4, 4, 4, 4),
    "U": (17, 17, 17, 17, 17, 17, 14),
    "V": (17, 17, 17, 17, 17, 10, 4),
    "W": (17, 17, 17, 21, 21, 27, 17),
    "X": (17, 17, 10, 4, 10, 17, 17),
    "Y": (17, 17, 10, 4, 4, 4, 4),
    "Z": (31, 1, 2, 4, 8, 16, 31),
    "0": (14, 17, 19, 21, 25, 17, 14),
    "1": (4, 12, 4, 4, 4, 4, 14),
    "2": (14, 17, 1, 6, 8, 16, 31),
    "3": (31, 2, 4, 2, 1, 17, 14),
    "4": (2, 6, 10, 18, 31, 2, 2),
    "5": (31, 16, 30, 1, 1, 17, 14),
    "6": (6, 8, 16, 30, 17, 17, 14),
    "7": (31, 1, 2, 4, 8, 8, 8),
    "8": (14, 17, 17, 14, 17, 17, 14),
    "9": (14, 17, 17, 15, 1, 2, 12),
    " ": (0, 0, 0, 0, 0, 0, 0),
    ".": (0, 0, 0, 0, 0, 12, 12),
    ",": (0, 0, 0, 0, 12, 4, 8),
    ":": (0, 12, 12, 0, 12, 12, 0),
    ";": (0, 12, 12, 0, 12, 4, 8),
    "!": (4, 4, 4, 4, 4, 0, 4),
    "?": (14, 17, 1, 6, 4, 0, 4),
    "-": (0, 0, 0, 14, 0, 0, 0),
    "(": (2, 4, 8, 8, 8, 4, 2),
    ")": (8, 4, 2, 2, 2, 4, 8),
    "%": (25, 26, 2, 4, 8, 11, 19),
    "$": (4, 15, 20, 14, 5, 30, 4),
    "&": (12, 18, 20, 8, 21, 18, 13),
    "+": (0, 4, 4, 31, 4, 4, 0),
    "=": (0, 0, 31, 0, 31, 0, 0),
    "*": (0, 21, 14, 21, 0, 0, 0),
    "#": (10, 10, 31, 10, 31, 10, 10),
    "'": (4, 4, 8, 0, 0, 0, 0),
    '"': (10, 10, 0, 0, 0, 0, 0),
}

# -------------------------------------------------------------- canvas -----
W, H = 1024, 1024
PAPER = (255, 255, 255)
INK = (17, 17, 17)
GRAY = (74, 74, 74)
RED = (185, 28, 28)
BLUE = (30, 58, 138)
LIGHT = (242, 242, 240)
RULE = (196, 196, 196)


class Canvas:
    def __init__(self, w=W, h=H):
        self.w = w
        self.h = h
        self.px = bytearray([255]) * (w * h * 3)

    def rect(self, x, y, w, h, color):
        r, g, b = color
        for yy in range(y, y + h):
            base = (yy * self.w + x) * 3
            for xx in range(w):
                o = base + xx * 3
                self.px[o] = r
                self.px[o + 1] = g
                self.px[o + 2] = b

    def border(self, x, y, w, h, color, t=1):
        self.rect(x, y, w, t, color)
        self.rect(x, y + h - t, w, t, color)
        self.rect(x, y, t, h, color)
        self.rect(x + w - t, y, t, h, color)

    def text(self, x, y, s, scale, color):
        for i, ch in enumerate(s):
            glyph = FONT[ch]
            cx = x + i * 6 * scale
            for row in range(7):
                bits = glyph[row]
                for col in range(5):
                    if bits & (1 << (4 - col)):
                        self.rect(cx + col * scale, y + row * scale,
                                  scale, scale, color)

    def text_w(self, s, scale):
        return len(s) * 6 * scale - scale

    def text_right(self, x_right, y, s, scale, color):
        self.text(x_right - self.text_w(s, scale), y, s, scale, color)

    def text_center(self, cx, y, s, scale, color):
        self.text(cx - self.text_w(s, scale) // 2, y, s, scale, color)


# ----------------------------------------------------------------- png -----
def write_png(path, canvas):
    raw = b"".join(
        b"\x00" + bytes(canvas.px[y * canvas.w * 3:(y + 1) * canvas.w * 3])
        for y in range(canvas.h)
    )

    def chunk(tag, data):
        out = struct.pack(">I", len(data)) + tag + data
        return out + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)

    ihdr = struct.pack(">IIBBBBB", canvas.w, canvas.h, 8, 2, 0, 0, 0)
    png = (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr)
           + chunk(b"IDAT", zlib.compress(raw, 9)) + chunk(b"IEND", b""))
    with open(path, "wb") as f:
        f.write(png)
    return len(png)

# -------------------------------------------------------------- stories -----
# Each story: (headline <= 32 chars, deck <= 39 chars, date).
# Headlines are uppercase; decks are uppercase too (the font is caps-only).
SECTIONS = [
    ("EUROPE", [
        ("RUSSIAN MISSILES FALL IN POLAND",
         "Warsaw summons Moscow envoy", "24 NOV"),
        ("RUSSIA WARNS ESTONIA OF WAR",
         "Tallinn to shut border crossings 1 Dec", "23 NOV"),
        ("MI5 WARNS UK ARMS FIRMS",
         "Joint alert over Russian sabotage", "24 NOV"),
        ("EU WARNS 11 STATES ON BUDGETS",
         "Tougher action sought on Hungary", "25 NOV"),
        ("SARKOZY AND WIFE FACE TRIAL",
         "Corruption case; hearing April 2027", "24 NOV"),
    ]),
    ("MIDDLE EAST", [
        ("HOUTHIS STRIKE RIYADH TOP TOWER",
         "Drone attack wounds 11 people", "24 NOV"),
        ("ISRAEL KILLS HAMAS SECURITY BOSS",
         "Naeem Abu Nahal dead in Gaza City", "24 NOV"),
        ("THREE TANKERS ABLAZE IN HORMUZ",
         "Iran says mines hit ships; US escort", "24 NOV"),
        ("US SANCTIONS IRAN-LINKED HOUSES",
         "Treasury targets shadow banking", "24 NOV"),
    ]),
    ("ASIA", [
        ("CHINA PROBES SHANGHAI PARTY BOSS",
         "Chen Jining is 4th Politburo fall", "24 NOV"),
        ("HUAWEI GUILTY IN US TRADE TRIAL",
         "Acquitted of racketeering in US trial", "24 NOV"),
        ("RUSSIAN JETS ENTER KOREA ZONE",
         "Seoul scrambles fighters, issues alert", "24 NOV"),
        ("INDONESIA FIRE TOLL RISES TO 26",
         "Dozens still missing in Cikande", "24 NOV"),
        ("ICJ: MYANMAR COMMITTED GENOCIDE",
         "Ruling on Rohingya; Singapore studies", "24 NOV"),
    ]),
    ("AMERICAS", [
        ("GIULIANI GETS MEDAL OF FREEDOM",
         "Ex-mayor honoured at White House", "24 NOV"),
        ("CIA AND ODNI HIT BY CYBER BREACH",
         "Unclassified data taken, source says", "24 NOV"),
        ("FORT HOOD KILLER SEEKS STAY",
         "Hasan's execution set for next week", "24 NOV"),
        ("US CONSUMER CONFIDENCE SOARS",
         "Best reading in almost two years", "24 NOV"),
    ]),
    ("AFRICA", [
        ("MSF HALTS SOUTH SUDAN OPERATIONS",
         "Staff abducted in Yei River area", "24 NOV"),
        ("EBOLA TEAM TRAPPED IN DR CONGO",
         "DR Congo responders stuck by clashes", "23 NOV"),
        ("ECOWAS PLANS 2027 ONE CURRENCY",
         "Ministers prepare launch plans", "24 NOV"),
        ("GAMBIA STOPS 491 MIGRANT BOAT",
         "Boat stopped en route to Europe", "24 NOV"),
    ]),
    ("OCEANIA", [
        ("SOLOMONS DITCHES CHINA PACT",
         "Treaty with Australia due today", "25 NOV"),
        ("FIJI DROUGHT SHUTS SCHOOLS",
         "El Nino water crisis may run to 2027", "25 NOV"),
        ("AUSTRALIA BLOCKS VANUATU TREATY",
         "Climate clause kills bipartisanship", "24 NOV"),
    ]),
    ("SPORT & TECH", [
        ("SENEGAL BACK AS AFCON CHAMPIONS",
         "CAS overturns CAF title stripping", "24 NOV"),
        ("SOORYAVANSHI, 15, HITS 204",
         "Fastest List A double hundred ever", "24 NOV"),
        ("ENGLAND LEVEL T20 SERIES 1-1",
         "Eight-wicket win chasing 185", "24 NOV"),
    ]),
    ("ALSO TODAY", [
        ("SHENZHOU-24 CARRIES PAKISTANI",
         "First foreign astronaut aboard", "24 NOV"),
        ("US OCTOBER PCE DATA DUE TODAY",
         "Plus second reading of Q3 GDP", "25 NOV"),
        ("RUSSIA WAR DEATHS NEAR 500,000",
         "Moscow's own figures, BBC reports", "24 NOV"),
        ("TRUMP PARDONS TWO TURKEYS",
         "Freedom and Feathers spared", "24 NOV"),
    ]),
]

MARKETS = [
    ("NASDAQ", -1.5),
    ("NVIDIA", -6.0),
    ("KOSPI", -5.3),
    ("TAIWAN", -5.1),
    ("NIKKEI", -2.9),
]

# -------------------------------------------------------------- layout -----
MARGIN = 24
COL_W = 476
COL_X = (MARGIN, MARGIN + COL_W + 24)
STORY_H = 32          # headline line + deck line + gap
BOX_PAD = 6
HEADER_H = 22


def draw_section(cv, x, y, title, stories):
    """Draw one region box; return its height."""
    box_h = HEADER_H + BOX_PAD + len(stories) * STORY_H + BOX_PAD
    cv.border(x, y, COL_W, box_h, INK, 1)
    cv.rect(x, y, COL_W, HEADER_H, BLUE)
    cv.text(x + 8, y + 4, title, 2, PAPER)
    sy = y + HEADER_H + BOX_PAD
    for headline, deck, date in stories:
        headline = headline.upper()
        deck = deck.upper()
        assert len(headline) <= 32, headline
        assert len(deck) <= 39, deck
        cv.text(x + 8, sy, headline, 2, INK)
        cv.text_right(x + COL_W - 8, sy, date, 2, RED)
        cv.text(x + 8, sy + 15, deck, 2, GRAY)
        sy += STORY_H
    return box_h


def build():
    cv = Canvas()

    # Masthead
    cv.text_center(W // 2, 10, "THE WORLD TODAY", 6, INK)
    cv.text_center(W // 2, 58, "WEDNESDAY 25 NOVEMBER 2026", 2, INK)
    cv.rect(MARGIN, 76, W - 2 * MARGIN, 3, RED)
    cv.rect(MARGIN, 81, W - 2 * MARGIN, 1, INK)

    # Lead story (left) + market panel (right)
    cv.text(MARGIN, 90, "TRADE WAR", 2, RED)
    cv.text(MARGIN, 112, "TRUMP TARIFF THREAT", 4, INK)
    cv.text(MARGIN, 140, "SINKS WORLD MARKETS", 4, INK)
    cv.text(MARGIN, 176, "USTR TO UNVEIL FINDINGS ON CHINA AND 16", 2, GRAY)
    cv.text(MARGIN, 192, "PARTNERS; NEW DUTIES MAY FOLLOW IN DAYS.", 2, GRAY)

    px, py, pw, ph = 640, 88, 360, 126
    cv.border(px, py, pw, ph, INK, 1)
    cv.rect(px, py, pw, 24, INK)
    cv.text(px + 10, py + 5, "MARKETS TUMBLE", 2, PAPER)
    cv.text(px + 10, py + 30, "US CLOSE TUE 24 NOV - ASIA WED 25 NOV", 1, GRAY)
    by = py + 46
    for name, val in MARKETS:
        cv.text(px + 10, by, name, 2, INK)
        bar_w = int(abs(val) / 6.0 * 150)
        cv.rect(px + 130, by + 2, bar_w, 10, RED)
        cv.text_right(px + pw - 10, by, "%+.1f%%" % val, 2, RED)
        by += 17

    # War-at-sea strip
    sy = 222
    cv.rect(MARGIN, sy, W - 2 * MARGIN, 52, LIGHT)
    cv.rect(MARGIN, sy, 8, 52, RED)
    cv.text(MARGIN + 16, sy + 6, "ZELENSKY: UKRAINE SANK RUSSIAN SHIP OFF LIBYA",
            3, INK)
    cv.text(MARGIN + 16, sy + 32,
            "SEVEN NAVAL DRONES HIT A CORVETTE, A HELICOPTER AND A CARGO SHIP OFF BENGHAZI.",
            2, GRAY)

    # Region grid: 2 columns x 4 rows
    gy = 282
    rows = [(0, 1), (2, 3), (4, 5), (6, 7)]
    for li, ri in rows:
        h = 0
        for idx, cx in ((li, COL_X[0]), (ri, COL_X[1])):
            title, stories = SECTIONS[idx]
            h = max(h, draw_section(cv, cx, gy, title, stories))
        gy += h + 4
    grid_bottom = gy - 4
    assert grid_bottom <= 1010, grid_bottom

    # Footer
    cv.text_center(W // 2, 1013,
                   "ALL STORIES DATED 23-25 NOVEMBER 2026 - SOURCES: REUTERS, AP, BBC, CNA, PINA",
                   1, GRAY)
    return cv


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    outdir = os.path.join(here, "output")
    os.makedirs(outdir, exist_ok=True)
    cv = build()
    path = os.path.join(outdir, "entry.png")
    size = write_png(path, cv)
    with open(path, "rb") as f:
        digest = hashlib.sha256(f.read()).hexdigest()
    print("wrote %s (%d bytes, sha256 %s)" % (path, size, digest))


if __name__ == "__main__":
    main()
