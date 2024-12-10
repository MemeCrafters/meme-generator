from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.utils import FrameAlignPolicy, Maker, make_gif_or_combined_gif

img_dir = Path(__file__).parent / "images"


def saimin_app(images: list[BuildImage], texts, args):
    app_w, app_h = BuildImage.open(img_dir / "0.png").size
    img_w, img_h = images[0].size
    ratio = 1
    if img_w > img_h:
        frame_h = round(app_h * ratio)
        frame_w = round(frame_h * img_w / img_h)
    else:
        frame_w = round(app_w * ratio)
        frame_h = round(frame_w * img_h / img_w)

    def maker(i: int) -> Maker:
        def make(imgs: list[BuildImage]) -> BuildImage:
            frame = imgs[0].convert("RGBA").resize((frame_w, frame_h), keep_ratio=True)
            app = BuildImage.open(img_dir / f"{i}.png")
            frame.paste(app, (0, frame_h - app_h), alpha=True)
            return frame

        return make

    return make_gif_or_combined_gif(
        images, maker, 25, 0.03, FrameAlignPolicy.extend_loop
    )


add_meme(
    "saimin_app",
    saimin_app,
    min_images=1,
    max_images=1,
    keywords=["催眠app"],
    date_created=datetime(2024, 12, 10),
    date_modified=datetime(2024, 12, 10),
)
