from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.utils import make_png_or_gif

img_dir = Path(__file__).parent / "images"


def stare_at_you(images: list[BuildImage], texts, args):
    frame = BuildImage.open(img_dir / "0.png")

    def make(imgs: list[BuildImage]) -> BuildImage:
        img = imgs[0].convert("RGBA").resize((405, 305), keep_ratio=True)
        thumbnail = imgs[0].convert("RGBA").resize((70, 50), keep_ratio=True)
        return frame.copy().paste(img, (0,100),alpha=True).paste(thumbnail,(164,25),alpha=True)

    return make_png_or_gif(images, make)


add_meme(
    "stare_at_you",
    stare_at_you,
    min_images=1,
    max_images=1,
    keywords=["盯着你"],
    date_created=datetime(2025, 1, 28),
    date_modified=datetime(2025, 1, 28),
)
