import random
from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.tags import MemeTags

img_dir = Path(__file__).parent / "images"


def throw(images: list[BuildImage], texts, args):
    img = (
        images[0]
        .convert("RGBA")
        .circle()
        .rotate(random.randint(1, 360))
        .resize((143, 143))
    )
    frame = BuildImage.open(img_dir / "0.png")
    frame.paste(img, (15, 178), alpha=True)
    return frame.save_jpg()


add_meme(
    "throw",
    throw,
    min_images=1,
    max_images=1,
    keywords=["丢", "扔"],
    tags=MemeTags.touhou,
    date_created=datetime(2021, 5, 5),
    date_modified=datetime(2023, 3, 30),
)
