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
