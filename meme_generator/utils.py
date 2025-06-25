import asyncio
import hashlib
import inspect
import math
import random
import time
from collections.abc import Coroutine
from dataclasses import dataclass, field
from enum import Enum
from functools import partial, wraps
from io import BytesIO
from pathlib import Path
from typing import TYPE_CHECKING, Any, Callable, Literal, TypeVar

import httpx
import skia
from PIL import Image
from PIL.Image import Image as IMG
from pil_utils import BuildImage, Text2Image
from pil_utils.typing import ColorType
from typing_extensions import ParamSpec

from .config import meme_config
from .exception import MemeFeedback

if TYPE_CHECKING:
    from .meme import Meme

resources_dir = Path(__file__).parent / "resources"


P = ParamSpec("P")
R = TypeVar("R")


def run_sync(call: Callable[P, R]) -> Callable[P, Coroutine[None, None, R]]:
    """一个用于包装 sync function 为 async function 的装饰器
    参数:
        call: 被装饰的同步函数
    """

    @wraps(call)
    async def _wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        loop = asyncio.get_running_loop()
        pfunc = partial(call, *args, **kwargs)
        result = await loop.run_in_executor(None, pfunc)
        return result

    return _wrapper


def is_coroutine_callable(call: Callable[..., Any]) -> bool:
    """检查 call 是否是一个 callable 协程函数"""
    if inspect.isroutine(call):
        return inspect.iscoroutinefunction(call)
    if inspect.isclass(call):
        return False
    func_ = getattr(call, "__call__", None)
    return inspect.iscoroutinefunction(func_)


def save_gif(frames: list[IMG], duration: float) -> BytesIO:
    output = BytesIO()
    frames[0].save(
        output,
        format="GIF",
        save_all=True,
        append_images=frames[1:],
        duration=duration * 1000,
        loop=0,
        disposal=2,
        optimize=False,
    )

    # 没有超出最大大小，直接返回
    nbytes = output.getbuffer().nbytes
    if nbytes <= meme_config.gif.gif_max_size * 10**6:
        return output

    # 超出最大大小，帧数超出最大帧数时，缩减帧数
    n_frames = len(frames)
    gif_max_frames = meme_config.gif.gif_max_frames
    if n_frames > gif_max_frames:
        index = range(n_frames)
        ratio = n_frames / gif_max_frames
        index = (int(i * ratio) for i in range(gif_max_frames))
        new_duration = duration * ratio
        new_frames = [frames[i] for i in index]
        return save_gif(new_frames, new_duration)

    # 超出最大大小，帧数没有超出最大帧数时，缩小尺寸
    new_frames = [
        frame.resize((int(frame.width * 0.9), int(frame.height * 0.9)))
        for frame in frames
    ]
    return save_gif(new_frames, duration)


def get_avg_duration(image: IMG) -> float:
    if not getattr(image, "is_animated", False):
        return 0
    total_duration = 0
    n_frames = getattr(image, "n_frames", 1)
    for i in range(n_frames):
        image.seek(i)
        total_duration += image.info.get("duration", 20)
    return total_duration / n_frames / 1000


def split_gif(image: IMG) -> list[IMG]:
    frames: list[IMG] = []
    n_frames = getattr(image, "n_frames", 1)
    for i in range(n_frames):
        image.seek(i)
        frame = image.copy()
        frames.append(frame)
    image.seek(0)
    if image.info.__contains__("transparency"):
        frames[0].info["transparency"] = image.info["transparency"]
    return frames


class FrameAlignPolicy(Enum):
    """
    要叠加的gif长度大于基准gif时，是否延长基准gif长度以对齐两个gif
    """

    no_extend = 0
    """不延长"""
    extend_first = 1
    """延长第一帧"""
    extend_last = 2
    """延长最后一帧"""
    extend_loop = 3
    """以循环方式延长"""


def get_aligned_gif_indexes(
    gif_infos: list[tuple[int, float]],
    frame_num_target: int,
    duration_target: float,
    frame_align: FrameAlignPolicy = FrameAlignPolicy.no_extend,
) -> tuple[list[list[int]], list[int]]:
    """
    将gif按照目标帧数和帧间隔对齐
    :params
        * ``gif_infos``: 每个输入gif的帧数和帧间隔，帧间隔单位为秒
        * ``frame_num_target``: 目标gif的帧数
        * ``duration_target``: 目标gif的帧间隔，单位为秒
        * ``frame_align``: 要对齐的gif长度大于目标gif时，gif长度对齐方式
    :return
        * 输入gif的帧索引列表和目标gif的帧索引列表
    """

    frame_idxs_target: list[int] = list(range(frame_num_target))

    max_total_duration_input = max(
        frame_num * duration for frame_num, duration in gif_infos
    )
    total_duration_target = frame_num_target * duration_target
    if (
        diff_duration := max_total_duration_input - total_duration_target
    ) >= duration_target:
        diff_num = math.ceil(diff_duration / duration_target)

        if frame_align == FrameAlignPolicy.extend_first:
            frame_idxs_target = [0] * diff_num + frame_idxs_target

        elif frame_align == FrameAlignPolicy.extend_last:
            frame_idxs_target += [frame_num_target - 1] * diff_num

        elif frame_align == FrameAlignPolicy.extend_loop:
            frame_num_total = frame_num_target
            # 重复目标gif，直到每个gif总时长之差在1个间隔以内，或总帧数超出最大帧数
            while frame_num_total + frame_num_target <= meme_config.gif.gif_max_frames:
                frame_num_total += frame_num_target
                frame_idxs_target += list(range(frame_num_target))
                total_duration = frame_num_total * duration_target
                if all(
                    math.fabs(
                        round(total_duration / duration / frame_num)
                        * duration
                        * frame_num
                        - total_duration
                    )
                    <= duration_target
                    for frame_num, duration in gif_infos
                ):
                    break

    frame_idxs_input: list[list[int]] = []
    for frame_num, duration in gif_infos:
        frame_idx = 0
        time_start = 0
        frame_idxs: list[int] = []
        for i in range(len(frame_idxs_target)):
            while frame_idx < frame_num:
                if (
                    frame_idx * duration
                    <= i * duration_target - time_start
                    < (frame_idx + 1) * duration
                ):
                    frame_idxs.append(frame_idx)
                    break
                else:
                    frame_idx += 1
                    if frame_idx >= frame_num:
                        frame_idx = 0
                        time_start += frame_num * duration
        frame_idxs_input.append(frame_idxs)

    return frame_idxs_input, frame_idxs_target


Maker = Callable[[list[BuildImage]], BuildImage]

GifMaker = Callable[[int], Maker]


def merge_gif(imgs: list[BuildImage], func: Maker) -> BytesIO:
    """
    合并动图
    :params
      * ``imgs``: 输入图片列表
      * ``func``: 图片处理函数，输入imgs，返回处理后的图片
    """
    images = [img.image for img in imgs]
    gif_images = [image for image in images if getattr(image, "is_animated", False)]

    if len(gif_images) == 1:
        frames: list[IMG] = []
        frame_num = getattr(gif_images[0], "n_frames", 1)
        duration = get_avg_duration(gif_images[0])
        for i in range(frame_num):
            frame_images: list[IMG] = []
            for image in images:
                if getattr(image, "is_animated", False):
                    image.seek(i)
                frame_images.append(image.copy())
            frame = func([BuildImage(image) for image in frame_images])
            frames.append(frame.image)
        return save_gif(frames, duration)

    gif_infos = [
        (getattr(image, "n_frames", 1), get_avg_duration(image)) for image in gif_images
    ]
    target_duration = min(duration for _, duration in gif_infos)
    target_gif_idx = [
        i for i, (_, duration) in enumerate(gif_infos) if duration == target_duration
    ][0]
    target_frame_num = gif_infos[target_gif_idx][0]
    gif_infos.pop(target_gif_idx)
    frame_idxs, target_frame_idxs = get_aligned_gif_indexes(
        gif_infos, target_frame_num, target_duration, FrameAlignPolicy.extend_loop
    )
    frame_idxs.insert(target_gif_idx, target_frame_idxs)

    frames: list[IMG] = []
    for i in range(len(target_frame_idxs)):
        frame_images: list[IMG] = []
        gif_idx = 0
        for image in images:
            if getattr(image, "is_animated", False):
                image.seek(frame_idxs[gif_idx][i])
                gif_idx += 1
            frame_images.append(image.copy())
        frame = func([BuildImage(image) for image in frame_images])
        frames.append(frame.image)

    return save_gif(frames, target_duration)


def make_jpg_or_gif(imgs: list[BuildImage], func: Maker) -> BytesIO:
    """
    制作静图或者动图
    :params
      * ``imgs``: 输入图片列表
      * ``func``: 图片处理函数，输入imgs，返回处理后的图片
    """
    images = [img.image for img in imgs]
    if all(not getattr(image, "is_animated", False) for image in images):
        return func(imgs).save_jpg()

    return merge_gif(imgs, func)


def make_png_or_gif(imgs: list[BuildImage], func: Maker) -> BytesIO:
    """
    制作静图或者动图
    :params
      * ``imgs``: 输入图片列表
      * ``func``: 图片处理函数，输入imgs，返回处理后的图片
    """
    images = [img.image for img in imgs]
    if all(not getattr(image, "is_animated", False) for image in images):
        return func(imgs).save_png()

    return merge_gif(imgs, func)


def make_gif_or_combined_gif(
    imgs: list[BuildImage],
    maker: GifMaker,
    frame_num: int,
    duration: float,
    frame_align: FrameAlignPolicy = FrameAlignPolicy.no_extend,
) -> BytesIO:
    """
    使用静图或动图制作gif
    :params
      * ``imgs``: 输入图片列表
      * ``maker``: 图片处理函数生成，传入第几帧，返回对应的图片处理函数
      * ``frame_num``: 目标gif的帧数
      * ``duration``: 相邻帧之间的时间间隔，单位为秒
      * ``frame_align``: 要叠加的gif长度大于基准gif时，gif长度对齐方式
    """
    images = [img.image for img in imgs]
    if all(not getattr(image, "is_animated", False) for image in images):
        return save_gif([maker(i)(imgs).image for i in range(frame_num)], duration)

    gif_infos = [
        (getattr(image, "n_frames", 1), get_avg_duration(image))
        for image in images
        if getattr(image, "is_animated", False)
    ]
    frame_idxs_input, frame_idxs_target = get_aligned_gif_indexes(
        gif_infos, frame_num, duration, frame_align
    )

    frames: list[IMG] = []
    for i, idx in enumerate(frame_idxs_target):
        frame_images: list[IMG] = []
        gif_idx = 0
        for image in images:
            if getattr(image, "is_animated", False):
                image.seek(frame_idxs_input[gif_idx][i])
                gif_idx += 1
            frame_images.append(image.copy())
        frame = maker(idx)([BuildImage(image) for image in frame_images])
        frames.append(frame.image)

    return save_gif(frames, duration)


def to_skia_image(image: IMG) -> skia.Image:
    return skia.Image.frombytes(
        image.convert("RGBA").tobytes(), image.size, skia.kRGBA_8888_ColorType
    )


def from_skia_image(image: skia.Image) -> IMG:
    return Image.fromarray(
        image.convert(
            colorType=skia.kRGBA_8888_ColorType, alphaType=skia.kUnpremul_AlphaType
        )
    ).convert("RGBA")


def new_skia_surface(size: tuple[int, int]):
    return skia.Surfaces.MakeRasterN32Premul(size[0], size[1])


def skia_sampling_options() -> skia.SamplingOptions:
    return skia.SamplingOptions(skia.FilterMode.kLinear, skia.MipmapMode.kLinear)


def translate(text: str, lang_from: str = "auto", lang_to: str = "zh") -> str:
    appid = meme_config.translate.baidu_trans_appid
    apikey = meme_config.translate.baidu_trans_apikey
    if not appid or not apikey:
        raise MemeFeedback(
            '"baidu_trans_appid" 或 "baidu_trans_apikey" 未设置，请检查配置文件！'
        )
    salt = str(round(time.time() * 1000))
    sign_raw = appid + text + salt + apikey
    sign = hashlib.md5(sign_raw.encode("utf8")).hexdigest()
    params = {
        "q": text,
        "from": lang_from,
        "to": lang_to,
        "appid": appid,
        "salt": salt,
        "sign": sign,
    }
    url = "https://fanyi-api.baidu.com/api/trans/vip/translate"
    resp = httpx.get(url, params=params)
    result = resp.json()
    return result["trans_result"][0]["dst"]


def random_text() -> str:
    return random.choice(
        ["刘一", "陈二", "张三", "李四", "王五", "赵六", "孙七", "周八", "吴九", "郑十"]
    )


def random_image() -> bytes:
    return random.choice(
        list((resources_dir / "images" / "emojis").glob("*.png"))
    ).read_bytes()


@dataclass
class MemeProperties:
    disabled: bool = False
    labels: list[Literal["new", "hot"]] = field(default_factory=list)


def render_meme_list(
    meme_list: list[tuple["Meme", MemeProperties]],
    *,
    text_template: str = "{keywords}",
    add_category_icon: bool = True,
) -> BytesIO:
    TEXT_COLOR_NORMAL = "#444444"
    TEXT_COLOR_DISABLED = "#d3d3d3"
    BLOCK_COLOR_1 = "#f5f5f5"
    BLOCK_COLOR_2 = "#ffffff"
    BG_COLOR = "#fdfcf8"
    FONTSIZE = 30
    BLOCK_HEIGHT = 50

    icon_dir = resources_dir / "images" / "icons"
    category_image = BuildImage.open(icon_dir / "image.png").resize((30, 30))
    category_text = BuildImage.open(icon_dir / "text.png").resize((30, 30))
    category_image_disabled = BuildImage.open(icon_dir / "image_disabled.png").resize(
        (30, 30)
    )
    category_text_disabled = BuildImage.open(icon_dir / "text_disabled.png").resize(
        (30, 30)
    )
    label_new = BuildImage.open(icon_dir / "new.png").resize((30, 30))
    label_hot = BuildImage.open(icon_dir / "hot.png").resize((30, 30))

    def meme_text(number: int, meme: "Meme") -> str:
        return text_template.format(
            index=number + 1,
            key=meme.key,
            keywords="/".join(meme.keywords),
            shortcuts="/".join(
                shortcut.humanized or shortcut.key for shortcut in meme.shortcuts
            ),
            tags="/".join(meme.tags),
        )

    def text_block(
        text: str,
        max_width: int,
        block_color: ColorType,
        properties: MemeProperties,
        category: Literal["text", "image"] = "text",
    ) -> BuildImage:
        image = BuildImage.new("RGBA", (max_width, BLOCK_HEIGHT), block_color)
        if category == "text":
            icon = category_text_disabled if properties.disabled else category_text
        else:
            icon = category_image_disabled if properties.disabled else category_image
        x = 0
        if add_category_icon:
            image.paste(icon, (x + 10, 10), alpha=True)
            x += 50
        text_color = TEXT_COLOR_DISABLED if properties.disabled else TEXT_COLOR_NORMAL
        t2m = Text2Image.from_text(text, FONTSIZE, fill=text_color)
        t2m.draw_on_image(image.image, (x + 5, (image.height - t2m.height) // 2))
        x += math.ceil(t2m.longest_line) + 10
        if "new" in properties.labels:
            image.paste(label_new, (x + 5, 10), alpha=True)
            x += 35
        if "hot" in properties.labels:
            image.paste(label_hot, (x + 5, 10), alpha=True)
            x += 35
        return image

    meme_num = len(meme_list)
    cols = math.ceil(math.sqrt(meme_num / 16))
    rows = math.ceil(meme_num / cols)

    col_images: list[BuildImage] = []
    for col in range(cols):
        col_meme_list = meme_list[col * rows : (col + 1) * rows]
        max_width = max(
            math.ceil(
                Text2Image.from_text(
                    meme_text(col * rows + row, meme), FONTSIZE
                ).longest_line
            )
            + (50 if add_category_icon else 0)
            + 20
            + len(properties.labels) * 35
            for row, (meme, properties) in enumerate(col_meme_list)
        )
        col_image = BuildImage.new("RGBA", (max_width, rows * BLOCK_HEIGHT), BG_COLOR)
        for row, (meme, properties) in enumerate(col_meme_list):
            text = meme_text(col * rows + row, meme)
            block_color = BLOCK_COLOR_1 if (row + col) % 2 == 0 else BLOCK_COLOR_2
            category = "text" if meme.params_type.max_images == 0 else "image"
            col_image.paste(
                text_block(text, max_width, block_color, properties, category),
                (0, row * BLOCK_HEIGHT),
            )
        col_images.append(col_image)

    margin = 30
    frame = BuildImage.new(
        "RGBA",
        (
            sum(image.width for image in col_images) + margin * 2,
            rows * BLOCK_HEIGHT + margin * 2,
        ),
        BG_COLOR,
    )
    x = margin
    y = margin
    for image in col_images:
        frame.paste(image, (x, y))
        x += image.width
    return frame.save_png()
