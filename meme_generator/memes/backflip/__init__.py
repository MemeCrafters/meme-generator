import math
from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.utils import FrameAlignPolicy, Maker, make_gif_or_combined_gif

img_dir = Path(__file__).parent / "images"


def backflip(images: list[BuildImage], texts, args):
    img_w, img_h = images[0].size
    length = math.sqrt(img_w * img_w + img_h * img_h)
    frame_w = int(length * 1.3)
    bounce_h = img_h * 1.2
    frame_h = int(bounce_h + length / 2 + img_h * 0.6)
    center_x = frame_w / 2
    ground_y = frame_h - img_h / 2

    total_frames = 30
    bounce1_range = (0.0, 0.3)
    bounce2_range = (0.3, 0.6)
    rise_range = (0.6, 0.65)
    flip_range = (0.65, 0.95)
    land_range = (0.95, 1.0)

    def maker(i: int) -> Maker:
        def make(imgs: list[BuildImage]) -> BuildImage:
            t = i / total_frames

            if bounce1_range[0] <= t < bounce1_range[1]:
                local_t = (t - bounce1_range[0]) / (bounce1_range[1] - bounce1_range[0])
                y = -4 * bounce_h * (local_t - 0.5) ** 2 + bounce_h
                rot = 45 * (1 - 2 * abs(local_t - 0.5))
            elif bounce2_range[0] <= t < bounce2_range[1]:
                local_t = (t - bounce2_range[0]) / (bounce2_range[1] - bounce2_range[0])
                y = -4 * bounce_h * (local_t - 0.5) ** 2 + bounce_h
                rot = -45 * (1 - 2 * abs(local_t - 0.5))
            elif rise_range[0] <= t < rise_range[1]:
                local_t = (t - rise_range[0]) / (rise_range[1] - rise_range[0])
                y = bounce_h - bounce_h * (1 - local_t) ** 2
                rot = 0.0
            elif flip_range[0] <= t < flip_range[1]:
                local_t = (t - flip_range[0]) / (flip_range[1] - flip_range[0])
                y = bounce_h
                rot = 360 * local_t
            elif land_range[0] <= t < land_range[1]:
                local_t = (t - land_range[0]) / (land_range[1] - land_range[0])
                y = bounce_h - bounce_h * local_t**2
                rot = 0.0
            else:
                y = ground_y
                rot = 0.0

            frame = BuildImage.new("RGBA", (frame_w, frame_h))
            img = imgs[0].convert("RGBA").rotate(-rot, expand=True)
            frame.paste(
                img,
                (int(center_x - img.width / 2), int(ground_y - y - img.height / 2)),
                alpha=True,
            )
            return frame

        return make

    return make_gif_or_combined_gif(
        images, maker, total_frames, 0.05, FrameAlignPolicy.extend_loop
    )


add_meme(
    "backflip",
    backflip,
    min_images=1,
    max_images=1,
    keywords=["后空翻"],
    date_created=datetime(2025, 6, 29),
    date_modified=datetime(2025, 6, 29),
)
