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

img_dir = Path(__file__).parent / "images"

holiday_dict = {
    "跨年": 0,
    "五一": 1,
}

help_text = (
    "假日编号：" + ",".join([f"{v + 1}、{k}" for k, v in holiday_dict.items()]) + "。"
)


class Model(MemeArgsModel):
    holiday: int = Field(0, description=help_text)


args_type = MemeArgsType(
    args_model=Model,
    args_examples=[Model(holiday=h) for h in range(2)],
    parser_options=[
        ParserOption(
            names=["-h", "--holiday", "假日编号"],
            args=[ParserArg(name="holiday", value="int")],
            help_text=help_text,
        )
    ],
)


def your_holiday(images: list[BuildImage], texts: list[str], args: Model):
    frame = BuildImage.open(img_dir / f"{args.holiday - 1}.png")
    img = images[0].convert("RGBA").resize((586, 430), inside=True, keep_ratio=True)
    frame.paste(img, (0, 650), alpha=True, below=True)
    return frame.save_jpg()


add_meme(
    "your_holiday",
    your_holiday,
    min_images=1,
    max_images=1,
    args_type=args_type,
    keywords=["你的假日"],
    shortcuts=[
        CommandShortcut(key="你的" + k, args=["--holiday", f"{v}"])
        for k, v in holiday_dict.items()
    ],
    date_created=datetime(2024, 12, 31),
    date_modified=datetime(2024, 12, 31),
)
