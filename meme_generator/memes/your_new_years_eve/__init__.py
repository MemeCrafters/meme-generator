from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage

from meme_generator import add_meme

img_dir = Path(__file__).parent / "images"


def my_newyear(images: list[BuildImage], texts: list[str], args):
    frame = BuildImage.open(img_dir / "0.png")
    img = images[0].convert("RGBA").resize((586,430),inside=True,keep_ratio=True)
    frame.paste(img,(0,650),alpha=True,below=True)
    return frame.save_jpg()


add_meme(
    "my_newyear",
    my_newyear,
    min_images=1,
    max_images=1,
    keywords=["你的跨年"],
    date_created=datetime(2024,12,31),
    date_modified=datetime(2024,12,31),
)
