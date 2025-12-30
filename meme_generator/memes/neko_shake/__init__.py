from datetime import datetime
from pathlib import Path

from arclet.alconna import store_true
from PIL import Image, ImageSequence
from pil_utils import BuildImage
from pydantic import Field

from meme_generator import MemeArgsModel, MemeArgsType, ParserOption, add_meme
from meme_generator.utils import save_gif

img_dir = Path(__file__).parent / "images"


class Model(MemeArgsModel):
    circle: bool = Field(False, description="是否将图片变为圆形")


args_type = MemeArgsType(
    args_model=Model,
    args_examples=[Model(circle=False), Model(circle=True)],
    parser_options=[
        ParserOption(
            names=["--circle", "圆"],
            default=False,
            action=store_true,
            help_text="是否将图片变为圆形",
        ),
    ],
)


def neko_shake(images, texts, args: Model):
    # 1. 加载猫
    neko = BuildImage.open(img_dir / "neko.gif")

    item_size = 103
    w, h = 245, 200

    # 2. 处理用户图片
    img = images[0].convert("RGBA")
    user_img = img.resize(
        (item_size, item_size), keep_ratio=True, resample=Image.Resampling.LANCZOS
    )

    # 3. 处理 Alpha 通道 将透明度二值化：>128 变全不透，<=128 变全透
    pil_img = user_img.image
    if pil_img.mode == "RGBA":
        _, _, _, a = pil_img.split()
        a = a.point(lambda x: 255 if x > 128 else 0)
        pil_img.putalpha(a)
        user_img.image = pil_img

    # 4. 圆形处理
    if args.circle:
        user_img = user_img.circle()

    # 5. 图片在每一帧的坐标
    locs = [(142, 95), (118, 57), (118, 16), (142, 42)]

    # 6. 逐帧合成
    frames = []
    source_frames = [frame.copy() for frame in ImageSequence.Iterator(neko.image)]

    for i, frame in enumerate(source_frames):
        frame = BuildImage(frame)
        new_img = BuildImage.new("RGBA", (w, h), (255, 255, 255, 0))
        # 绘制猫咪
        new_img.paste(frame)
        # 绘制图片
        loc_x, loc_y = locs[i % len(locs)]
        new_img.paste(user_img, (loc_x, loc_y), alpha=True)
        frames.append(new_img.image)

    # 7. 返回 GIF
    return save_gif(frames, 0.04)


add_meme(
    "neko_shake",
    neko_shake,
    min_images=1,
    max_images=1,
    args_type=args_type,
    keywords=["猫摇"],
    date_created=datetime(2025, 12, 29),
    date_modified=datetime(2025, 12, 29),
)
