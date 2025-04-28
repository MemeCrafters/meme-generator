import random
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

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
    color: str
    img_num: int


characters = [
    Character("爱莉", "airi", "#FB8AAC", 15),
    Character("彰人", "akito", "#FF7722", 13),
    Character("杏", "an", "#00BADC", 13),
    Character("梦", "emu", "#FF66BB", 13),
    Character("绘名", "ena", "#B18F6C", 16),
    Character("遥", "haruka", "#6495F0", 13),
    Character("穗波", "honami", "#F86666", 15),
    Character("一歌", "ichika", "#33AAEE", 15),
    Character("KAITO", "kaito", "#3366CC", 13),
    Character("奏", "kanade", "#BB6688", 14),
    Character("心羽", "kohane", "#FF6699", 14),
    Character("连", "len", "#D3BD00", 14),
    Character("流歌", "luka", "#F88CA7", 13),
    Character("真冬", "mafuyu", "#7171AF", 14),
    Character("MEIKO", "meiko", "#E4485F", 13),
    Character("初音未来", "miku", "#33CCBB", 13),
    Character("实乃理", "minori", "#F39E7D", 14),
    Character("瑞希", "mizuki", "#CA8DB6", 14),
    Character("宁宁", "nene", "#19CD94", 13),
    Character("铃", "rin", "#E8A505", 13),
    Character("类", "rui", "#BB88EE", 16),
    Character("咲希", "saki", "#F5B303", 15),
    Character("志步", "shiho", "#A0C10B", 15),
    Character("雫", "shizuku", "#5CD0B9", 13),
    Character("冬弥", "touya", "#0077DD", 15),
    Character("司", "tsukasa", "#F09A04", 15),
]


help_text = "角色编号：" + "，".join(
    [f"{i + 1}、{characters[i].name_cn}" for i in range(26)]
)


class Model(MemeArgsModel):
    character: int = Field(0, description=help_text)
    number: int = Field(0, description="图片编号")


args_type = MemeArgsType(
    args_model=Model,
    args_examples=[Model(character=i, number=0) for i in range(1, 27)],
    parser_options=[
        ParserOption(
            names=["-c", "--character", "角色编号"],
            args=[ParserArg(name="character", value="int")],
            help_text=help_text,
        ),
        ParserOption(
            names=["-n", "--number", "图片编号"],
            args=[ParserArg(name="number", value="int")],
            help_text="图片编号",
        ),
    ],
)


def pjsk(images, texts: list[str], args: Model):
    text = texts[0]

    character = None
    if args.character == 0:
        character = random.choice(characters)
    elif args.character in range(1, 27):
        character = characters[int(args.character) - 1]
    else:
        raise MemeFeedback("角色编号错误，请输入1-26")

    if args.number == 0:
        n = random.randint(0, character.img_num - 1)
    elif args.number in range(1, character.img_num + 1):
        n = args.number - 1
    else:
        raise MemeFeedback(
            f"角色{character.name_cn}的图片编号错误，请输入1-{character.img_num}"
        )

    img = BuildImage.open(img_dir / character.name_en / f"{n:02d}.png")
    color = character.color
    w, h = img.size

    text_frame = BuildImage.new("RGBA", (w - 20, 50))
    try:
        text_frame.draw_text(
            (0, 0, w - 20, 50),
            text,
            fill=color,
            max_fontsize=50,
            min_fontsize=20,
            stroke_ratio=0.12,
            stroke_fill="white",
            font_families=["033-SSFangTangTi"],
        )
    except ValueError:
        raise TextOverLength(text)

    img.paste(
        text_frame.rotate(40 * (0.5 - random.random()), expand=True),
        (0, 10),
        alpha=True,
    )
    return img.save_png()


add_meme(
    "pjsk",
    pjsk,
    min_texts=1,
    max_texts=1,
    args_type=args_type,
    keywords=["pjsk", "世界计划"],
    shortcuts=[
        CommandShortcut(
            key=rf"(:?pjsk|世界计划)[_-]?(:?{characters[i].name_cn}|{characters[i].name_en})",
            args=["--character", f"{i + 1}"],
            humanized=f"pjsk{characters[i].name_cn}",
        )
        for i in range(26)
    ],
    tags=MemeTags.project_sekai,
    date_created=datetime(2024, 12, 19),
    date_modified=datetime(2024, 12, 19),
)
