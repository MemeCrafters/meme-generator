from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.utils import FrameAlignPolicy, Maker, make_gif_or_combined_gif

img_dir = Path(__file__).parent / "images"


def sora(images: list[BuildImage], texts, args):
    def maker(i: int) -> Maker:
        def make(imgs: list[BuildImage]) -> BuildImage:
            img = imgs[0].convert("RGBA").resize((480, 270), keep_ratio=True)
            frame = BuildImage.open(img_dir / f"{i}.png")

            frame.paste(img, (0, 0), below=True)
            return frame

        return make

    return make_gif_or_combined_gif(
        images, maker, 41, 0.1, FrameAlignPolicy.extend_first
    )


add_meme(
    "sora",
    sora,
    min_images=1,
    max_images=1,
    keywords=["撕衣服"],
    date_created=datetime(2025, 5, 7),
    date_modified=datetime(2025, 5, 26),
)
