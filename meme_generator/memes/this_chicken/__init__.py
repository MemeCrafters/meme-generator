import random
from pathlib import Path
from typing import List

from pil_utils import BuildImage

from meme_generator import add_meme

img_dir = Path(__file__).parent / "images"


def this_chichen(images: List[BuildImage], texts, args):
    img = images[0].convert("RGBA").resize((640, 640), keep_ratio=True)

    frame = BuildImage.open(img_dir / "0.png")
    frame.paste(
        img.perspective(((507, 0), (940, 351), (383, 625), (0, 256))),
        (201, 201),
        below=True,
    )
    return frame.save_jpg()


add_meme(
    "this_chichen", this_chichen, min_images=1, max_images=1, keywords=["这是鸡", "🐔"]
)