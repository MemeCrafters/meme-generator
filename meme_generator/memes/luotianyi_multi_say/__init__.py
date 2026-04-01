from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.exception import TextOverLength
from meme_generator.tags import MemeTags
from meme_generator.utils import save_gif

img_dir = Path(__file__).parent / "images"

# 默认文本（2个词示例）
default_text = [
    "啊→↑→↓→",
    "How I long~~\nTo embrace~~~",
    "The future breaking~\nOut of shades",
    "From the past\nStill ablaze!",
]


def luotianyi_multi_say(images: list[BuildImage], texts: list[str], args):
    # 校验：必须输入2~10个文字/文本
    text_list = texts
    if len(text_list) < 2 or len(text_list) > 10:
        raise TextOverLength(f"请输入2~10个文字，当前输入了{len(text_list)}个")

    frames = []
    # 遍历每一段文本，逐帧生成画面
    for text in text_list:
        # 打开底图（单张底图循环使用，如需多帧底图可改为 f"{i}.png"）
        frame = BuildImage.open(img_dir / "0.png")
        try:
            # 绘制当前文本
            frame.draw_text(
                (520, 20, frame.width - 20, 220),
                text,
                min_fontsize=40,
                max_fontsize=140,
                fill="#66CCFF",
                allow_wrap=True,
                lines_align="center",
            )
        except ValueError:
            raise TextOverLength(text)
        # 添加到帧列表
        frames.append(frame.image)

    return save_gif(frames, 3)


add_meme(
    "luotianyi_multi_say",
    luotianyi_multi_say,
    min_texts=2,  # 最小2个文本
    max_texts=10,  # 最大10个文本
    default_texts=default_text,
    keywords=["洛天依多说", "天依多说"],
    tags=MemeTags.luotianyi,
    date_created=datetime(2025, 1, 7),
    date_modified=datetime(2025, 4, 1),
)
