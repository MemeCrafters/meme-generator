import random
from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.utils import FrameAlignPolicy, Maker, make_gif_or_combined_gif

img_dir = Path(__file__).parent / "images"


def remote_control(images: list[BuildImage], texts, args):
    def maker(i: int) -> Maker:
        def make(imgs: list[BuildImage]) -> BuildImage:
            img = imgs[0].convert("RGBA")
            img_w = min(img.width, 500)
            img = img.resize_width(img_w)
            img_w, img_h = img.size

            frame = BuildImage.new("RGBA", (img_w, img_h), (0, 0, 0, 0))
            if i < 4:
                pos = (0, 0)
            else:
                dx = int(img_w * (random.random() - 0.5) / 30)
                dy = int(img_h * (random.random() - 0.5) / 30)
                pos = (dx, dy)
            frame.paste(img, pos, alpha=True)
            overlay = BuildImage.open(img_dir / f"{i}.png")
            overlay = overlay.resize_height(int(img_h / 1.5))
            x = img_w - overlay.width
            y = img_h - overlay.height
            frame.paste(overlay, (x, y), alpha=True)

            return frame

        return make

    return make_gif_or_combined_gif(
        images, maker, 17, 0.07, FrameAlignPolicy.extend_loop
    )


add_meme(
    "remote_control",
    remote_control,
    min_images=1,
    max_images=1,
    keywords=["遥控", "控制"],
    date_created=datetime(2025, 3, 4),
    date_modified=datetime(2025, 3, 24),
)
