from datetime import datetime
from typing import Literal
from PIL import Image

from pydantic import Field
from arclet.alconna import store_value
from pil_utils import BuildImage, Text2Image
from pil_utils.gradient import LinearGradient, ColorStop

from meme_generator import MemeArgsModel, MemeArgsType, add_meme, ParserArg, ParserOption
import meme_generator.exception as exception

# 位置参数说明
POSITION_HELP_TEXT = "名称及标签位置: left | right";
# 稀有度参数说明
RANK_HELP_TEXT = "稀有度: 0~4";

class Model(MemeArgsModel):
    # 位置
    position: Literal["left", "right"] = Field(default = "left", description = POSITION_HELP_TEXT);
    # 稀有度 
    rank: Literal["0", "1", "2", "3", "4"] = Field(default = "4", description = RANK_HELP_TEXT);

chess_args = MemeArgsType(
    args_model = Model,
    args_examples = [Model(position="left", rank = "4")], # type: ignore
    parser_options = [
        ParserOption(
            names = ["-p","--position"],
            args = [ParserArg(name = "position",value = "str")],
            help_text = POSITION_HELP_TEXT
        ),
        ParserOption(
            names = ["--left", "左侧", "左"],
            dest = "position",
            action = store_value("left")
        ),
        ParserOption(
            names = ["--right", "右侧", "右"],
            dest = "position",
            action = store_value("right")
        ),
        ParserOption(
            names = ["-r","--rank"],
            args = [ParserArg(name = "rank",value = "str")],
            help_text = RANK_HELP_TEXT
        ),
        ParserOption(
            names = ["--normal", "普通"],
            dest = "rank",
            action = store_value("0")
        ),
        ParserOption(
            names = ["--good", "良好"],
            dest = "rank",
            action = store_value("1")
        ),
        ParserOption(
            names = ["--rare", "稀有"],
            dest = "rank",
            action = store_value("2")
        ),
        ParserOption(
            names = ["--epic", "史诗"],
            dest = "rank",
            action = store_value("3")
        ),
        ParserOption(
            names = ["--legend", "传说"],
            dest = "rank",
            action = store_value("4")
        ),
    ]           
)

def auto_chess_gen(images: list[BuildImage], texts:list[str], args: Model):
    ## ======= settings ======= ##
    # 图片尺寸
    meme_width = 600;
    meme_height = 480;
    # 边缘尺寸
    side_weight = 16;
    # 描边颜色
    border_color = (20, 20, 20, 127);
    # 侧边距
    padding_side = 12 + side_weight;
    # 上边距
    padding_top = 18 + side_weight;
    # 间距
    text_interval = 16; 
    # 字体
    text_size = 48;
    # 字体颜色
    text_color = (230, 230, 230, 255);
    # 渐变灰度
    gray1 = 96;
    gray2 = 160;
    # 背景灰度
    grayBG = 192;
    # 稀有度颜色
    rank_color = [
        (200, 200, 200, 255), 
        (119, 190, 106, 255), 
        (30,  144, 255, 255), 
        (147, 112, 209, 255), 
        (255, 140, 0  , 255), 
    ];
    ## ======================== ##
    is_left:bool = args.position == "left";
    # 棋子名称
    name_text:str = texts.pop(0);
    nameImg = Text2Image.from_text(
        name_text, 
        text_size, 
        fill = text_color, 
        font_style = "bold",
        stroke_width = 1, 
        stroke_fill = border_color,
    );#.to_image();
    # 稀有度
    rank:int = int(args.rank);
    rankImg = Text2Image.from_text(
        f"Cost {rank + 1}", 
        text_size,
        fill = text_color,
        font_style = "bold", 
        stroke_width = 1, 
        stroke_fill = border_color,
    );#.to_image();
    # 核心图片
    mainImg:BuildImage = images[0].convert("RGBA").resize((meme_width, meme_height), keep_ratio = True);
    # tag 背景
    tagBG:BuildImage = BuildImage.new(
        "RGBA", (meme_width, meme_height), (0, 0, 0, 0)
    ).gradient_color(
        LinearGradient(
            (0, meme_height >> 1, meme_width >> 1, meme_height >> 1),
            [
                ColorStop(1, (0, 0, 0, 0)), 
                ColorStop(0, (0, 0, 0, grayBG))
            ]
        ) 
        if is_left else
        LinearGradient(
            (meme_width >> 1, meme_height >> 1, meme_width, meme_height >> 1),
            [
                ColorStop(0, (0, 0, 0, 0)), 
                ColorStop(1, (0, 0, 0, grayBG))
            ]
        )
    );
    # 内框点位
    name_pxy:list[tuple[float, float]] = [
        # 左上
        (side_weight, side_weight),
        # 花费处边框
        (meme_width - side_weight - rankImg.longest_line - rankImg.height, side_weight),         
        (meme_width - (side_weight << 1) - rankImg.longest_line, side_weight + rankImg.height),
        (meme_width - side_weight, side_weight + rankImg.height),
        # 右下
        (meme_width - side_weight, meme_height - side_weight),
        # 名字处边框
        (side_weight + nameImg.longest_line + nameImg.height, meme_height - side_weight),
        ((side_weight << 1) + nameImg.longest_line, meme_height - side_weight - nameImg.height),
        (side_weight, meme_height - side_weight - nameImg.height),
    ];
    # 边框蒙版
    maskImg = BuildImage.new("RGBA", (meme_width, meme_height), (0, 0, 0, 255)).draw_polygon(name_pxy, fill = (0, 0, 0, 0));
    # 边框渐变色(灰度 + 滤镜)
    colorImp = BuildImage.new(
        "RGBA", (meme_width, meme_height), (0, 0, 0, 0)
    ).gradient_color(
        LinearGradient(
            (0, meme_height >> 1, meme_width, meme_height >> 1),
            [
                ColorStop(0, (gray1, gray1, gray1, 255)), 
                ColorStop(1, (gray2, gray2, gray2, 255))
            ]
        )
    ).color_mask(rank_color[rank if rank in range(5) else 4]);
    # 边框图片
    borderImg = Image.composite(colorImp.image, Image.new("RGBA", colorImp.size), maskImg.image);

    # 合体！
    mainImg.paste(tagBG, alpha = True);
    mainImg.paste(borderImg, alpha = True);
    #mainImg.paste(nameImg, ((side_weight << 1), meme_height - (side_weight >> 1) - nameImg.height), alpha = True);
    #mainImg.paste(rankImg, (meme_width - rankImg.longest_line - (side_weight << 1), (side_weight >> 1)), alpha = True);
    mainImg.draw_text(
        ((side_weight << 1), meme_height - (side_weight >> 1) - nameImg.height),
        name_text,
        font_size = text_size, 
        fill = text_color, 
        font_style = "bold",
        stroke_fill = border_color,
    );
    mainImg.draw_text(
        (meme_width - rankImg.longest_line - (side_weight << 1), (side_weight >> 1)),
        f"Cost {rank + 1}",
        font_size = text_size, 
        fill = text_color, 
        font_style = "bold",
        stroke_fill = border_color,
    )

    # 绘制标签
    it = iter(texts);
    while True:
        try:
            text = next(it);
            tagImg = Text2Image.from_text(
                text, 
                text_size, 
                fill = text_color, 
                font_style = "bold",        
                stroke_width = 1, 
                stroke_fill = border_color,
            );#.to_image();
            mainImg.draw_text(
                (
                    padding_side if is_left else meme_width - padding_side - tagImg.longest_line,
                    meme_height - padding_top - tagImg.height - nameImg.height if is_left else padding_top + rankImg.height
                ),
                text,
                font_size = text_size, 
                fill = text_color, 
                font_style = "bold",        
                stroke_fill = border_color,
            )
            padding_top += tagImg.height + text_interval;
        except StopIteration:
            break;

    return mainImg.save_png();

add_meme(
    "auto_chess_gen",
    auto_chess_gen,
    min_images=1,
    max_images=1,
    min_texts=1,
    max_texts=4,
    args_type=chess_args,
    keywords=["自走棋", "acg"],
    date_created=datetime(2025, 3, 29),
    date_modified=datetime(2025, 3, 29),
)