import random
from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage, Text2Image

from meme_generator import MemeArgsModel, add_meme
from meme_generator.exception import TextOrNameNotEnough, TextOverLength

img_dir = Path(__file__).parent / "images"


def stop_playing(images: list[BuildImage], texts: list[str], args: MemeArgsModel):
    if not texts:
        texts = ["玩尼玛，不玩了！"]
    else:
        texts = texts[:1]

    if len(images) > len(texts):
        raise TextOrNameNotEnough()

    text = texts[0]

    frame = BuildImage.open(img_dir / "0.png")

    for i, img in enumerate(images):
        img = img.convert("RGBA")
        rotated_img = img.resize((64, 64), keep_ratio=True, inside=True).rotate(20, expand=True)
        x = 140 + random.randint(-10, 10) if i > 0 else 140
        y = 95 + random.randint(-10, 10) if i > 0 else 95
        frame.paste(rotated_img, (x, y), alpha=True)

    try:
        frame.draw_text(
            (50, 190, frame.width - 10, 230),
            text,
            max_fontsize=30,
            min_fontsize=10,
            font_style="bold",
        )
    except ValueError:
        raise TextOverLength(text)

    return frame.save_jpg()


add_meme(
    "stop_playing",
    stop_playing,
    min_images=1,
    max_images=1,
    min_texts=0,
    max_texts=10,
    keywords=["不玩了"],
    date_created=datetime(2025, 3, 26),
    date_modified=datetime(2023, 3, 26),
)
