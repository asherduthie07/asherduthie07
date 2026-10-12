"""Generate the grayscale pixel animations used by the profile README.

Requires Pillow: python3 -m pip install pillow
Run from the repository root: python3 scripts/build_art.py
"""

from __future__ import annotations

import math
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets"
OUT.mkdir(exist_ok=True)
SCALE = 2
FRAMES = 36
INK = (9, 10, 12)
PANEL = (17, 18, 21)
MID = (69, 72, 78)
SOFT = (138, 141, 147)
LIT = (223, 225, 228)
WHITE = (247, 247, 247)


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    paths = (
        ["/System/Library/Fonts/Supplemental/Menlo Bold.ttf", "/System/Library/Fonts/Supplemental/Courier New Bold.ttf"]
        if bold else
        ["/System/Library/Fonts/Supplemental/Menlo Regular.ttf", "/System/Library/Fonts/Supplemental/Courier New.ttf"]
    )
    paths += ["/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"]
    for path in paths:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


F8 = font(8)
F9 = font(9, True)
F11 = font(11, True)
F35 = font(35, True)


def text(draw: ImageDraw.ImageDraw, xy: tuple[int, int], label: str, color=SOFT, face=F8):
    draw.text(xy, label, fill=color, font=face, stroke_width=0)


def frame(width: int, height: int, label: str) -> tuple[Image.Image, ImageDraw.ImageDraw]:
    im = Image.new("RGB", (width, height), INK)
    d = ImageDraw.Draw(im)
    d.rectangle((3, 3, width - 4, height - 4), outline=MID, width=1)
    d.rectangle((8, 8, width - 9, height - 9), outline=(31, 33, 37), width=1)
    for x in range(13, width - 11, 8):
        d.point((x, 3), fill=SOFT if x % 40 == 13 else MID)
    text(d, (17, 12), label, SOFT, F8)
    return im, d


def rain(d: ImageDraw.ImageDraw, t: int, width: int, height: int, seed: int, count: int):
    rng = random.Random(seed)
    for _ in range(count):
        x = rng.randrange(12, width - 12)
        y0 = rng.randrange(8, height + 20)
        speed = rng.choice((2, 3, 4))
        y = (y0 + t * speed) % (height - 17) + 9
        color = (46, 49, 54) if x < 270 else (77, 80, 85)
        d.line((x, y, x, min(y + rng.choice((2, 3, 5)), height - 10)), fill=color)


def building(d: ImageDraw.ImageDraw, x: int, top: int, width: int, height: int, t: int, index: int):
    d.rectangle((x, top, x + width, height), fill=(25, 27, 30))
    d.line((x, top, x + width, top), fill=(80, 83, 88), width=1)
    d.rectangle((x + 5, top - 5, x + 7, top), fill=MID)
    for wy in range(top + 9, height - 3, 12):
        for wx in range(x + 6, x + width - 5, 10):
            if ((wx * 13 + wy * 7 + index) % 5) < 3:
                glow = (142, 145, 149) if (t // 6 + wx + wy) % 7 else LIT
                d.rectangle((wx, wy, wx + 2, wy + 3), fill=glow)


def walker(d: ImageDraw.ImageDraw, x: int, y: int, t: int):
    # A tiny two-frame sprite with a coat, pale face, and alternating steps.
    d.rectangle((x + 4, y, x + 9, y + 2), fill=SOFT)
    d.rectangle((x + 3, y + 3, x + 10, y + 7), fill=LIT)
    d.rectangle((x + 2, y + 8, x + 11, y + 16), fill=(85, 88, 93))
    d.rectangle((x + 1, y + 10, x + 2, y + 16), fill=SOFT)
    d.rectangle((x + 11, y + 10, x + 12, y + 16), fill=SOFT)
    if t % 8 < 4:
        d.rectangle((x + 3, y + 17, x + 5, y + 21), fill=LIT)
        d.rectangle((x + 9, y + 17, x + 12, y + 19), fill=LIT)
    else:
        d.rectangle((x + 2, y + 17, x + 5, y + 19), fill=LIT)
        d.rectangle((x + 9, y + 17, x + 11, y + 21), fill=LIT)


def hero(t: int) -> Image.Image:
    im, d = frame(480, 180, "//  ASHER_DUTHIE.exe                         PROFILE / 001")
    # The skyline, moon, rain, signal lamp, and sprite each animate independently.
    d.ellipse((367, 28, 429, 90), fill=(31, 33, 37))
    d.ellipse((378, 39, 418, 79), fill=(188, 190, 193))
    d.ellipse((383, 42, 421, 78), fill=(215, 216, 217))
    d.rectangle((335 + t // 5, 51, 429 + t // 5, 54), fill=(29, 31, 35))
    d.rectangle((347 - t // 7, 67, 447 - t // 7, 70), fill=(35, 37, 40))
    for i, (x, y, w) in enumerate(((280, 88, 36), (311, 70, 43), (348, 99, 31), (375, 83, 41), (411, 103, 38), (446, 74, 29))):
        building(d, x, y, w, 158, t, i)
    d.rectangle((275, 157, 474, 160), fill=MID)
    d.line((281, 162, 467, 162), fill=(35, 38, 42))
    walker(d, 312 + (t * 2) % 135, 135, t)
    rain(d, t, 480, 159, 2514, 66)
    # A heavy black text panel gives the title a clean silhouette over the weather.
    d.rectangle((17, 31, 272, 136), fill=(12, 13, 16))
    d.line((17, 31, 273, 31), fill=(65, 68, 73))
    d.rectangle((25, 42, 28, 46), fill=WHITE if t % 12 < 7 else MID)
    text(d, (34, 39), "TRANSMISSION FOUND", SOFT, F9)
    # One-frame glitch ghosts create a deliberately sharp, pixelated flash.
    if t in (5, 18, 29):
        text(d, (31, 55), "ASHER", MID, F35)
        text(d, (33, 92), "DUTHIE", MID, F35)
        d.rectangle((103, 84, 244, 86), fill=MID)
    text(d, (26, 53), "ASHER", WHITE, F35)
    text(d, (26, 90), "DUTHIE", LIT, F35)
    d.rectangle((26, 132, 264, 133), fill=MID)
    d.rectangle((26, 132, 26 + (t * 9) % 238, 133), fill=WHITE)
    d.rectangle((12, 143, 269, 169), fill=PANEL)
    d.rectangle((13, 144, 268, 168), outline=MID)
    text(d, (20, 151), "> FULL-STACK  /  SECURITY  /  GAME DEV", LIT, F9)
    d.rectangle((294, 22, 472, 37), fill=PANEL)
    text(d, (302, 25), "STATUS : STILL EXPLORING", LIT, F8)
    d.rectangle((461, 26, 465, 30), fill=WHITE if t % 10 < 5 else MID)
    for i in range(8):
        d.rectangle((391 + i * 9, 167, 395 + i * 9, 169), fill=SOFT if (i + t // 3) % 8 < 3 else MID)
    return im


def frequency(t: int) -> Image.Image:
    im, d = frame(480, 56, "//  SIGNAL MONITOR")
    d.rectangle((20, 29, 460, 30), fill=MID)
    for x in range(22, 459, 4):
        distance = abs(x - ((t * 16) % 520 - 20))
        amp = max(1, int(17 * math.exp(-distance / 70) * abs(math.sin((x - t * 12) / 13))))
        d.line((x, 30 - amp // 2, x, 30 + amp // 2), fill=LIT if distance < 50 else SOFT)
    d.rectangle((19, 42, 461, 44), fill=(36, 38, 42))
    d.rectangle((19 + (t * 12) % 400, 42, 59 + (t * 12) % 400, 44), fill=WHITE)
    return im


def domains(t: int) -> Image.Image:
    im, d = frame(480, 98, "//  ACTIVE QUESTS")
    for x, label in ((17, "01  BUILD"), (171, "02  EXPLORE"), (325, "03  PLAY")):
        d.rectangle((x, 28, x + 138, 81), fill=PANEL, outline=MID)
        text(d, (x + 9, 35), label, LIT, F9)
        d.line((x + 9, 50, x + 129, 50), fill=MID)
    # Code window: the caret and the bars march through a tiny program.
    d.rectangle((36, 56, 74, 75), outline=SOFT)
    for row in range(3):
        d.rectangle((41, 59 + row * 5, 47 + (row * 7) % 11, 60 + row * 5), fill=SOFT)
    d.rectangle((52 + (t // 4) % 13, 69, 54 + (t // 4) % 13, 71), fill=WHITE if t % 8 < 5 else MID)
    for i in range(5):
        d.rectangle((87 + i * 10, 73 - (i * 4 + t // 3) % 17, 91 + i * 10, 75), fill=LIT if i == (t // 7) % 5 else MID)
    # Scanner: a lock under a sweeping beam.
    d.arc((224, 56, 241, 72), 180, 360, fill=LIT, width=2)
    d.rectangle((222, 64, 243, 76), fill=SOFT)
    d.rectangle((231, 68, 233, 72), fill=INK)
    sx = 183 + (t * 4) % 121
    d.line((sx, 55, sx, 75), fill=WHITE)
    # Arcade: pixel ship bobs and fires a looping projectile.
    ship_x = 376 + int(6 * math.sin(t / 4))
    d.rectangle((ship_x + 6, 67, ship_x + 17, 72), fill=LIT)
    d.rectangle((ship_x + 10, 63, ship_x + 13, 66), fill=LIT)
    d.rectangle((ship_x + 3, 72, ship_x + 6, 75), fill=SOFT)
    d.rectangle((ship_x + 17, 72, ship_x + 20, 75), fill=SOFT)
    d.rectangle((ship_x + 11, 59 - (t * 2) % 15, ship_x + 12, 61 - (t * 2) % 15), fill=WHITE)
    for i in range(3):
        d.rectangle((431 + i * 7, 65 + ((i + t // 5) % 2) * 4, 433 + i * 7, 67 + ((i + t // 5) % 2) * 4), fill=MID)
    return im


def footer(t: int) -> Image.Image:
    im, d = frame(480, 94, "//  END OF FILE                                       004 / 004")
    rng = random.Random(407)
    for _ in range(56):
        x, y = rng.randrange(17, 462), rng.randrange(25, 75)
        d.rectangle((x, y, x + 1, y + 1), fill=LIT if (x + y + t // 4) % 11 < 3 else MID)
    d.rectangle((18, 46, 463, 48), fill=(36, 38, 42))
    d.rectangle((18, 75, 463, 79), fill=MID)
    for x in range(22, 462, 24):
        d.rectangle((x + (t * 3) % 24, 76, x + 7 + (t * 3) % 24, 78), fill=LIT)
    walker(d, 39 + (t * 11) % 394, 51, t)
    d.rectangle((120, 30, 363, 67), fill=(12, 13, 16))
    d.rectangle((120, 30, 363, 67), outline=MID)
    text(d, (138, 37), "STILL EXPLORING...", WHITE, F11)
    text(d, (165, 53), "ALWAYS WILL BE" + ("_" if t % 10 < 6 else " "), SOFT, F8)
    return im


def save(name: str, generator, duration: int):
    originals = [generator(t) for t in range(FRAMES)]
    images = [im.resize((im.width * SCALE, im.height * SCALE), Image.Resampling.NEAREST) for im in originals]
    images[0].save(
        OUT / name,
        save_all=True,
        append_images=images[1:],
        duration=duration,
        loop=0,
        optimize=True,
        disposal=2,
    )
    print(f"{name}: {(OUT / name).stat().st_size / 1024:.0f} KB")


if __name__ == "__main__":
    save("hero.gif", hero, 85)
    save("frequency.gif", frequency, 75)
    save("domains.gif", domains, 85)
    save("footer.gif", footer, 90)
