from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.utils import make_jpg_or_gif

img_dir = Path(__file__).parent / "images"


def your_new_years_eve(images: list[BuildImage], texts: list[str], args):
    frame = BuildImage.open(img_dir / "0.png")

    def make(imgs: list[BuildImage]) -> BuildImage:
        img = (
            imgs[0]
            .convert("RGBA")
            .resize((586, 430), inside=True, keep_ratio=True, bg_color="white")
        )
        return frame.copy().paste(img, (0, 650), alpha=True, below=True)

    return make_jpg_or_gif(images, make)


add_meme(
    "your_new_years_eve",
    your_new_years_eve,
    min_images=1,
    max_images=1,
    keywords=["你的跨年"],
    date_created=datetime(2024, 12, 31),
    date_modified=datetime(2024, 12, 31),
)
