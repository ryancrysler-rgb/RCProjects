# Parses the Golf Blueprint practice-plan PDFs into plans.json (run with -I: python3 -I parse.py <pdf dir>)
import json, os, sys, pdfplumber
BLUE=(0.184314,0.47451,0.752941)
def isblue(c): return c is not None and len(c)==3 and all(abs(a-b)<.02 for a,b in zip(c,BLUE))
def lines(ws):
    rows={}
    for w in ws: rows.setdefault(round(w['top']/3),[]).append(w)
    out=[]
    for k in sorted(rows):
        r=sorted(rows[k],key=lambda w:w['x0']); out.append((r[0]['top'],r[0]['x0'],' '.join(w['text'] for w in r)))
    return out
def paras(ls):
    ps=[];cur=[];last=None
    for top,x,t in ls:
        if t.strip() in ('.',''): continue
        if last is not None and top-last>24 and cur: ps.append(' '.join(cur)); cur=[]
        cur.append(t); last=top
    if cur: ps.append(' '.join(cur))
    return ps
def parse(fn):
    pdf=pdfplumber.open(fn); plan={'intro':None,'sessions':[],'cards':[]}
    for pg in pdf.pages:
        ws=pg.extract_words(extra_attrs=['non_stroking_color','size'])
        txt=' '.join(w['text'] for w in ws)
        if 'PRESCRIPTION' in txt:
            if plan['sessions']: continue
            left=[w for w in ws if w['x0']<300 and w['top']<330 and w['size']<20 and not isblue(w['non_stroking_color']) or (w['x0']<300 and w['top']<330 and w['size']<16)]
            intro=' '.join(t for _,_,t in lines([w for w in ws if w['x0']<300 and w['top']<330 and w['size']<16]))
            plan['intro']=intro.replace(' .','').strip()
            heads=[w for w in ws if w['text']=='SESSION']
            for h in sorted(heads,key=lambda w:w['top']):
                n=[w for w in ws if abs(w['top']-h['top'])<3 and w['x0']>h['x0'] and w['x0']<h['x0']+140]
                num=next((w['text'] for w in n if w['text'].isdigit()),'?')
                mins=next((w['text'] for w in ws if w['text'].startswith('(') and abs(w['top']-h['top']-22)<18 and w['x0']<330),'')
                plan['sessions'].append({'n':num,'mins':(mins+' '+next((w['text'] for w in ws if w['text'].startswith('min') and abs(w['top']-h['top']-22)<18),'')).strip(),'top':h['top']})
            items=[(t,x,s) for t,x,s in lines([w for w in ws if w['x0']>320]) ]
            its=[(t,s2) for t,x,s2 in items if s2.strip() not in ('.','') and 'BLUEPRINT' not in s2 and 'PRESCRIPTION' not in s2]
            groups=[];last=None
            for t,s2 in its:
                if last is None or t-last>22: groups.append([])
                groups[-1].append(s2); last=t
            for i,sess in enumerate(plan['sessions']):
                sess['n']=str(i+1); sess['cards']=groups[i] if i<len(groups) else []; del sess['top']
            continue
        if 'Skillset:' not in txt: continue
        im=pg.to_image(resolution=72).original.convert('RGB')
        def dark(w):
            b=im.crop((int(w['x0']),int(w['top']),int(w['x1'])+1,int(w['bottom'])+1)); return min(sum(c) for c in b.get_flattened_data() if True)<500
        big=[w for w in ws if w['size']>28]; title=' '.join(w['text'] for w in sorted(big,key=lambda w:w['x0']))
        def field(label_words, xmin, xmax, top):
            vals=[w['text'] for w in ws if abs(w['top']-top)<3 and xmin<=w['x0']<xmax and isblue(w['non_stroking_color']) and dark(w) and w['text'] not in label_words]
            return ' '.join(vals)
        lab={w['text']:w for w in ws if w['text'] in ('Skillset:','Type:','Monitor:','Pressure:','Location:')}
        f={}
        f['Skillset']=field({'Skillset:'},60,330,lab['Skillset:']['top'])
        f['Type']=field({'Type:'},60,330,lab['Type:']['top'])
        f['Launch monitor']=field({'Launch','Monitor:'},60,330,lab['Monitor:']['top'])
        f['Simulate pressure']=field({'Simulate','Pressure:'},330,612,lab['Pressure:']['top'])
        loc=[w for w in ws if isblue(w['non_stroking_color']) and dark(w) and w['x0']>335 and w['text']!='Location:' and w['text'] not in ('Simulate','Pressure:','Yes','No') and lab['Location:']['top']-3<w['top']<lab['Location:']['top']+30 and w['text']!='Location:']
        f['Location']=' '.join(w['text'] for w in sorted(loc,key=lambda w:(round(w['top']),w['x0'])))
        heads={w['text']:w for w in ws if w['size']>20 and w['text'] in ('Description','Advice','Tracking')}
        body=[w for w in ws if w['size']<20 and w['size']>10 and not isblue(w['non_stroking_color'])]
        dtop=heads['Description']['top']; atop=heads['Advice']['top']
        desc=paras(lines([w for w in body if dtop<w['top']<atop-10]))
        adv=paras(lines([w for w in body if w['top']>atop and w['x0']<315]))
        trk=paras(lines([w for w in body if w['top']>atop and w['x0']>=315]))
        plan['cards'].append({'title':title,'fields':f,'description':desc,'advice':adv,'tracking':trk})
    return plan
src=sys.argv[1]; out={}
for name in ['IntentionalPractice','Intentional3','IntentionalFail','Approach','DistanceControl','DrivingSpecificBlueprint','HabitsAndProcess','Process2','ProcessAllAreasBlueprint','ProcessAllAspects','Reflection','Reflection2','Session1']:
    out[name]=parse(os.path.join(src,name+'.pdf'))
json.dump(out,open('plans.json','w'),indent=1,ensure_ascii=False)
for k,v in out.items(): print(k,len(v['sessions']),[len(s['cards']) for s in v['sessions']],len(v['cards']))
