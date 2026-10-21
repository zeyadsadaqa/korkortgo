"""Hash every accepted artwork binding, font and licence in a newly built target."""
import argparse,hashlib,json,zipfile
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--package',type=Path,required=True);p.add_argument('--prefix',default='composeResources/se.korkort.resources/');p.add_argument('--output',type=Path,required=True);p.add_argument('--label',required=True);a=p.parse_args()
R=Path(__file__).resolve().parents[5];c=json.loads((R/'content/curriculum.json').read_text());base=R/'composeApp/src/commonMain/composeResources'
sha=lambda b:hashlib.sha256(b).hexdigest();z=zipfile.ZipFile(a.package) if a.package.is_file() else None
rows=[]
inputs=[(x['id'],x['bundled']['path'].removeprefix('composeApp/src/commonMain/composeResources/'),x['bundled']['sha256'],'artwork') for x in c['assets']]
inputs += [(p.name,str(p.relative_to(base)),sha(p.read_bytes()),'font' if p.suffix=='.ttf' else 'font_license') for folder in ['font','files/font-licenses'] for p in sorted((base/folder).glob('*')) if p.is_file()]
for ident,suffix,expected,kind in inputs:
 name=a.prefix+suffix
 try:data=z.read(name) if z else (a.package/name).read_bytes();actual=sha(data);error=None
 except (OSError,KeyError) as e:actual=None;error=str(e)
 rows.append({'id':ident,'kind':kind,'entry':name,'expected_sha256':expected,'actual_sha256':actual,'pass':actual==expected,'error':error})
result={'label':a.label,'package_path':str(a.package),'package_sha256':sha(a.package.read_bytes()) if z else None,'identity':json.loads((R/'content/accepted-content-manifest.json').read_text())['identity'],'artwork_bindings':sum(x['kind']=='artwork' for x in rows),'distinct_artwork_files':len({x['entry'] for x in rows if x['kind']=='artwork'}),'fonts':sum(x['kind']=='font' for x in rows),'font_licenses':sum(x['kind']=='font_license' for x in rows),'status':'pass' if all(x['pass'] for x in rows) else 'fail','checks':rows,'scope':'Fresh packaged byte parity only; not visual legibility, native accessibility or external-source currency.'}
a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(result,indent=2)+'\n');print(result['label'],result['status'],len(rows),'resource checks');raise SystemExit(0 if result['status']=='pass' else 1)
