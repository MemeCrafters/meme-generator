from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.utils import make_png_or_gif

img_dir = Path(__file__).parent / "images"


def stare_at_you(images: list[BuildImage], texts, args):
    frame = BuildImage.new("RGBA", (400, 400), "white")
    frame.draw_text(
        (10, 0, 150, 100),
        "我雇了一只",
        halign="right",
        max_fontsize=30,
        font_style="bold",
    )
    frame.draw_text(
        (250, 0, 390, 100),
        "来盯着👁你",
        halign="left",
        max_fontsize=30,
        font_style="bold",
    )

    def make(imgs: list[BuildImage]) -> BuildImage:
        img = imgs[0].convert("RGBA").resize((400, 300), keep_ratio=True)
        thumbnail = imgs[0].convert("RGBA").resize((80, 60), keep_ratio=True)
        return (
            frame.copy()
            .paste(img, (0, 100), alpha=True)
            .paste(thumbnail, (160, 20), alpha=True)
        )

    return make_png_or_gif(images, make)


add_meme(
    "stare_at_you",
    stare_at_you,
    min_images=1,
    max_images=1,
    keywords=["盯着你"],
    date_created=datetime(2025, 1, 28),
    date_modified=datetime(2025, 2, 2),
)
