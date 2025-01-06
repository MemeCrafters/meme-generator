import random
from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage
from pydantic import Field

from meme_generator import (
    MemeArgsModel,
    MemeArgsType,
    ParserArg,
    ParserOption,
    add_meme,
)
from meme_generator.exception import MemeFeedback
from meme_generator.tags import MemeTags
from meme_generator.utils import make_jpg_or_gif

img_dir = Path(__file__).parent / "images"

help_text = "图片编号，1-阿罗娜，2-普拉娜"


class Model(MemeArgsModel):
    number: int = Field(0, description=help_text)


args_type = MemeArgsType(
    args_model=Model,
    parser_options=[
        ParserOption(
            names=["-n", "--number"],
            args=[ParserArg(name="number", value="int")],
            help_text=help_text,
        ),
    ],
)


def keep_your_money(images: list[BuildImage], texts: list[str], args: Model):
    if args.number == 0:
        number = random.randint(1, 2)
    elif args.number in [1, 2]:
        number = args.number
    else:
        raise MemeFeedback("图片编号错误，请输入1或2")
    frame = BuildImage.open(img_dir / f"{number}.png")

    def make(imgs: list[BuildImage]) -> BuildImage:
        img = (
            imgs[0]
            .convert("RGBA")
            .resize((500, 640), keep_ratio=True, inside=True, bg_color="white")
        )
        return frame.copy().paste(img, (0, 1080 - img.height), alpha=True, below=True)

    return make_jpg_or_gif(images, make)


add_meme(
    "keep_your_money",
    keep_your_money,
    min_images=1,
    max_images=1,
    args_type=args_type,
    keywords=["压岁钱不要交给"],
    tags=MemeTags.arona | MemeTags.plana,
    date_created=datetime(2024, 12, 29),
    date_modified=datetime(2024, 12, 31),
)
