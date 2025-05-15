from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage

from meme_generator import add_meme

img_dir = Path(__file__).parent / "images"


def capoo_nibudongla(images: list[BuildImage], texts, args):
    user_img = images[0].convert("RGBA").resize((142, 139), keep_ratio=True)
    frame = BuildImage.open(img_dir / "0.png")
    frame.paste(user_img, (217, 181), below=True)
    return frame.save_jpg()


add_meme(
    "capoo_nibudongla",
    capoo_nibudongla,
    min_images=1,
    max_images=1,
    keywords=["你不懂啦"],
    date_created=datetime(2025, 5, 15),
    date_modified=datetime(2025, 5, 15),
)
