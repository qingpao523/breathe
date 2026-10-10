import pathlib
j = pathlib.Path("render.js").read_text(encoding="utf-8")
for f in ["web/index.html","index.html"]:
    p = pathlib.Path(f); h = p.read_text(encoding="utf-8")
    k = h.rfind("</script>")
    h = h[:k] + j + h[k:]
    h = h.replace("if(E.m.card){ E.si++; return E.list[E.si] ? loadStep() : finish(); }",
                  'if(E.m.card){ alert(E.m.name+" 需要器械，只做方法说明，不计入练习"); return nextStep(); }')
    p.write_text(h, encoding="utf-8")
b = pathlib.Path("build_app.py"); t = b.read_text(encoding="utf-8")
b.write_text(t.replace("呼吸测试","呼吸"), encoding="utf-8")
print("patched")
