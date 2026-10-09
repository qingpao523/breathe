# 方法格式（Method Schema）

一个呼吸方法就是一段 JSON：**新增方法 = 加一段配置，不用写代码。**

## 字段

| 字段 | 说明 |
|---|---|
| id | 唯一标识，用作文件名 |
| name | 显示名 |
| phases | 相位序列（见下） |
| cycles | 循环次数（mode=free 时可忽略） |
| mode | timed 按循环数 / free 自由练习 |
| geometry | square 方形轨道 / ring 圆环 / wave 连续波 |
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
