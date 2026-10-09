import os, sys, subprocess, zipfile
ROOT="/Users/qingpao/.dsh/handoffs/qingpao/breathing-app"
SDK=os.path.expanduser("~/Library/Android/sdk")
BT=os.path.join(SDK,"build-tools","34.0.0")
PLAT=os.path.join(SDK,"platforms","android-34","android.jar")
AND=os.path.join(ROOT,"andapp")
PKG="com/qingpao/app"
OUT=os.path.join(ROOT,"Breathe-v2-test.apk")
def sh(n,c):
    p=subprocess.run(c,capture_output=True,text=True)
    o=((p.stdout or "")+(p.stderr or "")).strip()
    if o: print(o[-700:])
    if p.returncode: print("FAIL",n); sys.exit(1)
for d in ["assets","classes","dexout","src/"+PKG]:
    os.makedirs(os.path.join(AND,d),exist_ok=True)
s1="<resources>\n<string name=\"app_name\">\u547c\u5438</string>\n"
s2="<string name=\"app_name2\">\u547c\u5438\u6d4b\u8bd5</string>\n</resources>\n"
open(os.path.join(ROOT,"android","res","values","strings.xml"),"w",encoding="utf-8").write(s1+s2)
open(os.path.join(AND,"assets","index.html"),"w",encoding="utf-8").write(open(os.path.join(ROOT,"android","assets","index.html"),encoding="utf-8").read())
m1="<?xml version=\"1.0\" encoding=\"utf-8\"?>\n<manifest xmlns:android=\"http://schemas.android.com/apk/res/android\" package=\"com.qingpao.app\" android:versionCode=\"2\" android:versionName=\"2.0\">\n"
m2="<uses-sdk android:minSdkVersion=\"26\" android:targetSdkVersion=\"34\"/>\n<uses-permission android:name=\"android.permission.VIBRATE\"/>\n<application android:label=\"@string/app_name2\">\n"
m3="<activity android:name=\".MainActivity\" android:exported=\"true\"><intent-filter><action android:name=\"android.intent.action.MAIN\"/><category android:name=\"android.intent.category.LAUNCHER\"/></intent-filter></activity></application></manifest>\n"
open(os.path.join(AND,"AndroidManifest.xml"),"w",encoding="utf-8").write(m1+m2+m3)
j1="package com.qingpao.app;\nimport android.app.Activity; import android.os.Bundle; import android.widget.TextView;\nimport android.webkit.WebView; import android.webkit.WebSettings; import android.webkit.WebViewClient;\n"
j2="public class MainActivity extends Activity {\n@Override protected void onCreate(Bundle b){ super.onCreate(b);\n try {\n  WebView w=new WebView(this); WebSettings s=w.getSettings();\n  s.setJavaScriptEnabled(true); s.setDomStorageEnabled(true); s.setAllowFileAccess(true);\n  w.setWebViewClient(new WebViewClient());\n  w.loadUrl(\"file:///android_asset/index.html\");\n  setContentView(w);\n } catch (Throwable e) {\n  TextView t=new TextView(this);\n  t.setText(\"WEBVIEW FAILED\\n\"+e.getClass().getName()+\"\\n\"+e.getMessage());\n  setContentView(t);\n }\n}\n}\n"
open(os.path.join(AND,"src",PKG,"MainActivity.java"),"w",encoding="utf-8").write(j1+j2)
sh("res",[os.path.join(BT,"aapt2"),"compile","--dir",os.path.join(ROOT,"android","res"),"-o",os.path.join(AND,"res.zip")])
sh("link",[os.path.join(BT,"aapt2"),"link","-o",os.path.join(AND,"base.apk"),"-I",PLAT,"--manifest",os.path.join(AND,"AndroidManifest.xml"),"-A",os.path.join(AND,"assets"),os.path.join(AND,"res.zip"),"--min-sdk-version","26","--target-sdk-version","34"])
sh("javac",["javac","-source","8","-target","8","-nowarn","-cp",PLAT,"-d",os.path.join(AND,"classes"),os.path.join(AND,"src",PKG,"MainActivity.java")])
sh("d8",[os.path.join(BT,"d8"),"--release","--min-api","26","--lib",PLAT,"--output",os.path.join(AND,"dexout"),os.path.join(AND,"classes",PKG,"MainActivity.class")])
z=zipfile.ZipFile(os.path.join(AND,"base.apk"),"a",zipfile.ZIP_STORED); z.write(os.path.join(AND,"dexout","classes.dex"),"classes.dex"); z.close()
sh("align",[os.path.join(BT,"zipalign"),"-f","4",os.path.join(AND,"base.apk"),os.path.join(AND,"aligned.apk")])
sh("sign",[os.path.join(BT,"apksigner"),"sign","--ks",os.path.expanduser("~/.android/debug.keystore"),"--ks-pass","pass:android","--key-pass","pass:android","--ks-key-alias","androiddebugkey","--out",OUT,os.path.join(AND,"aligned.apk")])
print("APP OK",OUT,os.path.getsize(OUT))
