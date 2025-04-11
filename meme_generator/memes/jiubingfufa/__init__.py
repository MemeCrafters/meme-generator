from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.exception import TextOverLength
from meme_generator.utils import Maker, make_gif_or_combined_gif

img_dir = Path(__file__).parent / "images"

default_text = "此乃旧病复发也"


def jiubingfufa(images: list[BuildImage], texts: list[str], args):
    text = texts[0] if texts else default_text

    def maker(i: int) -> Maker:
        def make(imgs: list[BuildImage]) -> BuildImage:
            frame = BuildImage.open(img_dir / f"{i}.jpg").convert("RGBA")
            img = imgs[0].convert("RGBA").circle().resize((120, 120))
            frame.paste(img, (32, frame.height - 162), alpha=True)
            if i > 9:
                try:
                    frame.draw_text(
                        (0, 0, 290, 160),
                        text,
                        max_fontsize=32,
                        fill="white",
                        stroke_fill="black",
                        stroke_ratio=0.05,
                    )
                except ValueError:
                    raise TextOverLength(text)
            return frame

        return make

    return make_gif_or_combined_gif(images, maker, 26, 0.06)


add_meme(
    "jiubingfufa",
    jiubingfufa,
    max_images=1,
    min_images=1,
    max_texts=1,
    min_texts=0,
    default_texts=[default_text],
    keywords=["旧病复发"],
    date_created=datetime(2025, 4, 1),
    date_modified=datetime(2025, 4, 11),
)
