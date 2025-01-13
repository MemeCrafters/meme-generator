from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.exception import TextOverLength
from meme_generator.tags import MemeTags

img_dir = Path(__file__).parent / "images"

default_text = "好想去海边啊～"


def luotianyi_say(images: list[BuildImage], texts: list[str], args):
    frame = BuildImage.open(img_dir / "0.png")
    text = texts[0]
    try:
        frame.draw_text(
            (520, 20, frame.width - 20, 220),
            text,
            min_fontsize=40,
            max_fontsize=140,
            fill="#66CCFF",
            allow_wrap=True,
            lines_align="center",
        )
    except ValueError:
        raise TextOverLength(text)

    return frame.save_jpg()


add_meme(
    "luotianyi_say",
    luotianyi_say,
    min_texts=1,
    max_texts=1,
    default_texts=[default_text],
    keywords=["洛天依说", "天依说"],
    tags=MemeTags.luotianyi,
    date_created=datetime(2025, 1, 7),
    date_modified=datetime(2025, 1, 7),
)
