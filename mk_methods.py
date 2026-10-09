import os,json
D="/Users/qingpao/.dsh/handoffs/qingpao/breathing-app/methods/builtin"
os.makedirs(D,exist_ok=True)
box={"id":"box-4-4-4-4","name":"\u76d2\u5f0f\u547c\u5438 4-4-4-4","phases":[{"k":"inhale","s":4},{"k":"hold","s":4},{"k":"exhale","s":4},{"k":"hold2","s":4}],"cycles":6,"mode":"timed","geometry":"square","meta":{"scene":["\u51cf\u538b","\u4e13\u6ce8","\u8fd0\u52a8"],"source":"\u5185\u7f6e","safety":"low","evidence":{"level":"\u2605\u2605","note":"\u8868\u73b0\u578b\u8bc1\u636e\uff1b\u751f\u7406\u53cd\u5e94\u6df7\u5408","ref":"Dujawara et al., Appl Psychophysiol Biofeedback 2026, 8 RCT review"}}}
coh={"id":"coherent-5-5","name":"\u5171\u632f\u6162\u547c\u5438 5.5","phases":[{"k":"inhale","s":5.5},{"k":"exhale","s":5.5}],"cycles":10,"mode":"timed","geometry":"wave","meta":{"scene":["\u7761\u7720","\u6062\u590d"],"source":"\u5185\u7f6e","safety":"none","evidence":{"level":"\u2605\u2605\u2605","note":"\u8ff7\u8d70\u6fc0\u6d3b\u4e0e HRV\uff0c\u8bc1\u636e\u6700\u5f3a\u7684\u6062\u590d\u624b\u6bb5","ref":"\u591a\u9879 RCT / \u5143\u5206\u6790 (6 \u6b21/\u5206)"}}}
sigh={"id":"physiological-sigh","name":"\u751f\u7406\u6027\u53f9\u606f","phases":[{"k":"inhale","s":2},{"k":"inhale2","s":1},{"k":"exhale","s":6}],"cycles":5,"mode":"timed","geometry":"ring","meta":{"scene":["\u51cf\u538b"],"source":"\u5185\u7f6e","safety":"none","evidence":{"level":"\u2605\u2605","note":"\u53cc\u6bb5\u5438\u6c14\uff0c\u6700\u5feb\u89c1\u6548\u7684\u6025\u6027\u51cf\u538b","ref":"Stanford 108 \u4eba\u5b9e\u9a8c"}}}
for k,v in [("box-4-4-4-4",box),("coherent-5-5",coh),("physiological-sigh",sigh)]:
    open(os.path.join(D,k+".json"),"w",encoding="utf-8").write(json.dumps(v,ensure_ascii=False,indent=2))
print("written",len(os.listdir(D)))
