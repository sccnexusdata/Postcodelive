from pathlib import Path
import json, sys
required=['config/localities/lewes.yaml','config/upstreams.json','src/postcodelive/config.py','src/postcodelive/contracts.py','scripts/import_upstreams.py','docs/ARCHITECTURE.md']
missing=[p for p in required if not Path(p).exists()]
if missing:
    print('Missing required infrastructure:',*missing,sep='\n- '); sys.exit(1)
if Path('public_html/data/lewes.bundle.v1.json').exists():
    data=json.loads(Path('public_html/data/lewes.bundle.v1.json').read_text())
    assert data['schema_version']=='1.0'
    assert 'items' in data and 'quality' in data
print('PostcodeLive infrastructure validation passed')
