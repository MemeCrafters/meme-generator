from datetime import datetime
from pathlib import Path

from PIL import ImageFilter
from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.exception import TextOverLength
from meme_generator.tags import MemeTags

img_dir = Path(__file__).parent / "images"


def ayachi_holdsign(images, texts: list[str], args):
    text = texts[0]
    frame = BuildImage.open(img_dir / "0.png")
    text_img = BuildImage.new("RGBA", (600, 350))
    try:
        text_img.draw_text(
            (20, 20, 580, 330),
            text,
            max_fontsize=150,
            min_fontsize=80,
            allow_wrap=True,
            lines_align="center",
            font_families=["FZShaoEr-M11S"],
            fill="#51201b",
        )
    except ValueError:
        raise TextOverLength(text)

    text_img.image = text_img.image.filter(ImageFilter.GaussianBlur(radius=1))

    text_img = text_img.perspective(((0, 235), (523, 0), (659, 297), (170, 536)))
    frame.paste(text_img, (125, 307), alpha=True)
    return frame.save_jpg()


add_meme(
    "ayachi_holdsign",
    ayachi_holdsign,
    min_texts=1,
    max_texts=1,
    default_texts=["我控制不住自己啊"],
    keywords=["宁宁举牌"],
    tags=MemeTags.ayachi,
    date_created=datetime(2025, 4, 28),
    date_modified=datetime(2025, 4, 28),
)
