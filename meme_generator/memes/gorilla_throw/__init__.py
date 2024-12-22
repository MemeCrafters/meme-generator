from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.utils import FrameAlignPolicy, Maker, make_gif_or_combined_gif

img_dir = Path(__file__).parent / "images"


def gorilla_throw(images: list[BuildImage], texts, args):
    params = [
        (74, 125, 24, 8, -135),  # 28
        (84, 119, 24, 8, -130),  # 29
        (111, 103, 22, 15, -100),  # 30
        (122, 95, 22, 15, -90),  # 31
        (136, 89, 25, 17, -87),  # 32
        (142, 60, 49, 22, -40),  # 33
        (134, 49, 66, 30, -30),  # 34
        (134, 49, 66, 30, -30),  # 35
        (116, 35, 92, 38, -25),  # 36
        (78, 26, 167, 73, -5),  # 37
        (-30, 0, 300, 180, 5),  # 38
        (-120, -85, 400, 240, 16),  # 39
        (-160, -125, 500, 300, 20),  # 40
        (-180, -180, 600, 360, 23),  # 41
    ]

    def maker(i: int) -> Maker:
        def make(imgs: list[BuildImage]) -> BuildImage:
            frame = BuildImage.open(img_dir / f"{i:02d}.png")
            if i < 28:
                return frame
            x, y, w, h, a = params[i - 28]
            nfsq = (
                imgs[0]
                .convert("RGBA")
                .resize((w, h), keep_ratio=True)
                .rotate(a, expand=True)
            )
            frame.paste(nfsq, (x, y), below=False, alpha=True)
            return frame

        return make

    return make_gif_or_combined_gif(images, maker, 42, 0.04, FrameAlignPolicy.no_extend)


add_meme(
    "gorilla_throw",
    gorilla_throw,
    min_images=1,
    max_images=1,
    keywords=["猩猩扔"],
    date_created=datetime(2024, 11, 16),
    date_modified=datetime(2024, 11, 22),
)
