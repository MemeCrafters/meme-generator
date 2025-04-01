from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.utils import make_gif_or_combined_gif, Maker

# 图片资源目录
IMG_DIR = Path(__file__).parent / "images";

# 旧病复发
def jiubingfufa(images:list[BuildImage], texts:list[str], args):
    # 默认文字
    text:str = texts[0];
    # 预处理
    target:BuildImage = images[0].convert("RGBA").resize((120, 120),keep_ratio=True).circle();

    def gif_maker(index:int) -> Maker :
        def maker(img:list[BuildImage]) -> BuildImage:
            # 底图
            basicImg: BuildImage = BuildImage.open(IMG_DIR / f"{index}.jpg").convert("RGBA").resize_width(480);
            # 目标图
            basicImg.paste(img[0].rotate(360 * index / 26), (32, basicImg.height - 162), alpha = True);
            # 测试标记
            basicImg.draw_text((0, 0),f"{index}", font_size = 16, fill = (0, 0, 0, 64));
            # 目标文字
            if index > 9:
                basicImg.draw_text((30, 80), text, font_size= 32, fill = "white", stroke_fill = "black");
            return basicImg;
            
        return maker;

    return make_gif_or_combined_gif([target], gif_maker, 26, 0.0625);

add_meme(
    "jiubingfufa",
    jiubingfufa,
    max_images = 1,
    min_images = 1,
    max_texts = 1,
    min_texts = 0,
    default_texts = ["此乃BUG复发也"],
    keywords = ["旧病复发", "jiubingfufa"],
    date_created = datetime(2025, 4, 1),
    date_modified = datetime(2025, 4, 1),
)