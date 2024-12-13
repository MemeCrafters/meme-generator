import random
from datetime import datetime
from pathlib import Path
from typing import Literal

from arclet.alconna import store_value
from pil_utils import BuildImage
from pydantic import Field

from meme_generator import (
    MemeArgsModel,
    MemeArgsType,
    ParserArg,
    ParserOption,
    add_meme,
)
from meme_generator.exception import TextOverLength
from meme_generator.tags import MemeTags

img_dir = Path(__file__).parent / "images"

help_text = "消息框的位置，包含 left、right、random"


class Model(MemeArgsModel):
    position: Literal["left", "right", "random"] = Field(
        "random", description=help_text
    )


args_type = MemeArgsType(
    args_model=Model,
    args_examples=[
        Model(position="left"),
        Model(position="right"),
    ],
    parser_options=[
        ParserOption(
            names=["-p", "--position"],
            args=[ParserArg(name="position", value="str")],
            help_text=help_text,
        ),
        ParserOption(
            names=["--left", "左"], dest="position", action=store_value("left")
        ),
        ParserOption(
            names=["--right", "右"], dest="position", action=store_value("right")
        ),
    ],
)


def kokona_say(images, texts: list[str], args: Model):
    position = args.position
    left = (
        True
        if position == "left"
        else False
        if position == "right"
        else random.choice([True, False])
    )
    img_name = "01.png" if left else "02.png"

    frame = BuildImage.open(img_dir / img_name)
    text = texts[0]

    try:
        if left:
            frame.draw_text(
                (0, 0, 680, 220),
                text,
                max_fontsize=100,
                min_fontsize=50,
                fill="black",
                lines_align="center",
            )
        else:
            frame.draw_text(
                (frame.width - 680, 0, frame.width, 220),
                text,
                max_fontsize=100,
                min_fontsize=50,
                fill="black",
                lines_align="center",
            )
    except TextOverLength:
        raise TextOverLength(text)

    return frame.save_png()


add_meme(
    "kokona_say",
    kokona_say,
    min_texts=1,
    max_texts=1,
    default_texts=["那我问你"],
    args_type=args_type,
    keywords=["心奈说"],
    tags=MemeTags.kokona,
    date_created=datetime(2024, 12, 12),
    date_modified=datetime(2024, 12, 12),
)
