from datetime import datetime
from pathlib import Path
from typing import Literal
from PIL import Image
from numpy import random

from pydantic import Field
from arclet.alconna import store_value
from pil_utils import BuildImage, Text2Image
from pil_utils.gradient import LinearGradient, ColorStop

from meme_generator import MemeArgsModel, MemeArgsType, add_meme, ParserArg, ParserOption

# 图片文件夹
IMG_DIR = Path(__file__).parent / "images";
# 位置参数说明
POSITION_HELP_TEXT:str = "标签位置: left | right";
# 稀有度参数说明
RANK_HELP_TEXT:str = "稀有度：0 ~ 4，默认为4";
# 图标参数说明
ICONS_HELP_TEXT:str = "图标选择: 字符串。 生成第几个标签就读取第几位字符，且只有为 1 ~ 8 时才会指定，否则随机生成";
# 稀有度文字参数说明
RANK_TEXT_HELP_TEXT:str = "稀有度文字：字符串。用于右上角表示, 第一个占用符会填充稀有度数字";
# 文字大小参数说明
TEXT_SIZE_HELP_TEXT:str = "文字大小。默认 48";
# 稀有度颜色
RANK_COLOR: list[tuple[int, int, int, int]] = [
    (200, 200, 200, 255),   # rank 0 (normal)
    (119, 190, 106, 255),   # rank 1 (good)
    (30,  144, 255, 255),   # rank 2 (rare)
    (147, 112, 209, 255),   # rank 3 (epic)
    (255, 140, 0  , 255)    # rank 4 (legend)
];

class Model(MemeArgsModel):
    # 位置
    position: Literal["left", "right"] = Field(default = "left", description = POSITION_HELP_TEXT);
    # 稀有度 
    rank: int = Field(default = 4, description = RANK_HELP_TEXT);
    # 图标
    icons: str = Field(default = "000", description = ICONS_HELP_TEXT);
    # 稀有度文字
    text: str = Field(default = "Cost {}", description = RANK_TEXT_HELP_TEXT);
    # 文字大小
    size: int = Field(default = 48, description = TEXT_SIZE_HELP_TEXT);

chess_args = MemeArgsType(
    args_model = Model,
    args_examples = 
        [Model(position="left", rank = i, icons = "000") for i in range(len(RANK_COLOR))] + # type: ignore
        [Model(position="right", rank = j, icons = "000") for j in range(len(RANK_COLOR))], # type: ignore
    parser_options = [
        ParserOption(
            names = ["-p", "--position"],
            args = [ParserArg(name = "position", value = "str")],
            help_text = POSITION_HELP_TEXT
        ), 
        ParserOption(
            names = ["-r", "--rank"],
            args = [ParserArg(name = "rank",  value = "int")],
            help_text = RANK_HELP_TEXT
        ),
        ParserOption(
            names = ["-i", "--icon"],
            args = [ParserArg(name = "icons", value = "str")],
            help_text = ICONS_HELP_TEXT
        ),
        ParserOption(
            names = ["-t", "--text"],
            args = [ParserArg(name = "text", value = "str")],
            help_text = RANK_TEXT_HELP_TEXT
        ),
        ParserOption(
            names = ["-s", "--size"],
            args = [ParserArg(name = "size", value = "int")],
            help_text = TEXT_SIZE_HELP_TEXT
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
            names = ["--normal", "普通"],
            dest = "rank",
            action = store_value(0)
        ),
        ParserOption(
            names = ["--good", "良好"],
            dest = "rank",
            action = store_value(1)
        ),
        ParserOption(
            names = ["--rare", "稀有"],
            dest = "rank",
            action = store_value(2)
        ),
        ParserOption(
            names = ["--epic", "史诗"],
            dest = "rank",
            action = store_value(3)
        ),
        ParserOption(
            names = ["--legend", "传说"],
            dest = "rank",
            action = store_value(4)
        ),
    ],
)

def auto_chess_gen(images: list[BuildImage], texts:list[str], args: Model):
    '''
    Meme表情： 自走棋生成器 (autochess)

    images{1}： 底片

    texts{1~4}： 其中第一段文字作为名称，后面最多三段文字作为标签贴在一侧
    '''
    ## ======= settings ======= ##
    # 图片尺寸
    meme_width:int = 600;
    meme_height:int = 480;
    # 边缘尺寸
    side_weight:int = 16;
    # 描边颜色
    border_color = (20, 20, 20, 127);
    # 侧边距
    padding_side:int = 12 + side_weight;
    # 上边距
    padding_top:int = 18 + side_weight;
    # 间距
    text_interval:int = 16; 
    # 字体
    text_size:int = int(args.size); #36;
    # 字体颜色
    text_color = (230, 230, 230, 255);
    # 渐变灰度
    gray1:int = 96;
    gray2:int = 160;
    # 背景灰度
    grayBG:int = 192;
    ## ======================== ##
    if len(texts) == 1: texts = texts[0].split(","); # 适配 FastAPI
    # 标签方向
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
    rank_text:str = args.text.format(rank + 1);
    rankImg = Text2Image.from_text(
        rank_text,
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
    border_pxy:list[tuple[float, float]] = [
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
    maskImg = BuildImage.new("RGBA", (meme_width, meme_height), (0, 0, 0, 255)).draw_polygon(border_pxy, fill = (0, 0, 0, 0));
    # 边框渐变色
    colorImp = BuildImage.new(
        "RGBA", (meme_width, meme_height), (0, 0, 0, 0)
    ).gradient_color( # 灰度
        LinearGradient(
            (0, meme_height >> 1, meme_width, meme_height >> 1),
            [
                ColorStop(0, (gray1, gray1, gray1, 255)), 
                ColorStop(1, (gray2, gray2, gray2, 255))
            ]
        )
    ).color_mask(RANK_COLOR[rank if rank in range(len(RANK_COLOR)) else len(RANK_COLOR) - 1]); # 滤镜颜色
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
        rank_text,
        font_size = text_size, 
        fill = text_color, 
        font_style = "bold",
        stroke_fill = border_color,
    );
    # 读取图标精灵 
    class_little_sprite:BuildImage = BuildImage.open(IMG_DIR / "class_little_sprite.png");
    # 读取图标的字符串标识
    icon_types:list[str] = list(args.icons);
    # 绘制标签
    it = iter(texts);
    while True:
        try:
            text = next(it);
            # 绘制坐标
            x:int = padding_side;
            y:int = padding_top + int(nameImg.height);
            # 绘制图标
            icon_index:int;
            # 获取文字图片
            tagImg = Text2Image.from_text(
                text, 
                text_size, 
                fill = text_color, 
                font_style = "bold",        
                stroke_width = 1, 
                stroke_fill = border_color,
            );#.to_image();
            try:
                icon_index = int(icon_types.pop(0));
            except: # 包括字符串无法转换成数字 或 字符串列表不够作为标识
                icon_index = 0;
            if icon_index not in range(1,9):
                icon_index = random.randint(1,9);
            unit_size:int = class_little_sprite.height;
            # 图标
            iconImp:BuildImage = class_little_sprite.crop(
                ((icon_index - 1) * unit_size, 0, icon_index * unit_size, unit_size)
            ).circle_corner(4);
            dy:int = (int(tagImg.height) - iconImp.height) >> 1; # 图标高度修正
            mainImg.paste(
                iconImp,
                (
                    x if is_left else meme_width - x - iconImp.width, 
                    meme_height - y - iconImp.height - dy if is_left else y + dy
                ),
                alpha = True
            );
            x += iconImp.width + 6;
            # 绘制文字
            mainImg.draw_text(
                (
                    x if is_left else meme_width - x - tagImg.longest_line,
                    meme_height - y - tagImg.height if is_left else y
                ),
                text,
                font_size = text_size, 
                fill = text_color, 
                font_style = "bold",        
                stroke_fill = border_color,
            );
            # 迭代坐标
            padding_top += int(tagImg.height) + text_interval;
        except StopIteration: # 迭代结束
            break;

    return mainImg.save_png();

add_meme(
    "auto_chess_gen",
    auto_chess_gen,
    min_images = 1,
    max_images = 1,
    min_texts = 1,
    max_texts = 9,
    args_type = chess_args,
    default_texts = ["Lunastic", "嘿，Meme Generator", "你动不动BUG日子结束了", "把表情交出来"],
    keywords = ["自走棋", "autochess"],
    date_created = datetime(2025, 3, 29),
    date_modified = datetime(2025, 3, 30),
)