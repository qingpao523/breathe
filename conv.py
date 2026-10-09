import re,html
SRC="/Users/qingpao/.dsh/handoffs/breathing-app/followalong-types-v1.md"
OUT="/Users/qingpao/.dsh/handoffs/breathing-app/followalong-types-v1.html"
md=open(SRC,encoding="utf-8").read()
md=re.sub(r"\\([\\\\`*_{}\[\]()#+\-.!])", r"\1", md)
def inline(s):
    s=html.escape(s)
    s=re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s=re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", s)
    s=re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    return s
out=[];tbl=[]
def flush():
    global tbl
    if not tbl: return
    rows=[[c.strip() for c in r.strip("|").split("|")] for r in tbl if not re.match(r"^\|[\s\-:|]+\|$", r)]
    if rows:
        h="".join("<th>"+inline(c)+"</th>" for c in rows[0])
        b="".join("<tr>"+"".join("<td>"+inline(c)+"</td>" for c in r)+"</tr>" for r in rows[1:])
        out.append("<div class=tw><table><thead><tr>"+h+"</tr></thead><tbody>"+b+"</tbody></table></div>")
    tbl=[]
for ln in md.split("\n"):
    s=ln.rstrip()
    if s.strip().startswith("|"):
        tbl.append(s.strip()); continue
    flush()
    if not s.strip(): continue
    if s.startswith("### "): out.append("<h3>"+inline(s[4:])+"</h3>")
    elif s.startswith("## "): out.append("<h2>"+inline(s[3:])+"</h2>")
    elif s.startswith("# "): out.append("<h1>"+inline(s[2:])+"</h1>")
    elif s.strip()=="---": out.append("<hr>")
    elif s.startswith("> "): out.append("<blockquote>"+inline(s[2:])+"</blockquote>")
    elif s.startswith("- "): out.append("<div class=li>"+inline(s[2:])+"</div>")
    elif re.match(r"^\d+\.\s", s): out.append("<div class=li>"+inline(re.sub(r"^\d+\.\s","",s))+"</div>")
    else: out.append("<p>"+inline(s)+"</p>")
flush()
CSS="*{box-sizing:border-box}body{margin:0;background:radial-gradient(1200px 600px at 12% -8%,#2b3f7a 0%,transparent 55%),radial-gradient(900px 500px at 92% 6%,#6d2f6b 0%,transparent 52%),linear-gradient(160deg,#080b16,#101a33 45%,#170f24);color:#e9edf9;-webkit-font-smoothing:antialiased;font-family:-apple-system,BlinkMacSystemFont,system-ui,sans-serif;line-height:1.78}.wrap{max-width:1000px;margin:0 auto;padding:56px 26px 96px}h1{font-size:33px;letter-spacing:.4px;margin:0 0 10px;background:linear-gradient(92deg,#8fd0ff,#c9a6ff 55%,#ffb3d1);-webkit-background-clip:text;background-clip:text;color:transparent}h2{font-size:21px;margin:46px 0 14px;padding-left:14px;border-left:3px solid #7cc4ff;color:#eef4ff}h3{font-size:17px;margin:28px 0 10px;color:#bcd4ff}p{margin:11px 0;color:#d6def2}strong{color:#fff}em{color:#c8b6ff;font-style:normal}code{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;background:rgba(255,255,255,.1);padding:1px 6px;border-radius:6px;font-size:.92em}blockquote{margin:16px 0;padding:16px 20px;border-radius:14px;background:rgba(255,255,255,.07);border:1px solid rgba(255,255,255,.13);border-left:3px solid #ffb3d1;backdrop-filter:blur(14px);color:#f0e9ff}.tw{margin:18px 0;border-radius:16px;overflow:hidden;background:rgba(255,255,255,.055);border:1px solid rgba(255,255,255,.12);backdrop-filter:blur(14px);box-shadow:0 18px 45px rgba(0,0,0,.34)}table{width:100%;border-collapse:collapse;font-size:14.5px}th{text-align:left;padding:12px 14px;background:rgba(124,196,255,.13);color:#dceaff;font-weight:600;border-bottom:1px solid rgba(255,255,255,.14)}td{padding:11px 14px;border-bottom:1px solid rgba(255,255,255,.07);color:#d3dcf0;vertical-align:top}tr:last-child td{border-bottom:0}.li{position:relative;margin:9px 0 9px 20px;padding-left:16px;color:#d6def2}.li:before{content:"";position:absolute;left:0;top:11px;width:6px;height:6px;border-radius:50%;background:linear-gradient(135deg,#8fd0ff,#c9a6ff)}hr{border:0;height:1px;margin:40px 0;background:linear-gradient(90deg,transparent,rgba(255,255,255,.28),transparent)}"
open(OUT,"w",encoding="utf-8").write("<!DOCTYPE html><html lang=zh-CN><head><meta charset=utf-8><meta name=viewport content=\"width=device-width,initial-scale=1\"><title>Breathing Follow-along Types v1</title><style>"+CSS+"</style></head><body><div class=wrap>"+"\n".join(out)+"</div></body></html>")
