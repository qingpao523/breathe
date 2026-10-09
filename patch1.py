import os,pathlib
AND="/Users/qingpao/.dsh/handoffs/qingpao/breathing-app/android"
os.makedirs(AND+"/res/values",exist_ok=True)
open(AND+"/res/values/strings.xml","w",encoding="utf-8").write("<resources>\n  <string name=\"app_name\">\u547c\u5438</string>\n</resources>\n")
p=pathlib.Path("/Users/qingpao/.dsh/handoffs/qingpao/breathing-app/build_apk.py")
t=p.read_text(encoding="utf-8")
t=t.replace("android:label=\"\u547c\u5438\"","android:label=\"@string/app_name\"")
t=t.replace("\"-A\", os.path.join(AND, \"assets\"),","\"-A\", os.path.join(AND, \"assets\"), \"-R\", os.path.join(AND, \"res.zip\"),")
t=t.replace("sh(\"aapt2 link\"","sh(\"aapt2 compile\", [os.path.join(BT, \"aapt2\"), \"compile\", \"--dir\", os.path.join(AND, \"res\"), \"-o\", os.path.join(AND, \"res.zip\")])\nsh(\"aapt2 link\"")
p.write_text(t,encoding="utf-8")
print("label", "@string/app_name" in t, "R", "\"-R\"" in t, "compile", "aapt2 compile" in t)
