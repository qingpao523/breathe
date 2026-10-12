# PITFALLS · 真机与构建踩坑记录
> 只收录**已复现 / 已实机确认**的事实。每条给出：现象 / 根因 / 验证方法 / 对策。
> 环境：macOS + Android SDK build-tools 34.0.0（aapt2、d8 8.2.2-dev）+ javac `-source 8 -target 8`；出包链路见 `build_app.py`。

## 速查表

| # | 坑 | 一句话对策 |
|---|---|---------------|
| 1 | 平台全屏主题在部分 ROM 上启动闪退 | 不要用 `Theme.NoTitleBar.Fullscreen` |
| 2 | `aapt2 link` 无资源输入 → 40 字节非法 `resources.arsc` | 先 `aapt2 compile`，再用**位置参数**把 res.zip 传给 link |
| 3 | `-R` 是 overlay 语义，不是"资源输入" | 普通资源用位置参数；overlay 才用 `-R` + `--auto-add-overlay` |
| 4 | d8 只传入口 class → 内部类静默不进 dex | d8 传全部 `*.class` |
| 5 | 本机 shell：中文 / 特殊字符 / 长命令挂死或写坏文件 | 命令行只用 ASCII + 脚本文件 + 非 shell 通道落盘中文 |

---

## 1\. Android 主题：`Theme.NoTitleBar.Fullscreen`

**现象**
- manifest 写 `android:theme="@android:style/Theme.NoTitleBar.Fullscreen"` 的 APK，在小米等部分机型上**点图标即闪退**（无界面，来不及打日志）。
- 同一个包：`apksigner verify` 全绿、`aapt2 dump badging` 正常输出 label / icon / launchable-activity —— 静态检查完全看不出问题。

**根因**
- 这是平台内置主题，部分定制 ROM 不保证可用；Activity 主题解析/应用在启动早期失败，直接崩溃。
- 打包链路（aapt2 link → zipalign → apksigner）只校验包结构与签名，不校验运行时主题可用性。

**验证方法**
- 真机安装启动（`adb install -r` 后点图标）；对比"去掉 `android:theme` 重新打包"的版本。
- 只跑 `apksigner verify` / `aapt2 dump badging` 会误判为"包没问题"。

**对策**
- 不指定该主题；需要全屏走代码路径（窗口 flags）或自定义 theme。
- 当前出包模板 `andapp/AndroidManifest.xml` 已去掉 `android:theme`；旧壳 `android/AndroidManifest.xml` 里还留着，模仿时别抄旧文件。

---

## 2\. aapt2：无资源输入产出 40 字节 `resources.arsc`

**现象**
- `aapt2 link` 不传任何资源输入时**不报错**，照常产出 APK；但包内 `resources.arsc` 只有 **40 字节**。
- 这种包装到真机**启动即崩**；`aapt2 dump resources` 看不到任何资源内容（空表）。

**根因**
- link 在没有资源输入时仍会写一个最小空资源表（表头 + 空 package），不是运行时能正常解析的完整资源表。

**验证方法**
- `unzip -l app.apk` 看 `resources.arsc` 大小：40 = 空表；正常出包 `breathe-v1.3.apk` 里是 **1776 字节**。
- 本机复现（已跑通）：
    - 只给 manifest：`aapt2 link -o nores.apk -I android.jar --manifest M.xml` → `unzip -l` 显示 `resources.arsc` 40 字节，hexdump 头 `02 00 0c 00 28 00 ...`。
    - 用真实资源：`aapt2 compile --dir android/res -o res.zip` → `aapt2 link ... res.zip`（位置参数）→ `resources.arsc` 1776 字节。

**对策**
- 必须给真实资源：先 `aapt2 compile --dir <res-dir> -o res.zip`，再 `aapt2 link ... <位置参数> res.zip`。
- `build_app.py` 已是正确写法：`aapt2 compile --dir android/res -o andapp/res.zip`，link 时把 `andapp/res.zip` 放在位置参数位。

---

## 3\. `-R` 不是"指定资源"，是 overlay

**现象**
- `aapt2 link ... -R res.zip` 报错并中止，原文：
```
/tmp/res.zip@values_strings.arsc.flat: error: resource string/app_name does not override an existing resource.
/tmp/res.zip@values_strings.arsc.flat: note: define an <add-resource> tag or use --auto-add-overlay.
/tmp/res.zip@values_strings.arsc.flat: error: resource string/app_name2 does not override an existing resource.
error: failed to merge resource table.
error: failed parsing overlays.
```

**根因**
- `-R` 语义是 overlay（覆盖包），要求被覆盖资源已存在；把编译产物当普通资源传进去必然失败。

**验证方法**
- 同一条命令：`-R` 失败；把 `res.zip` 放到位置参数位（`aapt2 link -o out.apk -I android.jar --manifest M.xml res.zip`）成功。
- overlay 的正确用法是配合 `--auto-add-overlay` 或真的做覆盖。

**对策**
- 普通资源：位置参数；overlay：`-R` + `--auto-add-overlay`，两者别混。

---

## 4\. d8 漏打内部类：编译/打包/签名全过，桥方法静默失效

**现象**
- `MainActivity` 里有内部类 `Bridge`（方法上用 `@JavascriptInterface` 暴露给 WebView）。只把 `MainActivity.class` 传给 d8 时，`MainActivity$Bridge`、`MainActivity$Bridge$1`、`MainActivity$Bridge$2` 都不会进 `classes.dex`。
- 结果：网页里 `window.AndroidBridge.vibrate / keepScreenOn / toast` 静默无效（前端调用包了 try/catch，连报错都看不到）；而 javac、d8、zipalign、apksigner 全部成功。

**根因**
- d8 只打包显式传入的 class 文件；javac 为内部类/匿名类生成独立 `.class`，不会被自动带上。
- 出包脚本用 `javac -source 8 -target 8`，没有 nestmates 元数据，d8 不报错、直接静默漏打；本机已复现。

**验证方法**
- 最小复现：`javac -source 8 -target 8` 编译含内部类 `In` 的 `T`；只传 `T.class` 给 d8 → 成功产出 `classes.dex`，但 `dexdump -f classes.dex | grep 'T$In'` 命中 0；把 `T$In.class` 一起传 → 能命中。
- 检查真实产物：`unzip -p app.apk classes.dex | strings | grep Bridge`。正常出包能命中；`andapp/classes/com/qingpao/app/` 下确实有 `MainActivity.class` 和 3 个嵌套类，共 4 个 class。

**对策**
- d8 输入用**全部** `*.class`：`glob.glob('classes/**/*.class', recursive=True)`（`build_app.py` 已这样写）。
- 只传入口 class 的极简脚本（如 `build_min.py` 的 d8 行）只适用于没有内部类的 demo。

---

## 5\. 本机 shell：中文 / 特殊字符 / 长命令会挂死或写坏文件

**现象**
- 命令行里出现中文字面量：不报错，但中文会被替换成 `-` 写进文件（静默写坏）；叠加长 heredoc / 反引号 / 特殊字符时，整条命令挂死约 **300 秒**并重置 shell。
- 单条命令超过约 60–80 字符容易触发；一条命令里塞多个 heredoc 时，正文可能被当命令执行，或 heredoc 提前结束。
- 典型症状：`bash: -source: command not found`、`bash: -R: command not found` —— 其实是 heredoc 正文里的行被拿去执行了。

**根因**
- 该 shell 通道对非 ASCII 与部分特殊字符的预处理有缺陷：命令还没到 shell 就已经被改写/截断，超时后前端重置会话。

**验证方法**
- 写一个含中文的小文件再 `xxd`：字节全是 `0x2d`（`-`）；同样的中文经 Unicode 保真的通道（MCP 服务导出 → `curl` 落盘）写出来再 `cat`，显示正常。
- 对照：纯 ASCII 短命令立即返回；含中文字面量的命令在本环境下失败/超时。

**对策**
- 命令行只写 ASCII；中文不要出现在命令、参数、heredoc 正文里。
- 需要写中文文件时，用非 shell 的 Unicode 保真通道落盘（例如 MCP 服务生成内容 → 导出下载 URL → `curl -o` 到本地），或在脚本源里用 `\uXXXX` 转义。
- 复杂操作先落成脚本文件再执行；命令保持短（< ~60–80 字符）；一条命令只放一个 heredoc，大文件分块追加并用 `wc -c` / `md5` 校验。
- 路径/文件名含中文时用 glob 或变量间接引用，不要把中文写进命令。

---

## 附：环境快照
- 出包脚本：`build_app.py`（aapt2 compile → link → javac → d8 全部 class → 手写 classes.dex 进 zip → zipalign → apksigner）。
- build-tools：34.0.0；d8：8.2.2-dev；javac：`-source 8 -target 8`；minSdk 26 / targetSdk 34。
- 本文的真机结论（闪退、桥失效）来自项目实机验证记录；40 / 1776 字节、`-R` 报错原文、d8 漏类已在本机用 build-tools 34 复现。
