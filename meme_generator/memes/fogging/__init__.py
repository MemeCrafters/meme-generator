from datetime import datetime
from pathlib import Path

from PIL import ImageFilter
from pil_utils import BuildImage

from meme_generator import MemeArgsModel, add_meme
from meme_generator.exception import TextOverLength
from meme_generator.utils import make_png_or_gif

img_dir = Path(__file__).parent / "images"


default_text = "兄弟，回南了"


def fogging(images: list[BuildImage], texts: list[str], args: MemeArgsModel):
    img_w = min(images[0].width, 500)
    img_h = int(images[0].height * img_w / images[0].width)
    mask = BuildImage.open(img_dir / "0.png").resize((img_w, img_h), keep_ratio=True)
    text = texts[0] if texts else default_text
    try:
        mask.draw_text((10, 10, mask.width - 10, 80), text, max_fontsize=40)
    except ValueError:
        raise TextOverLength(text)

    def make(imgs: list[BuildImage]) -> BuildImage:
        img = (
            imgs[0]
            .convert("RGBA")
            .resize((img_w, img_h))
            .filter(ImageFilter.GaussianBlur(radius=10))
        )
        img.paste(mask, alpha=True)
        return img

    return make_png_or_gif(images, make)


add_meme(
    "fogging",
    fogging,
    min_images=1,
    max_images=1,
    min_texts=0,
    max_texts=1,
    default_texts=[default_text],
    keywords=["回南天", "水雾"],
    date_created=datetime(2025, 3, 16),
    date_modified=datetime(2025, 3, 16),
)
