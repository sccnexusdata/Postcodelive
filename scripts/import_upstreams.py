from __future__ import annotations
import argparse, json, hashlib
from pathlib import Path
from postcodelive.config import LocalityConfig
from postcodelive.quality import quality_report

def load_json(path: Path):
    return json.loads(path.read_text(encoding='utf-8'))

def stable_id(prefix: str, obj: dict) -> str:
    seed = '|'.join(str(obj.get(k,'')) for k in ('id','name','title','postcode','start_date','date','website','url'))
    return f"{prefix}-{hashlib.sha1(seed.encode()).hexdigest()[:12]}"

def provenance_from(obj: dict, fallback: str):
    prov=obj.get('provenance')
    if isinstance(prov,list) and prov: return prov
    src=obj.get('source') or obj.get('source_name') or obj.get('organiser') or fallback
    url=obj.get('source_url') or obj.get('website') or obj.get('url')
    return [{'source':src,'url':url,'confidence':obj.get('confidence','imported')}]

def normalise_directory(obj: dict) -> dict:
    return {k:v for k,v in {'id':obj.get('id') or stable_id('place',obj),'kind':'place','name':obj.get('name') or obj.get('title') or 'Unnamed place','category':obj.get('category') or obj.get('primary_category') or 'Uncategorised','latitude':obj.get('latitude') or obj.get('lat'),'longitude':obj.get('longitude') or obj.get('lng') or obj.get('lon'),'postcode':obj.get('postcode'),'url':obj.get('website') or obj.get('url'),'image_url':obj.get('image_url') or obj.get('image'),'description':obj.get('description') or obj.get('summary'),'provenance':provenance_from(obj,'LocalDirectory')}.items() if v not in (None,'',[])}

def normalise_event(obj: dict) -> dict:
    start=obj.get('start') or obj.get('start_datetime') or obj.get('start_date') or obj.get('date')
    return {k:v for k,v in {'id':obj.get('id') or stable_id('event',obj),'kind':'event','name':obj.get('title') or obj.get('name') or 'Untitled event','category':obj.get('category') or 'Uncategorised','latitude':obj.get('latitude') or obj.get('lat'),'longitude':obj.get('longitude') or obj.get('lng') or obj.get('lon'),'postcode':obj.get('postcode'),'url':obj.get('booking_url') or obj.get('website') or obj.get('url'),'image_url':obj.get('image_url') or obj.get('image'),'start':start,'end':obj.get('end') or obj.get('end_datetime') or obj.get('end_date'),'description':obj.get('description') or obj.get('summary'),'provenance':provenance_from(obj,'LocalEventsEngine')}.items() if v not in (None,'',[])}

def records(payload):
    if isinstance(payload,list): return payload
    if isinstance(payload,dict):
        for key in ('items','events','listings','directory','records','data'):
            if isinstance(payload.get(key),list): return payload[key]
    return []

def first_existing(root:Path, patterns:list[str]):
    for pattern in patterns:
        found=list(root.glob(pattern))
        if found: return found[0]
    return None

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--config',default='config/localities/lewes.yaml')
    p.add_argument('--events-root',required=True); p.add_argument('--directory-root',required=True); p.add_argument('--leweslive-root',required=True)
    p.add_argument('--output',default='public_html/data')
    a=p.parse_args(); cfg=LocalityConfig.load(a.config); out=Path(a.output); out.mkdir(parents=True,exist_ok=True)
    eroot=Path(a.events_root); droot=Path(a.directory_root); lroot=Path(a.leweslive_root)
    ep=first_existing(eroot,['exports/leweslive/events.v1.json','exports/**/events.v1.json','**/events.v1.json'])
    if not ep: ep=first_existing(lroot,['public_html/events/events.v1.json'])
    dp=first_existing(droot,['published/leweslive/directory.v1.json','candidate/leweslive/directory.v1.json','**/directory.v1.json'])
    events=[normalise_event(x) for x in records(load_json(ep))] if ep else []
    directory=[normalise_directory(x) for x in records(load_json(dp))] if dp else []
    items=directory+events
    bundle={'schema_version':'1.0','locality':{'slug':cfg.slug,'display_name':cfg.display_name,'postcode_prefixes':cfg.postcode_prefixes,'centre':{'latitude':cfg.latitude,'longitude':cfg.longitude},'radius_km':cfg.radius_km},'counts':{'places':len(directory),'events':len(events),'total':len(items)},'items':items,'quality':quality_report(items),'sources':{'events_file':str(ep) if ep else None,'directory_file':str(dp) if dp else None}}
    (out/f'{cfg.slug}.bundle.v1.json').write_text(json.dumps(bundle,indent=2,ensure_ascii=False),encoding='utf-8')
    (out/f'{cfg.slug}.events.v1.json').write_text(json.dumps(events,indent=2,ensure_ascii=False),encoding='utf-8')
    (out/f'{cfg.slug}.directory.v1.json').write_text(json.dumps(directory,indent=2,ensure_ascii=False),encoding='utf-8')
    (out/f'{cfg.slug}.quality.v1.json').write_text(json.dumps(bundle['quality'],indent=2),encoding='utf-8')
    print(json.dumps(bundle['counts']))
if __name__=='__main__': main()
