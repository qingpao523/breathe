import pathlib
a=pathlib.Path("p1raw.md").read_text(encoding="utf-8")
i=a.find("import pathlib")
j=a.find(chr(96)*3,i)
s=a[i:j]
bs=chr(92)
for c in "()[]*_#+-."+chr(96):
    s=s.replace(bs+c,c)
pathlib.Path("p1.py").write_text(s,encoding="utf-8")
print("script",len(s))
