from pathlib import Path
from typing import List

from PIL.Image import Image as IMG
from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.utils import save_gif

img_dir = Path(__file__).parent / "images"

import sys

import cv2
import dlib
import numpy as np


def hog_anime_face_detect(image_path, model_path):
    img = cv2.imread(image_path) if type(image_path) == str else image_path  # 读取图片
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # 图片灰度化
    img_gray = cv2.equalizeHist(img_gray)  # 直方图均衡化
    face_detector = dlib.simple_object_detector(str(model_path))  # 加载检测器
    faces = face_detector(img_gray)

    return faces


def remake(images: List[BuildImage], texts, args):
    img = images[0].convert("RGBA").square().resize((289, 138))
    user = images[1].convert("RGB").copy()

    image = np.array(user.image)
    user_face = hog_anime_face_detect(image, img_dir / "hog_anime_face_detect.svm")
    if len(user_face) > 0:
        rectangle = user_face[0]
        x = rectangle.left()
        y = rectangle.top()
        w = rectangle.right()
        h = rectangle.bottom()
        user = user.copy().crop((x, y, w, h)).convert("RGBA")
        user = user.resize((68, 68)).rotate(5)
    else:
        user = user.convert("RGBA").resize((68, 68))

    # fmt: off
    locs = (
        (((30, 1), (258, 1), (268, 138), (1, 138)), (230, 26)),
        (((30, 1), (258, 1), (268, 138), (1, 138)), (210, 22)),
        (((30, 1), (258, 1), (268, 138), (1, 138)), (195, 20)),
        (((30, 1), (258, 1), (268, 138), (1, 138)), (190, 20)),

        (((30, 1), (258, 1), (268, 138), (1, 138)), (184, 60)),
        (((30, 1), (258, 1), (268, 138), (1, 138)), (0, 0)),

        (((30, 1), (298, -5), (278, 158), (-15, 138)), (145, 0)),
        (((30, 1), (298, -5), (278, 158), (-15, 138)), (140, 0)),
        (((30, 1), (298, -5), (278, 158), (-15, 138)), (130, -2)),
        (((30, 1), (298, -5), (278, 158), (-15, 138)), (120, -4)),
        (((30, 1), (298, -5), (278, 158), (-15, 138)), (110, -4)),
        (((30, 1), (298, -5), (278, 158), (-15, 138)), (100, -6)),
        (((30, 1), (298, -5), (278, 158), (-15, 138)), (100, -6)),
        (((30, 1), (298, -5), (278, 158), (-15, 138)), (90, -6)),
    )
    # fmt: on
    frames: List[IMG] = []
    for i in range(14):
        frame = BuildImage.new("RGBA", (480, 270), "white")
        bg = BuildImage.open(img_dir / f"{i}.png")
        frame.paste(bg, (0, 0))
        if i != 4 and i != 5:
            points, pos = locs[i]
            frame.paste(img.perspective(points), pos, below=True)
            frames.append(frame.image)
        elif i == 4:
            points, pos = locs[i]
            frame.paste(user, pos, below=True)
            frames.append(frame.image)
            frames.append(frame.copy().image)
            frames.append(frame.copy().image)
        else:
            frames.append(frame.image)
            frames.append(frame.image)

    return save_gif(frames, 0.1)


add_meme("remake", remake, min_images=2, max_images=2, keywords=["创", "泥头车"])
