# 参与贡献

## 添加一个呼吸方法

当前内置方法由 `web/index.html` 里的两张表定义；新增一个方法要**同时**改这两处（根目录 `index.html` 是同一份拷贝，记得同步）：
1. `METHODS`：加一条方法数据（示例见下）。
2. `SH`：登记这个方法的形状身份，否则会按 0 退回圆。
3. `methods/builtin/`：按 `methods/SCHEMA.md` 放一份同名 JSON（含 `meta.evidence`），作为可引用的数据镜像；**引擎目前不读取这个 JSON**，它是给人审阅/引用的。

`METHODS` 里一条长这样：
```js
{ id:"my-coh", name:"我的共振 6-6", group:"睡眠", level:1, ev:"★", shape:"wave",
  scene:["睡前"], trains:"训练目标一句话",
  phases:[{k:"inhale",s:6},{k:"exhale",s:6}], cyc:[4,6,10], rec:["4 循环","6 循环","10 循环"] }
```

`SH` 表长这样：
```js
const SH={dia:0,nose:8,coh:4,sigh:3,box:4,temp:6,co2:3};
// 0 = 圆；3/4/6/8 = 正三/四/六/八边形的边数（顶点数 = 边数）
```

**注意**：`geometry`（square / ring / wave）只是旧的描述标签，**不再决定渲染形状**；真正画什么由 `SH[id]` 决定。渲染规则：一相 = 一条边，`K = 边数 ÷ 相位数` 个循环画完图形，相位切换永远落在顶点；`hold`/`hold2` 画粉色虚线，呼吸相位画青色实线。详见 `docs/design-v3.md` §3。

字段速记：
- `group`：`减压` / `睡眠` / `运动` / `调息` 之一。
- `level`：1–5 难度点（界面上的 ● 数）。
- `ev`：证据等级（★ 起，见 `evidence/`）。
- `phases`：相位序列；`k` 只能是 `inhale` 吸 / `inhale2` 补吸（仅内置）/ `hold` 屏 / `exhale` 呼 / `hold2` 持。
- `cyc` / `rec`：三个档位各自的推荐循环数与显示文案。
- `mode`：目标模式（按次数 / 按时间 / 自由）由使用者在开始页选择并存本地设置，**不由方法数据决定**。
- `geometry`：只作描述，形状以 `SH[id]` 为准（见上）。

## 补充证据

在 `evidence/` 里更新，注明论文出处（作者、期刊、年份、样本量）；内置方法的证据等级写在 `METHODS[].ev` 与 `meta.evidence`。

## 安全

含屏息的技法必须标 `safety`（`low` 或 `high`）；`high` 会在 App 内触发屏息安全筛查（孕期 / 癫痫 / 心血管疾病等禁忌），并需在说明里写清禁忌。
