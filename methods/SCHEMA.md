# 方法格式（Method Schema）

注意：引擎现在不读取 JSON。方法定义位于 web/index.html 内的 METHODS 和 SH 中。此文件夹中的 JSON 文件仅是设计记录。

呼吸方法是一个定义块：添加方法意味着在SH中添加配置数据和形状条目，而无需编写引擎代码。

## 字段

| 字段 | 说明 |
|---|---|
| id | 唯一标识，用作文件名 |
| name | 显示名 |
| phases | 相位序列（见下） |
| cycles | 循环次数（mode=free 时可忽略） |
| mode | 目标模式：cyc表示循环或重复，time表示持续时间，free表示自由练习。这取代了旧的 timed/free 措辞。 |
| geometry | 已弃用：形状由 web/index.html 中的 SH[id] 决定，而不是由此 JSON 字段决定。 数字为多边形边数； 0 表示圆形。 |
| meta | 场景标签、来源、安全、证据 |

## 相位 k

| k | 含义 | 范围 |
|---|---|---|
| inhale | 吸 | 全部 |
| hold | 屏 | 全部 |
| exhale | 呼 | 全部 |
| hold2 | 持 | 全部 |
| inhale2 | 补吸 | **仅内置** |

## 约束

- 时长单位秒，精度 0.5（内置可用 0.25）
- 含屏息的方法必须标 meta.safety（low / high）
- meta.evidence 仅内置需要；自建留空显示未标注来源
- 引擎不读取JSON；上述字段遵循 web/index.html 中的 METHODS 和 SH。
