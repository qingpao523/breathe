# 参与贡献

## 添加一个呼吸方法

在 `methods/builtin/` 新建一个 JSON（文件名用 id）：

```json
{
  "id": "my-method",
  "name": "方法名",
  "phases": [{"k":"inhale","s":4},{"k":"exhale","s":6}],
  "cycles": 10,
  "mode": "timed",
  "geometry": "ring",
  "meta": {"scene":["减压"],"source":"自建","safety":"none"}
}
```

- `k` 只能是 `inhale` 吸 / `hold` 屏 / `exhale` 呼 / `hold2` 持 / `inhale2` 补吸（仅内置）
- `geometry`：`square` 方形轨道 / `ring` 圆环 / `wave` 连续波
- `mode`：`timed` 按循环数 / `free` 自由练习

## 补充证据

在 `evidence/` 里更新，注明论文出处（作者、期刊、年份、样本量）。

## 安全

含屏息的技法必须标 `safety`（`low` 或 `high`），并在说明里写清禁忌。
