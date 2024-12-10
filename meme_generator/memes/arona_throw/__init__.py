from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.tags import MemeTags
from meme_generator.utils import FrameAlignPolicy, Maker, make_gif_or_combined_gif

img_dir = Path(__file__).parent / "images"


def arona_throw(images: list[BuildImage], texts, args):
    position_list = [
        (270, 295),
        (154, 291),
        (154, 291),
        (89, 211),
        (41, 195),
        (28, 192),
        (16, 200),
        (-10, 206),
        (-40, 210),
        (-80, 214),
        (324, 245),
        (324, 256),
        (331, 251),
        (331, 251),
        (318, 260),
        (318, 260),
    ]
    position_list2 = [
        (324, 15),
        (324, 106),
        (324, 161),
        (324, 192),
    ]

    def maker(i: int) -> Maker:
        def make(imgs: list[BuildImage]) -> BuildImage:
            pyroxenes = (
                imgs[0].convert("RGBA").resize((120, 120), keep_ratio=True).circle()
            )
            arona = BuildImage.open(img_dir / f"{i}.png").convert("RGBA")
            arona.paste(pyroxenes, position_list[i], alpha=True)
            if i in [6, 7, 8, 9]:
                arona.paste(pyroxenes, position_list2[i - 6], alpha=True)
            return arona

        return make

    return make_gif_or_combined_gif(images, maker, 16, 0.04, FrameAlignPolicy.no_extend)


add_meme(
    "arona_throw",
    arona_throw,
    min_images=1,
    max_images=1,
    keywords=["阿罗娜扔"],
    tags=MemeTags.arona,
    date_created=datetime(2024, 12, 10),
    date_modified=datetime(2024, 12, 10),
)
