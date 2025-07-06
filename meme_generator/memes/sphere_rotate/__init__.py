import math
import struct
from datetime import datetime

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


def sphere_rotate(images: list[BuildImage], texts, args):
    total_frames = 60

    sksl_code = """
        uniform shader image;
        uniform float angle;
        uniform float2 canvas_size;
        uniform float2 image_size;

        const float PI = 3.14159265359;

        // Y轴旋转矩阵
        mat3 rotate_y(float a) {
            float s = sin(a);
            float c = cos(a);
            return mat3(
                c, 0, s,
                0, 1, 0,
                -s, 0, c
            );
        }

        // 光线与球体相交检测
        // ro: 光线原点, rd: 光线方向, r: 球体半径
        // 返回 vec2(近交点距离, 远交点距离), 如果不相交则都为-1.0
        vec2 intersect_sphere(vec3 ro, vec3 rd, float r) {
            float b = dot(ro, rd);
            float c = dot(ro, ro) - r * r;
            float h = b * b - c;
            if (h < 0.0) {
                return vec2(-1.0);
            }
            float sqrt_h = sqrt(h);
            return vec2(-b - sqrt_h, -b + sqrt_h);
        }

        // 将球体表面的3D坐标点转换为2D纹理UV坐标 (等距柱状投影)
        vec2 get_sphere_uv(vec3 p) {
            p = normalize(p);
            float u = 0.5 + atan(p.z, p.x) / (2.0 * PI);
            float v = 0.5 + asin(p.y) / PI;
            return vec2(u, v);
        }

        half4 main(vec2 coord) {
            // 将屏幕像素坐标转换为标准化坐标
            vec2 uv = (2.0 * coord - canvas_size.xy) / canvas_size.y;

            // 设置相机 (光线追踪)
            vec3 ro = vec3(0.0, 0.0, 3.5);
            vec3 rd = normalize(vec3(uv, -2.0));

            // 应用Y轴旋转
            mat3 rot = rotate_y(angle);
            ro = rot * ro;
            rd = rot * rd;

            float radius = 1.2;

            // 寻找光线与完整球体的所有交点
            vec2 t = intersect_sphere(ro, rd, radius);
            float t_hit = -1.0;

            // 测试近处的交点
            if (t.x > 0.0) {
                vec3 p1 = ro + rd * t.x;
                if (p1.x >= 0.0) {
                    t_hit = t.x;
                }
            }

            // 如果近处交点无效，则测试远处的交点 (处理看到内壁的情况)
            if (t_hit < 0.0 && t.y > 0.0) {
                vec3 p2 = ro + rd * t.y;
                if (p2.x >= 0.0) {
                    t_hit = t.y;
                }
            }

            // 如果找到了有效的交点，进行着色
            if (t_hit > 0.0) {
                vec3 pos = ro + rd * t_hit;
                vec3 normal = normalize(pos);
                float facing = dot(rd, normal);

                vec2 tex_uv = get_sphere_uv(pos);
                vec2 tex_coords = tex_uv * image_size;
                half4 tex_color = image.eval(tex_coords);

                if (facing < 0.0) {
                    // 外表面: 直接使用纹理颜色
                    return tex_color;
                } else {
                    // 内表面: 将纹理颜色变暗
                    return tex_color * half4(0.7, 0.7, 0.7, 1.0);
                }
            }

            return half4(0.0);
        }
    """
    effect = skia.RuntimeEffect.MakeForShader(sksl_code)

    def maker(i: int) -> Maker:
        def make(imgs: list[BuildImage]):
            img = imgs[0].convert("RGBA")
            canvas_w, canvas_h = (300, 300)
            surface = new_skia_surface((canvas_w, canvas_h))
            canvas = surface.getCanvas()

            angle = i / total_frames * math.pi * 2

            values = []
            for uniform in effect.uniforms():
                if uniform.name == "angle":
                    values.append(struct.pack("<f", angle))
                elif uniform.name == "canvas_size":
                    values.append(struct.pack("<f", canvas_w))
                    values.append(struct.pack("<f", canvas_h))
                elif uniform.name == "image_size":
                    values.append(struct.pack("<f", img.width))
                    values.append(struct.pack("<f", img.height))
            uniforms = skia.Data.MakeWithCopy(b"".join(values))

            skia_image = to_skia_image(img.image)
            image_shader = skia_image.makeShader(skia_sampling_options())
            shader = effect.makeShader(uniforms, image_shader, 1)

            paint = skia.Paint()
            paint.setShader(shader)
            canvas.drawPaint(paint)
            frame = BuildImage(from_skia_image(surface.makeImageSnapshot()))
            return frame

        return make

    return make_gif_or_combined_gif(images, maker, total_frames, 0.04)


add_meme(
    "sphere_rotate",
    sphere_rotate,
    min_images=1,
    max_images=1,
    keywords=["球面旋转"],
    date_created=datetime(2025, 7, 6),
    date_modified=datetime(2025, 7, 6),
)
