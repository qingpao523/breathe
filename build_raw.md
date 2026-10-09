安卓版 v1 一键构建脚本。**不用 Gradle**（本机没有全局 gradle，且首次拉 AGP 依赖动辄十几分钟），直接走 `aapt2 / javac / d8 / zipalign / apksigner` 手工链路 —— 本机 `build-tools 34.0.0` \+ `platforms/android-34` \+ `~/.android/debug.keystore` 都已就位，所以这是**秒级出包**的路子。

架构选择：**WebView 壳 \+ 原生桥**。理由不是省事，而是我们已经有跑通的相位引擎（那个单文件 HTML 模板），原生侧重写一遍 canvas/状态机毫无收益。原生侧只补 3 个 Web 拿不到的能力：**振动、屏幕常亮、Toast**。后续要做的 BLE 踏频、锁屏前台服务，都可以按这个模式增量加进 Bridge。
```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 呼吸 · 安卓版 v1 一键构建：模板HTML -> 资源 -> aapt2 link -> javac -> d8 -> 注入dex -> zipalign -> 签名
import os, sys, subprocess, zipfile

ROOT = "/Users/qingpao/.dsh/handoffs/breathing-app"
SDK  = os.path.expanduser("~/Library/Android/sdk")
BT   = os.path.join(SDK, "build-tools", "34.0.0")
PLAT = os.path.join(SDK, "platforms", "android-34", "android.jar")
AND  = os.path.join(ROOT, "android")
PKG  = "com/qingpao/breathe"
OUT  = os.path.join(ROOT, "Breathe-v1-debug.apk")

def sh(name, cmd):
    print("\n=== " + name + " ===")
    p = subprocess.run(cmd, capture_output=True, text=True)
    txt = ((p.stdout or "") + (p.stderr or "")).strip()
    if txt:
        print(txt[-3000:])
    if p.returncode != 0:
        print("!!! FAILED: " + name + " rc=" + str(p.returncode))
        sys.exit(1)
    return p

for d in ["assets", "classes", "dexout", "src/" + PKG]:
    os.makedirs(os.path.join(AND, d), exist_ok=True)

# ---------- 1. 模板 HTML -> assets/index.html（并注入原生桥适配层） ----------
raw = open(os.path.join(ROOT, "tpl_raw.md"), encoding="utf-8").read()
i = raw.find("<!DOCTYPE")
j = raw.find("</html>") + 7
if i < 0 or j < 7:
    print("!!! 找不到模板 HTML，检查 tpl_raw.md")
    sys.exit(1)
html = raw[i:j]

shim = (
"<script>\n"
"(function(){\n"
"  var A = window.AndroidBridge; if(!A) return;\n"
"  window.alert = function(m){ A.toast(String(m)); };\n"
"  if(!navigator.vibrate){ navigator.vibrate = function(ms){ A.vibrate(ms||18); }; }\n"
"  A.keepScreenOn(true);\n"
"})();\n"
"</script>"
)
html = html.replace("</body>", shim + "</body>")
open(os.path.join(AND, "assets", "index.html"), "w", encoding="utf-8").write(html)
print("assets/index.html bytes =", len(html.encode("utf-8")))

# ---------- 2. AndroidManifest.xml ----------
manifest = """<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="com.qingpao.breathe"
    android:versionCode="1" android:versionName="1.0">
  <uses-sdk android:minSdkVersion="26" android:targetSdkVersion="34" />
  <uses-permission android:name="android.permission.VIBRATE" />
  <application android:label="呼吸" android:allowBackup="false"
      android:hardwareAccelerated="true"
      android:theme="@android:style/Theme.NoTitleBar.Fullscreen">
    <activity android:name=".MainActivity" android:exported="true"
        android:screenOrientation="portrait"
        android:configChanges="orientation|screenSize|keyboardHidden">
      <intent-filter>
        <action android:name="android.intent.action.MAIN" />
        <category android:name="android.intent.category.LAUNCHER" />
      </intent-filter>
    </activity>
  </application>
</manifest>
"""
open(os.path.join(AND, "AndroidManifest.xml"), "w", encoding="utf-8").write(manifest)

# ---------- 3. MainActivity.java ----------
java = r"""package com.qingpao.breathe;

import android.app.Activity;
import android.os.Build;
import android.os.Bundle;
import android.os.VibrationEffect;
import android.os.Vibrator;
import android.os.VibratorManager;
import android.view.WindowManager;
import android.webkit.JavascriptInterface;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.Toast;

public class MainActivity extends Activity {

    private WebView web;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        web = new WebView(this);
        setContentView(web);

        WebSettings s = web.getSettings();
        s.setJavaScriptEnabled(true);
        s.setDomStorageEnabled(true);
        s.setAllowFileAccess(true);
        s.setAllowContentAccess(true);
        s.setMediaPlaybackRequiresUserGesture(false);
        s.setLoadWithOverviewMode(true);
        s.setUseWideViewPort(true);

        web.setWebViewClient(new WebViewClient());
        web.setBackgroundColor(0xFF070C14);
        web.addJavascriptInterface(new Bridge(), "AndroidBridge");
        web.loadUrl("file:///android_asset/index.html");
    }

    @Override
    protected void onPause() { super.onPause(); if (web != null) web.onPause(); }

    @Override
    protected void onResume() { super.onResume(); if (web != null) web.onResume(); }

    @Override
    public void onBackPressed() {
        if (web != null && web.canGoBack()) { web.goBack(); } else { super.onBackPressed(); }
    }

    public class Bridge {

        @JavascriptInterface
        public void vibrate(int ms) {
            try {
                Vibrator v;
                if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.S) {
                    VibratorManager vm = (VibratorManager) getSystemService(VIBRATOR_MANAGER_SERVICE);
                    v = vm.getDefaultVibrator();
                } else {
                    v = (Vibrator) getSystemService(VIBRATOR_SERVICE);
                }
                if (v == null || !v.hasVibrator()) { return; }
                if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
                    v.vibrate(VibrationEffect.createOneShot(ms, VibrationEffect.DEFAULT_AMPLITUDE));
                } else {
                    v.vibrate(ms);
                }
            } catch (Throwable ignored) { }
        }

        @JavascriptInterface
        public void keepScreenOn(final boolean on) {
            runOnUiThread(new Runnable() {
                public void run() {
                    if (on) {
                        getWindow().addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON);
                    } else {
                        getWindow().clearFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON);
                    }
                }
            });
        }

        @JavascriptInterface
        public void toast(final String msg) {
            runOnUiThread(new Runnable() {
                public void run() {
                    Toast.makeText(MainActivity.this, msg, Toast.LENGTH_SHORT).show();
                }
            });
        }
    }
}
"""
open(os.path.join(AND, "src", PKG, "MainActivity.java"), "w", encoding="utf-8").write(java)

# ---------- 4. 工具链 ----------
sh("aapt2 link", [os.path.join(BT, "aapt2"), "link",
    "-o", os.path.join(AND, "base.apk"),
    "-I", PLAT,
    "--manifest", os.path.join(AND, "AndroidManifest.xml"),
    "-A", os.path.join(AND, "assets"),
    "--min-sdk-version", "26", "--target-sdk-version", "34",
    "--version-code", "1", "--version-name", "1.0"])

sh("javac", ["javac", "-source", "8", "-target", "8", "-nowarn",
    "-cp", PLAT,
    "-d", os.path.join(AND, "classes"),
    os.path.join(AND, "src", PKG, "MainActivity.java")])

sh("d8", [os.path.join(BT, "d8"), "--release", "--min-api", "26", "--lib", PLAT,
    "--output", os.path.join(AND, "dexout"),
    os.path.join(AND, "classes", PKG, "MainActivity.class")])

with zipfile.ZipFile(os.path.join(AND, "base.apk"), "a", zipfile.ZIP_STORED) as z:
    z.write(os.path.join(AND, "dexout", "classes.dex"), "classes.dex")
print("classes.dex 已注入 base.apk")

sh("zipalign", [os.path.join(BT, "zipalign"), "-f", "-p", "4",
    os.path.join(AND, "base.apk"), os.path.join(AND, "base-aligned.apk")])

ks = os.path.expanduser("~/.android/debug.keystore")
sh("apksigner sign", [os.path.join(BT, "apksigner"), "sign",
    "--ks", ks, "--ks-pass", "pass:android", "--key-pass", "pass:android",
    "--ks-key-alias", "androiddebugkey",
    "--out", OUT, os.path.join(AND, "base-aligned.apk")])

sh("apksigner verify", [os.path.join(BT, "apksigner"), "verify", "--print-certs", OUT])

print("\n>>> APK OK: " + OUT)
print(">>> size = " + str(os.path.getsize(OUT)) + " bytes")
```

跑法（一条命令）：
```
python3 build_apk.py
```

装到手机（手机开 USB 调试后）：
```
~/Library/Android/sdk/platform-tools/adb install -r Breathe-v1-debug.apk
```

## 这一版做到什么程度

**已经能用**：
- 4 门课的课程卡片、相位引擎、方形轨道/圆环两种动效、阶段提示与倒计时、三通道（视觉/音频/触觉）、倍速档、结束页 —— 全部来自模板，原样复用。
- 振动走 `Vibrator`（Android 12\+ 用 `VibratorManager`）；跟练期间屏幕常亮走 `FLAG_KEEP_SCREEN_ON`；`alert` 被桥接到原生 Toast。
- 音频：`setMediaPlaybackRequiresUserGesture(false)` 已开，WebAudio 相位提示音可直接响，不受"必须先点一下"限制。

**故意留到 v2 的**（不要在第一版就塞）：
1. **锁屏继续 / 前台服务**：跑长课程时想息屏继续，需要 `ForegroundService` \+ `MediaSession`。这是安卓相对小程序最大的红利，但要做服务生命周期，建议单独一个迭代。
2. **BLE 踏频**：`BluetoothLeScanner` \+ 踏频服务 `0x1816`，要处理 Android 12\+ 的 `BLUETOOTH_SCAN / BLUETOOTH_CONNECT` 运行时权限。当前 F 原型用手动 rpm（L2 档）已经能用。
3. **每晚定时提醒**：`AlarmManager` \+ 通知渠道（API 26\+）\+ `POST_NOTIFICATIONS`（API 33\+）运行时权限。
4. **图标**：这一版没做图标资源（省掉 res/ 目录，链路更短），用的是系统默认图标。要换图标就加 `res/mipmap-anydpi-v26/ic_launcher.xml` 自适应图标（纯 XML，不需要 PNG）。
5. **签名**：现在是 `~/.android/debug.keystore` 调试签名，自用足够；要长期用就自建 keystore 并妥善备份（丢了就装不上更新版）。

## 技术选型的取舍记录

| 方案 | 结论 |
|------|------|
| Kotlin \+ Jetpack Compose 原生 | **不选**。相位引擎/canvas 要重写，工期数倍，而我们已经有跑通的 HTML 引擎 |
| Gradle \+ AGP | **不选**。本机无全局 gradle；AGP 首次依赖下载不可控。手工 aapt2/d8 链路秒级出包 |
| Capacitor / Cordova 套壳 | **不选**。为了一个 WebView 壳引入整条 Node 工具链，收益为零 |
| **WebView 壳 \+ 原生桥（采用）** | 复用引擎，原生只补 Web 拿不到的能力，后续 BLE/前台服务按同一模式增量加 |

这条路线还有个隐性好处：**同一份** `**index.html**` **既是安卓 App 的界面，也是浏览器里可预览的原型，也仍然是微信小程序版本的基础** —— 三个平台共用一套内容资产，而不是三套。
