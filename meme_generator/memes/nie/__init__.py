from pathlib import Path
from typing import List

from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.utils import make_jpg_or_gif

img_dir = Path(__file__).parent / "images"


def nie(images: List[BuildImage], texts, args):
    frame = BuildImage.open(img_dir / "0.png")

    def make(img: BuildImage) -> BuildImage:
        points = ((151, 0), (308, 0), (308, 151), (151, 151))
        screen = (
            img.convert("RGBA").resize((308, 151), keep_ratio=True).perspective(points)
        )
        return frame.paste(img.resize((160, 160)), (150, 0), below=True)

    return make_jpg_or_gif(images[0], make)


add_meme("nie", nie, min_images=1, max_images=1, keywords=["捏", "捏脸", "nie"])