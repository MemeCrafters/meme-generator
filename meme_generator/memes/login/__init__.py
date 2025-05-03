import random
from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage, Text2Image

from meme_generator import MemeArgsModel, add_meme
from meme_generator.exception import TextOrNameNotEnough, TextOverLength

img_dir = Path(__file__).parent / "images"


def login(images: list[BuildImage], texts: list[str], args: MemeArgsModel):
    if not texts:
        texts = ["上号"]
    else:
        texts = texts[:1]

    if len(images) > len(texts):
        raise TextOrNameNotEnough()

    text = texts[0]

    frame = BuildImage.open(img_dir / "0.png")

    for i, img in enumerate(images):
        img = img.convert("RGBA")
        resized_img = img.resize((280, 280), keep_ratio=True, inside=True)
        x = 1080 - 280 - 40
        y = 40
        frame.paste(resized_img, (x, y), alpha=True)

    try:
        text_w = Text2Image.from_text(text, 140).longest_line
        text_x = 239 - 100 + (500 - text_w) // 2
        text_y = frame.height - 20 - 140 - 10
        frame.draw_text(
            (text_x, text_y, text_x + text_w, text_y + 140),
            text,
            max_fontsize=140,
            min_fontsize=50,
            font_style="bold",
        )
    except ValueError:
        raise TextOverLength(text)

    return frame.save_jpg()


add_meme(
    "login",
    login,
    min_images=1,
    max_images=1,
    min_texts=0,
    max_texts=10,
    keywords=["上号"],
    date_created=datetime(2025, 3, 26),
    date_modified=datetime(2025, 3, 26),
)