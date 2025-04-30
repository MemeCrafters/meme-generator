from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage

from meme_generator import add_meme

img_dir = Path(__file__).parent / "images"


def work(images: list[BuildImage], texts, args):
    frame = BuildImage.open(img_dir / "0.jpg").convert("RGBA")
    frame.paste(
        images[0].convert("RGBA").circle().resize((155, 155)), (-7, 260), alpha=True
    )
    return frame.save_jpg()


add_meme(
    "work",
    work,
    min_images=1,
    max_images=1,
    keywords=["干活"],
    date_created=datetime(2025, 4, 30),
    date_modified=datetime(2025, 4, 30),
)
