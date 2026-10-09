import os, glob, shutil
R="/Users/qingpao/.dsh/handoffs/qingpao/breathing-app"
for d in ["evidence","methods/builtin","web","docs","archive"]:
    os.makedirs(os.path.join(R,d),exist_ok=True)
M={28722:"evidence/01-research-v1.md",17021:"evidence/02-research-v2.md",68970:"evidence/01-research-v1.html",30661:"evidence/02-research-v2.html",14081:"docs/product-plan-v1.md",33521:"docs/product-plan-v1.html",9063:"docs/followalong-types-v1.md",13725:"docs/followalong-types-v1.html",8495:"docs/app-pages-v1.md",1185:"docs/handoff.md",30907:"archive/v2-ui-source.md",17712:"archive/v1-template-source.md"}
n=0
for f in glob.glob(os.path.join(R,"*")):
    if not os.path.isfile(f): continue
    s=os.path.getsize(f)
    if s in M:
        shutil.move(f,os.path.join(R,M[s])); n+=1; print("moved",M[s])
print("total_moved",n)
