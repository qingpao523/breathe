# 呼吸 Breathe

呼吸法跟练 App。**方法即数据**：每个方法可溯源，用户也能自己加。

## 为什么做这个
市面 App 只告诉你吸几秒、屏几秒，不告诉你**这些数字从哪来**、证据多强。本项目把证据做进产品：每个方法标证据等级、论文出处、已知反证。

## 方法即数据
一个方法 = 一段 JSON：四种相位 inhale/hold/exhale/hold2 足够表达绝大多数呼吸法。**新增方法 = 加一段配置，不用写代码。**

## 结构
evidence/ 证据库 | methods/ 内置方法 | web/ 单文件引擎 | android/ 安卓实现 | docs/ 设计文档

## 参与
加方法：往 methods/builtin/ 加 JSON，附来历。补证据：更新 evidence/，注明出处。改代码：先读 docs/design-v3.md。

## 许可
代码 MIT；evidence/ 与 docs/ 为 CC BY 4.0。
