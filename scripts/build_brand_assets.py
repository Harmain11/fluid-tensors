"""Generate a deterministic, researcher-owned visual brand; no AI-generated chart data."""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1] / "docs"
ASSETS = ROOT / "assets"
PAPER = "#f7f4ed"
INK = "#172632"
COBALT = "#3658d4"
CORAL = "#e97759"


def font(name: str, size: int):
    candidates = {
        "serif": ["/usr/share/fonts/truetype/liberation2/LiberationSerif-Regular.ttf", "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"],
        "serif_italic": ["/usr/share/fonts/truetype/liberation2/LiberationSerif-Italic.ttf", "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"],
        "sans": ["/usr/share/fonts/truetype/open-sans/OpenSans-Regular.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"],
        "sans_bold": ["/usr/share/fonts/truetype/open-sans/OpenSans-Bold.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"],
        "mono": ["/usr/share/fonts/truetype/liberation2/LiberationMono-Regular.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"],
    }
    for candidate in candidates[name]:
        if Path(candidate).is_file():
            return ImageFont.truetype(candidate, size)
    return ImageFont.load_default(size=size)


def badge(draw, left, top, size):
    draw.rounded_rectangle((left, top, left + size, top + size), radius=int(size * .24), fill=COBALT)
    draw.text((left + size*.18, top + size*.075), "f", font=font("serif_italic", int(size*.75)), fill=PAPER)
    draw.ellipse((left + size*.57, top + size*.58, left + size*.65, top + size*.66), fill=CORAL)
    draw.text((left + size*.64, top + size*.13), "t", font=font("serif_italic", int(size*.65)), fill=PAPER)


def cover():
    width, height = 1280, 640
    image = Image.new("RGB", (width, height), PAPER)
    draw = ImageDraw.Draw(image)

    # A restrained editorial texture: linework remains outside the labels and chart.
    for shift in range(0, 530, 44):
        draw.arc((-320 + shift, -340 + shift//2, 400 + shift, 440 + shift//2), start=50, end=200, fill="#e0e3dc", width=2)
    badge(draw, 74, 52, 62)
    draw.text((153, 58), "F L U I D   T E N S O R S", font=font("sans_bold", 18), fill=INK)
    draw.text((154, 87), "INDEPENDENT ML RESEARCH  /  2026", font=font("mono", 13), fill="#67777d")
    draw.line((75, 141, 1205, 141), fill="#cbd0ca", width=2)

    draw.text((73, 176), "One frozen edit.", font=font("serif", 78), fill=INK)
    draw.text((72, 263), "Four ways to ask.", font=font("serif_italic", 78), fill=COBALT)
    draw.rounded_rectangle((77, 382, 130, 387), radius=3, fill=CORAL)
    draw.text((77, 408), "A transformer weight intervention", font=font("sans", 23), fill="#344650")
    draw.text((77, 444), "measured under four prompt conditions.", font=font("sans", 23), fill="#344650")
    draw.text((78, 511), "32 QUESTIONS   /   1,024 ARCHIVED CELLS", font=font("mono", 15), fill="#5f6e75")

    # Accurate four-condition scientific comparison: width proportional to |Δ|.
    left, top, right, bottom = 779, 178, 1203, 499
    draw.rounded_rectangle((left, top, right, bottom), radius=18, fill=INK)
    draw.text((804, 205), "FIG. 01   /   SIGNED EDIT", font=font("mono", 13), fill="#bed0d6")
    draw.text((804, 228), "Math + format − generic", font=font("sans", 15), fill="#9ab0bd")
    xzero, half_span, row_h = 1046, 110, 51
    for i, (label, value) in enumerate((("Original", .205542), ("Reworded", -.020673), ("Formal", -.045819), ("Terse", -.002337))):
        y = 290 + i*row_h
        draw.text((803, y-8), label, font=font("sans", 15), fill="#f3f0e9")
        draw.line((xzero-half_span, y+12, xzero+half_span, y+12), fill="#4b6172", width=1)
        draw.line((xzero, y-8, xzero, y+29), fill="#bed0d6", width=2)
        magnitude = abs(value)/.25*half_span
        if value >= 0:
            draw.rounded_rectangle((xzero, y+3, xzero + magnitude, y+22), radius=5, fill="#a6b8ff")
        else:
            draw.rounded_rectangle((xzero-magnitude, y+3, xzero, y+22), radius=3, fill="#ec947a")
    draw.text((805, 472), "ATTENUATION CONTRAST  ≠  ANSWER ACCURACY", font=font("mono", 10), fill="#89a1b0")
    draw.line((75, 566, 1205, 566), fill="#cbd0ca", width=2)
    draw.text((76, 586), "HARMAIN DASTGIR  /  WORKING PREPRINT", font=font("mono", 14), fill="#576b73")
    draw.text((910, 586), "DOI: 10.5281/zenodo.24280041", font=font("mono", 13), fill=COBALT)
    image.save(ASSETS / "social-cover.png", optimize=True)


def icons():
    canvas = Image.new("RGBA", (256, 256), (0,0,0,0))
    draw = ImageDraw.Draw(canvas)
    badge(draw, 12, 12, 232)
    canvas.resize((180, 180), Image.Resampling.LANCZOS).save(ROOT / "apple-touch-icon.png")
    canvas.save(ROOT / "favicon.ico", format="ICO", sizes=[(16,16),(32,32),(48,48),(64,64)])


if __name__ == "__main__":
    cover()
    icons()
    print(f"Created {ASSETS / 'social-cover.png'} and matching app/favicon icons")
