<div align="center">

<img src="https://s2.loli.net/2023/03/26/4URd1BKj3ToycLl.png" width=200 />

# meme-generator

_✨ 表情包生成器，用于制作各种沙雕表情包 ✨_

<p align="center">
  <img src="https://img.shields.io/github/license/MemeCrafters/meme-generator" alt="license">
  <img src="https://img.shields.io/badge/python-3.9+-blue.svg" alt="Python">
  <a href="https://pypi.org/project/meme-generator">
    <img src="https://badgen.net/pypi/v/meme-generator" alt="pypi">
  </a>
  <a href="https://jq.qq.com/?_wv=1027&k=wDVNrMdr">
    <img src="https://img.shields.io/badge/QQ%E7%BE%A4-682145034-orange" alt="qq group">
  </a>
</p>

</div>

> [!NOTE]
> 本项目另有 Rust 重构版 [--> meme-generator-rs <--](https://github.com/MemeCrafters/meme-generator-rs)
> 
> 拥有更小的内存占用和更快的运行速度，欢迎使用！

## 表情列表

表情详细信息、表情预览等可以在 [--> 表情列表 <--](https://github.com/MemeCrafters/meme-generator/wiki/%E8%A1%A8%E6%83%85%E5%88%97%E8%A1%A8) 查看

## 安装、使用、配置

详见 Wiki：[--> Wiki <--](https://github.com/MemeCrafters/meme-generator/wiki)

## 其他表情

可以加载非本仓库内置的表情，参考 [--> 加载其他表情 <--](https://github.com/MemeCrafters/meme-generator/wiki/%E5%8A%A0%E8%BD%BD%E5%85%B6%E4%BB%96%E8%A1%A8%E6%83%85)

其他表情仓库：
- [MemeCrafters/meme-generator-contrib](https://github.com/MemeCrafters/meme-generator-contrib) meme-generator 额外表情仓库
- [anyliew/meme_emoji](https://github.com/anyliew/meme_emoji) 更多热门表情包模板
- [LRZ9712/tudou-meme](https://github.com/LRZ9712/tudou-meme) 手搓的一些表情包模版

## 已知问题

- Windows 下程序无报错退出

需要安装 [Visual C++ 运行时](https://aka.ms/vs/17/release/VC_redist.x64.exe)

相关 Issue：https://github.com/kyamagu/skia-python/issues/289

- Linux 下字体异常

设置 locate 为英文：
```
export LANG=en_US.UTF-8
```

相关 Issue：https://github.com/rust-skia/rust-skia/issues/963

## 声明

本仓库的表情素材等均来自网络，如有侵权请联系作者删除

## 鸣谢

本仓库的表情整合自原 [nonebot-plugin-petpet](https://github.com/noneplugin/nonebot-plugin-petpet) 和 [nonebot-plugin-memes](https://github.com/noneplugin/nonebot-plugin-memes) 仓库

感谢以下开发者作出的贡献：

<a href="https://github.com/noneplugin/nonebot-plugin-petpet/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=noneplugin/nonebot-plugin-petpet&max=1000" />
</a>

部分表情素材或代码参考了以下项目，感谢这些项目的开发者们

- [Ailitonia/omega-miya](https://github.com/Ailitonia/omega-miya) 基于nonebot2的qq机器人
- [FloatTech/ZeroBot-Plugin](https://github.com/FloatTech/ZeroBot-Plugin) 基于 ZeroBot 的 OneBot 插件
- [HibiKier/zhenxun_bot](https://github.com/HibiKier/zhenxun_bot) 基于 Nonebot2 和 go-cqhttp 开发，以 postgresql 作为数据库，非常可爱的绪山真寻bot
- [SAGIRI-kawaii/sagiri-bot](https://github.com/SAGIRI-kawaii/sagiri-bot) 基于Graia Ariadne和Mirai的QQ机器人 SAGIRI-BOT
- [Dituon/petpet](https://github.com/Dituon/petpet) Mirai插件 生成各种奇怪的图片
- [kexue-z/nonebot-plugin-nokia](https://github.com/kexue-z/nonebot-plugin-nokia) 诺基亚手机图生成
- [RafuiiChan/nonebot_plugin_charpic](https://github.com/RafuiiChan/nonebot_plugin_charpic) 字符画生成插件
