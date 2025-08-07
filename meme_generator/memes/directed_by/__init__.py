from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage, Text2Image
from pypinyin import lazy_pinyin

from meme_generator import CommandShortcut, add_meme

img_dir = Path(__file__).parent / "images"


def directed_by(images: list[BuildImage], texts: list[str], args):
    font_families = ["Zhi Mang Xing"]

    name = texts[0][:-2]
    pinyin = "".join(lazy_pinyin(name))
    pinyin = pinyin.title()

    # 准备水印文本
    line1 = f"{name}作品"
    line2 = f"Directed By {pinyin}"

    # 加载基础图片
    img = images[0].convert("RGBA")
    width, height = img.size

    # 计算水印区域 (高度为图片的25%)
    watermark_height = int(height * 0.25)

    # 创建新画布 (带透明背景)
    frame = BuildImage.new("RGBA", (width, height), (0, 0, 0, 0))
    frame.paste(img, (0, 0))

    # 计算文字位置 (居中，宽度80%)
    text_area_width = int(width * 0.8)
    x = (width - text_area_width) // 2
    y = height - int(height * 0.4)

    # 绘制第一行 (中文)
    text1 = Text2Image.from_text(
        line1,
        font_size=int(width * 0.18),  # 动态字体大小
        font_families=font_families,
        fill="red",
    ).to_image()

    text2 = Text2Image.from_text(
        line2, font_size=int(width * 0.07), fill="red"
    ).to_image()

    # 计算居中位置
    text1_x = x + (text_area_width - text1.width) // 2
    text1_y = y + (watermark_height // 2 - text1.height) // 2

    text2_x = x + (text_area_width - text2.width) // 2
    text2_y = text1_y + text1.height

    # 粘贴文字a
    frame.paste(text1, (text1_x, text1_y), alpha=True)
    frame.paste(text2, (text2_x, int(text2_y)), alpha=True)

    return frame.save_png()


add_meme(
    "directed_by",
    directed_by,
    min_images=1,
    max_images=1,
    min_texts=0,
    max_texts=1,
    default_texts=["夏思源作品"],
    keywords=["夏思源作品"],
    shortcuts=[
        CommandShortcut(
            key=r"(?P<text>\S+作品[!！]?)",
            args=["{text}"],
            humanized="xx作品",
        )
    ],
    date_created=datetime(2025, 8, 6),
    date_modified=datetime(2025, 8, 6),
)
