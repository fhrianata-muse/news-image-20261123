#!/usr/bin/env python3
"""Draw the 23 November 2026 front page: one 1024x1024 PNG, fully deterministic.

No network, no clock, no randomness. Running this twice writes identical bytes.
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W = 1024
H = 1024
OUT = "entry.png"

PAPER = (248, 244, 233)
INK = (17, 17, 17)
RED = (178, 28, 28)
NAVY = (30, 58, 95)
GREY = (90, 86, 76)
LIGHT_RULE = (190, 182, 164)
BLUE = (42, 92, 150)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap to a pixel width; returns list of lines."""
    words = text.split()
    lines = []
    cur = ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_lines(draw, lines, x, y, fnt, fill, leading):
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    mx = 28  # margin

    # ---- Masthead -------------------------------------------------------
    f_mast = font(SERIF_B, 56)
    title = "THE WORLD IN ONE DAY"
    tw = d.textlength(title, font=f_mast)
    d.text(((W - tw) / 2, 18), title, font=f_mast, fill=INK)
    f_sub = font(SANS, 15)
    sub = "ONE DAY  •  EVERY CONTINENT  •  ONE FRONT PAGE"
    sw = d.textlength(sub, font=f_sub)
    d.text(((W - sw) / 2, 86), sub, font=f_sub, fill=GREY)
    d.line([(mx, 112), (W - mx, 112)], fill=INK, width=3)
    d.line([(mx, 117), (W - mx, 117)], fill=INK, width=1)

    # ---- Date banner ----------------------------------------------------
    d.rectangle([mx, 126, W - mx, 162], fill=RED)
    f_date = font(SANS_B, 28)
    date = "MONDAY  23  NOVEMBER  2026"
    dw = d.textlength(date, font=f_date)
    d.text(((W - dw) / 2, 132), date, font=f_date, fill=(255, 255, 255))

    # ---- Lead story: COP31 ----------------------------------------------
    lx, ly = mx, 178
    lw = 600  # lead text width
    f_kick = font(SANS_B, 16)
    d.text((lx, ly), "CLIMATE  —  ANTALYA, TÜRKİYE", font=f_kick, fill=RED)
    f_head = font(SERIF_B, 48)
    y = ly + 26
    y = draw_lines(d, ["COP31 COLLAPSES", "WITH NO DEAL"], lx, y, f_head, INK, 54)
    f_deck = font(SERIF, 21)
    deck = ("Two weeks of talks end in deadlock as 194 nations reject the "
            "Antalya Pact — the longest COP in history.")
    y = draw_lines(d, wrap(d, deck, f_deck, lw), lx, y + 6, f_deck, INK, 28) + 8
    f_bullet = font(SANS, 17)
    bullets = [
        "EU and Britain refuse a text with no fossil fuels.",
        "UN chief “deeply disappointed”; 44 hours into overtime.",
        "90+ nations still sign a pledge to electrify economies.",
    ]
    for b in bullets:
        lines = wrap(d, b, f_bullet, lw - 22)
        d.text((lx, y), "▪", font=f_bullet, fill=RED)
        y = draw_lines(d, lines, lx + 22, y, f_bullet, INK, 23)
        y += 2

    # Lead graphic: globe with a crack, right of the lead text.
    gx, gy = 668, 186
    d.ellipse([gx, gy, gx + 150, gy + 150], outline=NAVY, width=4, fill=(214, 230, 242))
    d.ellipse([gx + 22, gy + 22, gx + 128, gy + 128], outline=NAVY, width=2)
    d.line([(gx + 75, gy), (gx + 75, gy + 150)], fill=NAVY, width=2)
    d.line([(gx, gy + 75), (gx + 150, gy + 75)], fill=NAVY, width=2)
    d.arc([gx + 8, gy + 40, gx + 142, gy + 110], start=200, end=340, fill=NAVY, width=2)
    crack = [(gx + 60, gy + 6), (gx + 78, gy + 40), (gx + 62, gy + 72),
             (gx + 88, gy + 104), (gx + 70, gy + 144)]
    d.line(crack, fill=RED, width=5, joint="curve")
    f_cap = font(SANS_B, 15)
    cap = "LONGEST COP EVER"
    cw = d.textlength(cap, font=f_cap)
    d.text((gx + 75 - cw / 2, gy + 158), cap, font=f_cap, fill=RED)
    f_cap2 = font(SANS, 14)
    cap2 = "First collapse since Copenhagen 2009"
    cw2 = d.textlength(cap2, font=f_cap2)
    d.text((gx + 75 - cw2 / 2, gy + 180), cap2, font=f_cap2, fill=GREY)

    # ---- Divider ----------------------------------------------------------
    d.line([(mx, 464), (W - mx, 464)], fill=INK, width=2)

    # ---- 3x3 grid of stories --------------------------------------------
    cards = [
        ("GULF",
         "Iran hits U.S. bases in Bahrain",
         "Bahrain asks the UN to act after strikes on bases and a civilian "
         "site; Houthi drones hit Riyadh a third day."),
        ("STRAIT OF HORMUZ",
         "Tankers struck as Gulf oil flow falls",
         "Ships hit in and around the strait; U.S. and China talk over "
         "shipping and energy risks."),
        ("UKRAINE",
         "Drone hits Kyiv region; 14 missing",
         "New footage shows blasts moments before part of the Crimea "
         "Bridge collapses."),
        ("GULF OF FINLAND",
         "Russian cargo ship still burning",
         "Vessel ablaze off Finland after a drone attack; fire crews "
         "stand by as the hull smoulders."),
        ("GAZA",
         "Nine killed in Gaza in 48 hours",
         "Toll since the October 2025 ceasefire reaches 1,661, as "
         "strikes continue across the Strip."),
        ("SPACE",
         "BepiColombo reaches Mercury",
         "Europe-Japan probe enters orbit around the smallest planet "
         "after an eight-year journey."),
        ("WASHINGTON",
         "Pentagon releases 43 UAP files",
         "Declassified files include three Middle East military videos; "
         "every case stays unresolved."),
        ("UNITED NATIONS",
         "Lethal-weapons talks go on",
         "Nations agree to keep negotiating autonomous arms; no binding "
         "rules before 2028."),
        ("ASIA",
         "Nepal PM meets Modi in Delhi",
         "South Korea minister quits over AI exam cheating; 50 missing "
         "in an Indonesia factory fire."),
    ]
    grid_x, grid_y = mx, 480
    cw_, ch_ = 312, 134
    gap_x, gap_y = 16, 11
    f_ck = font(SANS_B, 14)
    f_ch = font(SERIF_B, 20)
    f_cd = font(SANS, 14)
    for i, (kicker, head, deck) in enumerate(cards):
        cx = grid_x + (i % 3) * (cw_ + gap_x)
        cy = grid_y + (i // 3) * (ch_ + gap_y)
        d.line([(cx, cy), (cx + cw_, cy)], fill=RED, width=2)
        d.text((cx, cy + 8), kicker, font=f_ck, fill=RED)
        hy = draw_lines(d, wrap(d, head, f_ch, cw_), cx, cy + 30, f_ch, INK, 24)
        draw_lines(d, wrap(d, deck, f_cd, cw_), cx, hy + 2, f_cd, (60, 58, 52), 19)

    # ---- Footer ticker ----------------------------------------------------
    ty = 912
    d.rectangle([mx, ty, W - mx, ty + 52], fill=NAVY)
    f_tick = font(SANS_B, 16)
    tick = ("COP31: NO DEAL  •  GULF STRIKES WIDEN  •  NIGERIA BOAT SINKS, 24 DEAD  •  "
            "TRUMP SEEKS PERMANENT IRAN NUCLEAR DEAL  •  INDIA 720/9 IN WELLINGTON")
    tlines = wrap(d, tick, f_tick, W - 2 * mx - 24)
    yy = ty + 7
    for line in tlines:
        d.text((mx + 12, yy), line, font=f_tick, fill=(255, 255, 255))
        yy += 20

    # ---- Source line ------------------------------------------------------
    f_src = font(SANS, 13)
    src = "The day's news as reported on Monday 23 November 2026  •  Sources: CNN, Reuters, Le Monde, Al Jazeera, BBC"
    sw = d.textlength(src, font=f_src)
    d.text(((W - sw) / 2, 980), src, font=f_src, fill=GREY)

    img.save(OUT, format="PNG", optimize=False)


if __name__ == "__main__":
    main()
