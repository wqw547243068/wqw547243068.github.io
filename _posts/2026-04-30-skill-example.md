---
layout: post
title:   优质 Skills 汇总
date:   2026-04-30 21:20:00
categories: 大模型
tags:  skill mcp 龙虾
excerpt: 总结各类实用 Skills 
mathjax: true
permalink: /skill_set
---

* content
{:toc}


# Skill 应用


## Skill 原理

详见站内专题：[Skill 技术专题](skill)



## ppt 制作

ppt制作技能

GitHub 上和 PPT 相关的 Skill 项目。

结论： 
- 做 PPT 这件事，已经不只是“让 AI 帮你写几页内容”了，而是分成了好几条路线。

路线
 
（1）如果做漂亮网页 PPT，优先看：
- guizang-ppt-skill：电子杂志感很强，适合发布会、分享、视觉化报告。
- next-slide：产品化程度高，零依赖 HTML，中文场景友好。
- html-ppt-skill：更像模板工厂，适合研究通用 HTML PPT 生成。
- revealjs-ppt-skill：标准 reveal.js 路线，适合技术分享、课程、文档型演示。

（2）如果你最终要的是可编辑 PPTX，可以重点看：
- anthropics/skills/pptx：官方基线型 PPTX skill。
- MiniMax-AI/pptx-generator：PptxGenJS 路线，生成、读取、编辑都比较工程化。
- powerpoint-skill：适合研究 HTML 到 PPTX 的高保真转换。
- mcp-server-ppt：更偏 Windows + Office 自动化场景。

（3）想做“高级感网页 PPT”，先看
- next-slide + guizang-ppt-skill + html-ppt-skill。

（4）想做“真正可编辑的 PPTX”，先看：
- anthropics/pptx + MiniMax pptx-generator。

（5）想把 PDF、图片、论文转成演示，可以看：
- glmv-pdf-to-ppt、image-to-pptx-skill、paper-slides 这类专用工具。        

## 视频制作

### ppt2video

[ppt2video](https://github.com/iburn78/ppt2video)

安装

```sh
pip install ppt2video
```
使用

```py
from ppt2video.tools import *

meta = Meta(
    ppt_file='your_ppt_slide.pptx',  # Name of your PPT file
    google_application_credentials='/config/google_cloud.json'  # Location and filename of your Google Cloud service account key
)

# Run the conversion
ppt_to_video(meta)
```


### slides2video


[slides2video 在线体验](https://slide2video.app/) 上传pdf/ppt，自动生成脚本+视频

开源神器 [slides2video](https://github.com/arpith/slides2video)
- 一键将 HTML 幻灯片 / PNG 素材转为带 AI 配音的 MP4 视频，深度对接豆包 TTS，搭载海量音色库，支持方言、IP 仿音、多情感与客服专属音色。
- 依托 ffmpeg + Playwright 实现无间隙音频合成，命令行极简操作，支持断点续跑、跳过重复环节，无需专业剪辑，快速产出教学、演示、自媒体视频，零基础也能批量生成高质量有声 PPT，办公与创作效率直接拉满！


# 结束
