import random
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Literal

from arclet.alconna import store_value
from PIL.Image import Transpose
from pil_utils import BuildImage
from pydantic import Field

from meme_generator import (
    CommandShortcut,
    MemeArgsModel,
    MemeArgsType,
    ParserArg,
    ParserOption,
    add_meme,
)
from meme_generator.exception import MemeFeedback, TextOverLength
from meme_generator.tags import MemeTags

img_dir = Path(__file__).parent / "images"


@dataclass
class Character:
    name_cn: str
    name_en: str


Characters = [
    # pixiv@lowLDR
    Character("心奈", "kokona"),
    # bilibili@mooooen
    Character("爱丽丝", "arisu"),
    Character("泉奈", "izuna"),
    Character("key", "key"),
    Character("玛丽", "mari"),
    Character("濑名", "sena"),
    Character("优香", "yuuka"),
]


help_character = "角色编号：" + "，".join(
    [f"{i+1}、{Characters[i].name_cn}" for i in range(len(Characters))]
)
help_position = "消息框的位置，包含 left、right、random"


class Model(MemeArgsModel):
    character: int = Field(0, description=help_character)
    position: Literal["left", "right", "random"] = Field(
        "random", description=help_position
    )


args_type = MemeArgsType(
    args_model=Model,
    args_examples=[Model(character=c, position="right") for c in range(1, 10)],
    parser_options=[
        ParserOption(
            names=["-c", "--character"],
            args=[ParserArg(name="character", value="str")],
            help_text=help_character,
        ),
        ParserOption(
            names=["-p", "--position"],
            args=[ParserArg(name="position", value="str")],
            help_text=help_position,
        ),
        ParserOption(
            names=["--left", "左"], dest="position", action=store_value("left")
        ),
        ParserOption(
            names=["--right", "右"], dest="position", action=store_value("right")
        ),
    ],
)


def ba_say(images, texts: list[str], args: Model):
    text = texts[0]

    if args.character == 0:
        character = random.choice(Characters)
    elif args.character <= len(Characters):
        character = Characters[args.character - 1]
    else:
        raise MemeFeedback(f"角色编号错误，请输入1-{len(Characters)}")

    if args.position in ["left", "right"]:
        position = args.position
    else:
        position = random.choice(["left", "right"])

    xy = (60, 0, 580, 200) if position == "left" else (500, 0, 1020, 200)

    frame = BuildImage.open(img_dir / f"{character.name_en}.png")
    if position == "left":
        frame = frame.transpose(Transpose.FLIP_LEFT_RIGHT)

    try:
        frame.draw_text(
            xy,
            text,
            allow_wrap=True,
            max_fontsize=100,
            min_fontsize=10,
            fill="black",
            lines_align="center",
        )
    except TextOverLength:
        raise TextOverLength(text)

    return frame.save_png()


add_meme(
    "ba_say",
    ba_say,
    min_texts=0,
    max_texts=1,
    default_texts=["那我问你"],
    args_type=args_type,
    keywords=["ba说"],
    shortcuts=[
        CommandShortcut(
            key=f"{Characters[i].name_cn}说", args=["--character", f"{i+1}"]
        )
        for i in range(len(Characters))
    ],
    tags=MemeTags.arisu
    | MemeTags.izuna
    | MemeTags.key
    | MemeTags.kokona
    | MemeTags.mari
    | MemeTags.sena
    | MemeTags.yuuka,
    date_created=datetime(2024, 12, 12),
    date_modified=datetime(2025, 1, 19),
)
