任务脚本（一次性中转，导出为本地 p1.py 后执行）。
```python
import pathlib
q = chr(34); bs = chr(92)
a = pathlib.Path("archive/v2-ui-source.md").read_text(encoding="utf-8")

for c in "()[ ]*_#+-.`!<>":

    a = a.replace(bs + c, c)
i = a.find("<!DOCTYPE"); j = a.find("</html>") + 7
h = a[i:j]

# 1) 方法分组 -> 四大板块
P = [("dia","睡眠"),("sigh","减压"),("coh","睡眠"),("nose","运动"),
     ("box","减压"),("temp","运动"),("imt","运动"),("co2","调息")]
n = 0
for mid, g in P:
    k = h.find("id:" + q + mid + q)
    if k < 0: continue
    p = h.find("group:" + q, k)
    if p < 0: continue
    s = p + 7
    e = h.find(q, s)
    h = h[:s] + g + h[e:]
    n += 1

oa = "[" + q + "基础" + q + "," + q + "节律" + q + "," + q + "效率" + q + "," + q + "进阶" + q + "]"
na = "[" + q + "减压" + q + "," + q + "睡眠" + q + "," + q + "运动" + q + "," + q + "调息" + q + "]"
h = h.replace(oa, na)

# 2) 字体族：-apple-system 在安卓 WebView 上失效
f1 = "font-family:-apple-system,BlinkMacSystemFont,system-ui,sans-serif"
f2 = "font-family:-apple-system,BlinkMacSystemFont," + q + "PingFang SC" + q + "," + q + "Noto Sans CJK SC" + q + ",system-ui,sans-serif"
h = h.replace(f1, f2)

pathlib.Path("web/index.html").write_text(h, encoding="utf-8")
pathlib.Path("index.html").write_text(h, encoding="utf-8")
print("bytes", len(h), "regrouped", n, "arr", na in h, "font", f2 in h)
```
