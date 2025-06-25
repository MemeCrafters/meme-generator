import math
import struct
from datetime import datetime
from pathlib import Path

import skia
from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.utils import (
    Maker,
    from_skia_image,
    make_gif_or_combined_gif,
    new_skia_surface,
    skia_sampling_options,
    to_skia_image,
)

img_dir = Path(__file__).parent / "images"


def flick(images: list[BuildImage], texts, args):
    sksl_code = """
        uniform shader image;
        uniform float width;
        uniform float height;
        uniform float offset;
        uniform float angle;

        half4 main(float2 coord) {
            float factor = 1.0 - coord.y / height;
            float dx = factor * offset;
            float a = angle * factor;
            float2 center = float2(width * 0.5, height * 0.5);
            coord -= center;
            float ca = cos(a);
            float sa = sin(a);
            float2 rotated = float2(
                coord.x * ca - coord.y * sa,
                coord.x * sa + coord.y * ca
            );
            coord = rotated + center;
            coord.x += dx;
            return image.eval(coord);
        }
    """
    effect = skia.RuntimeEffect.MakeForShader(sksl_code)

    def maker(i: int) -> Maker:
        def make(imgs: list[BuildImage]):
            img = imgs[0].convert("RGBA").square().resize((240, 240))

            if i < 3:
                return img
            elif i < 12:
                hand = BuildImage.open(img_dir / f"{i - 3}.png")
                return img.paste(hand, (0, 0), alpha=True)
            else:
                width, height = img.size
                amplitude = width / 2.0
                omega = 2.0 * math.pi / 5.0
                decay = 0.1
                max_angle = 0.5
                t = i - 3
                damping = math.exp(-decay * t)
                offset = amplitude * math.sin(omega * t) * damping
                angle = max_angle * math.sin(omega * t) * damping

                values = []
                for uniform in effect.uniforms():
                    if uniform.name == "width":
                        values.append(struct.pack("<f", width))
                    elif uniform.name == "height":
                        values.append(struct.pack("<f", height))
                    elif uniform.name == "offset":
                        values.append(struct.pack("<f", offset))
                    elif uniform.name == "angle":
                        values.append(struct.pack("<f", angle))
                uniforms = skia.Data.MakeWithCopy(b"".join(values))

                skia_image = to_skia_image(img.image)
                image_shader = skia_image.makeShader(skia_sampling_options())
                shader = effect.makeShader(uniforms, image_shader, 1)

                surface = new_skia_surface(img.size)
                canvas = surface.getCanvas()
                paint = skia.Paint()
                paint.setShader(shader)
                canvas.drawPaint(paint)
                frame = BuildImage(from_skia_image(surface.makeImageSnapshot()))
                if i == 12:
                    hand = BuildImage.open(img_dir / f"{i - 3}.png")
                    frame.paste(hand, (0, 0), alpha=True)
                return frame

        return make

    return make_gif_or_combined_gif(images, maker, 30, 0.05)


add_meme(
    "flick",
    flick,
    min_images=1,
    max_images=1,
    keywords=["弹", "脑瓜崩"],
    date_created=datetime(2025, 6, 22),
    date_modified=datetime(2025, 6, 22),
)
