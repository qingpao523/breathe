import os,re
R="/Users/qingpao/.dsh/handoffs/qingpao/breathing-app"
def secs(p):
    t=open(p,encoding="utf-8").read()
    return re.split("\n## ",t)[1:]
v1=secs(R+"/evidence/01-research-v1.md")
v2=secs(R+"/evidence/02-research-v2.md")
h1="# \u547c\u5438\u6280\u6cd5\u8bc1\u636e\u8868\n\n> \u6458\u81ea\u300a\u547c\u5438\u6cd5\u5168\u666f\u8c03\u7814\u300b\u7b2c\u4e09\u7ae0\uff1a\u6bcf\u4e2a\u6280\u6cd5\u7684\u505a\u6cd5\u3001\u8bc1\u636e\u7b49\u7ea7\u4e0e\u5df2\u77e5\u53cd\u8bc1\u3002\n\n## "
open(R+"/evidence/techniques.md","w",encoding="utf-8").write(h1+v1[2])
h2="# 2024-2026 \u65b0\u8bba\u6587\u6e05\u5355\n\n> \u6458\u81ea\u300a\u547c\u5438\u6cd5\u8c03\u7814 \u00b7 \u7b2c\u4e8c\u7248\u300b\uff1a\u8fd0\u52a8\u65b9\u5411\u4e0e\u653e\u677e\u7761\u7720\u65b9\u5411\u3002\n\n## "
open(R+"/evidence/papers-2024-2026.md","w",encoding="utf-8").write(h2+v2[1]+"\n\n## "+v2[2])
h3="# \u5e02\u9762\u5168\u666f 2026-09\n\n> \u6458\u81ea\u300a\u547c\u5438\u6cd5\u8c03\u7814 \u00b7 \u7b2c\u4e8c\u7248\u300b\u7b2c\u4e00\u7ae0\u3002\n\n## "
open(R+"/evidence/market-2026.md","w",encoding="utf-8").write(h3+v2[0])
print("sections",len(v1),len(v2))
print("bytes",[os.path.getsize(R+"/evidence/"+f) for f in ["techniques.md","papers-2024-2026.md","market-2026.md"]])
