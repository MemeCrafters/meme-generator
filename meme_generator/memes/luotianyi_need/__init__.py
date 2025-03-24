from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.tags import MemeTags
from meme_generator.utils import make_jpg_or_gif

img_dir = Path(__file__).parent / "images"


def luotianyi_need(images: list[BuildImage], texts: list[str], args):
    frame = BuildImage.open(img_dir / "0.png")

    def make(imgs: list[BuildImage]) -> BuildImage:
        img = imgs[0].convert("RGBA").resize((195, 195), keep_ratio=True, inside=True)
        return frame.copy().paste(img, (43, 146), alpha=True)

    return make_jpg_or_gif(images, make)


add_meme(
    "luotianyi_need",
    luotianyi_need,
    min_images=1,
    max_images=1,
    min_texts=0,
    max_texts=0,
    keywords=["洛天依要", "天依要"],
    tags=MemeTags.luotianyi,
    date_created=datetime(2025, 2, 11),
    date_modified=datetime(2025, 2, 11),
)
