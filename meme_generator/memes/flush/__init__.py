import random
from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.utils import Maker, make_gif_or_combined_gif

img_dir = Path(__file__).parent / "images"


def flush(images: list[BuildImage], texts, args):
    def maker(i: int) -> Maker:
        def make(imgs: list[BuildImage]):
            img = imgs[0].convert("RGBA").square()
            max_width = 282
            if img.width > max_width:
                img = img.resize((max_width, max_width))
            w, h = img.size

            if i >= 18:
                frame = BuildImage.open(img_dir / f"{i - 18}.png")
                return frame.resize((w, h))

            j = 0.2 * (2 * random.random() - 1)  # 抖动
            k = 8 * i  # 变红
            f = 0.01 * i  # 放大
            crop_box = (
                round(w * f + w * f * j),
                round(h * f + h * f * j),
                round(w * (1 - f) + w * f * j),
                round(h * (1 - f) + h * f * j),
            )
            croped_img = img.crop(crop_box)
            frame = BuildImage.new("RGBA", croped_img.size, "white")
            frame.paste(croped_img, (0, 0), alpha=True)
            red_filter = BuildImage.new("RGBA", croped_img.size, (255, 0, 0, k))
            frame.alpha_composite(red_filter)
            return frame.resize((w, h))

        return make

    return make_gif_or_combined_gif(images, maker, 30, 0.08)


add_meme(
    "flush",
    flush,
    min_images=1,
    max_images=1,
    keywords=["红温"],
    date_created=datetime(2024, 9, 3),
    date_modified=datetime(2024, 9, 3),
)
