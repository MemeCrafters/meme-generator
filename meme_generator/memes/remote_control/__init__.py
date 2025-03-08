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
            w, h = img.size

            locs = [
                (0, 0),
                (w // 80, h // 80),
                (-w // 100, -h // 100),
                (w // 60, 0),
                (0, h // 60),
            ]

            frame = BuildImage.new("RGBA", (w, h), (0, 0, 0, 0))
            frame.paste(img, locs[i], alpha=True)

            overlay = BuildImage.open(img_dir / "0.png")
            overlay = overlay.resize_height(int(h / 2.5))
            x = w - overlay.width
            y = h - overlay.height
            frame.paste(overlay, (x, y), alpha=True)

            return frame

        return make

    return make_gif_or_combined_gif(
        images, maker, 5, 0.05, FrameAlignPolicy.extend_loop
    )


add_meme(
    "remote_control",
    remote_control,
    min_images=1,
    max_images=1,
    keywords=["遥控", "控制"],
    date_created=datetime(2025, 3, 4),
    date_modified=datetime(2025, 3, 4),
)
