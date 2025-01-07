from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.exception import TextOverLength
from meme_generator.utils import make_jpg_or_gif

img_dir = Path(__file__).parent / "images"

default_text = "好想去海边啊～"


def lty(images: list[BuildImage],texts: list[str], args):
    frame = BuildImage.open(img_dir / "0.png")
    text = texts[0] if texts else default_text
    try:
        frame.draw_text(
            (520, frame.height - 1054, frame.width - 20, 184),
            text,
            min_fontsize=64,
            max_fontsize=140,
            fill=(102,204,255),
            allow_wrap=True,
            lines_align="center",
        )
    except ValueError:
        raise TextOverLength(text)
    
    return frame.save_jpg()


add_meme(
    "lty",
    lty,
    min_images=0,
    max_images=0,
    min_texts=0,
    max_texts=1,
    default_texts=[default_text],
    keywords=["天依say", "天依生","天依说"],
    date_created=datetime(2025, 1, 7),
    date_modified=datetime(2025, 1, 7),
)
