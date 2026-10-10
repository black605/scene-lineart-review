# scene-lineart-review · 场景线稿审查

审查 AI 生成的场景线稿/草图能不能承载 UI、跨屏是否一致，给出「通过 / 返工」结论、标注图和返工提示词。适用于「出图 → 审图 → 返工」循环。

核心做法：线稿阶段就按最终画布叠上 UI 占位去量。问题在灰稿阶段改最便宜，上色后再改成本翻倍。

## 能做什么

- 按目标画布（默认 1280×800）统一尺寸、画坐标网格、叠 UI 占位
- 按 12 项清单逐条测量：标签带、上下建筑间距、Dock 区、卡片区、入口露出、剪影辨识、数量与语义、跨屏一致、背景语义、角色站位、改动核对、交付处理
- 把问题分成「需返工（改场景几何）」和「后续处理（UI 层小调即可）」
- 产出每屏标注图、状态记录、可直接交给生图 agent 的返工提示词（附验收坐标）

审查者只负责判断和写任务单，不直接生图。

## 目录

```
scene-lineart-review/
├── SKILL.md              # Skill 主体：依据、流程、清单、分级规则、产出格式
└── scripts/
    └── annotate.py       # 标注图脚本（与 SKILL.md 第 6 节代码一致）
```

## 安装

把整个文件夹放进 agent 的 skills 目录，例如 Claude Code：

```bash
git clone https://github.com/black605/scene-lineart-review ~/.claude/skills/scene-lineart-review
```

其他支持 `SKILL.md` 的 agent，放到各自的 skills 目录即可。

## 标注脚本

需要 Python 3 和 Pillow（`pip install pillow`），中文字体会自动查找（macOS 用苹方 / 冬青，Linux 用 Noto CJK）。

```bash
python scripts/annotate.py spec.json
```

spec 示例见 `scripts/annotate.py` 文件头。输出为原图叠加半透明 UI 占位、热区虚线、红框（返工）/ 黄框（后续）编号，底部附结论和逐条说明。

## 注意

Skill 里的像素数值（顶栏 72、标签高 40、标签带 52、横移上限 40 等）是来自一个 1280×800 横屏项目的**默认值**。新项目请先换成自己的 UI 规范；没有规范时才用默认值，并在报告里标注「默认值，待确认」。
