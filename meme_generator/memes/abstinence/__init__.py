from datetime import datetime
from pathlib import Path

import dateparser
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

img_dir = Path(__file__).parent / "images"


class Model(MemeArgsModel):
    time: str = Field("", description="指定时间")
    name: str = Field("", description="指定名字")


args_type = MemeArgsType(
    args_model=Model,
    parser_options=[
        ParserOption(
            names=["-t", "--time"],
            args=[ParserArg(name="time", value="str")],
            help_text="指定时间",
        ),
        ParserOption(
            names=["-n", "--name"],
            args=[ParserArg(name="name", value="str")],
            help_text="指定名字",
        ),
    ],
)


def abstinence(images: list[BuildImage], texts: list[str], args: Model):
    time = datetime.now()
    if args.time and (parsed_time := dateparser.parse(args.time)):
        time = parsed_time
    name = args.name or (args.user_infos[-1].name if args.user_infos else "")

    img = (
        images[0]
        .convert("RGBA")
        .resize((300, 300), keep_ratio=True, inside=True, bg_color="white")
    )

    frame = BuildImage.open(img_dir / "base.png").convert("RGBA")

    try:
        frame.paste(img, (80, 400))
        frame.draw_bbcode_text(
            (150, 650, 760, 800),
            text=f"戒导人：[u] {name} [/u]",
            max_fontsize=20,
            min_fontsize=10,
            halign="center",
        )
    except ValueError:
        raise TextOverLength(name)
    frame.draw_bbcode_text(
        (150, 750, 760, 800),
        text=f"[u] {time.year} [/u]年[u] {time.month} [/u]月[u] {time.day} [/u]日",
        max_fontsize=20,
        min_fontsize=10,
        halign="center",
    )

    stamp = BuildImage.open(img_dir / "stamp.png").convert("RGBA")
    stamp = stamp.resize((200, 200))
    frame.paste(stamp, (350, 650), alpha=True)

    return frame.save_jpg()


add_meme(
    "abstinence",
    abstinence,
    min_images=1,
    max_images=1,
    min_texts=0,
    max_texts=0,
    args_type=args_type,
    keywords=["戒导"],
    date_created=datetime(2024, 12, 13),
    date_modified=datetime(2024, 12, 14),
)
