"""Collect exact XCTest attachment names without losing decimal font scales."""
import argparse
import json
import re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'docs/curriculum/app-migration/implementation-evidence/closure-9j-9m-9l14'

def collect(exports,partial=False,keep_zoom=False):
    destination=BASE/'ios';destination.mkdir(parents=True,exist_ok=True)
    mapping=[];matrices={}
    for folder in exports:
        for test in json.loads((folder/'manifest.json').read_text()):
            for attachment in test['attachments']:
                original=attachment['suggestedHumanReadableName']
                name=re.sub(r'_0_[0-9A-Fa-f]{8}(?:-[0-9A-Fa-f]{4}){3}-[0-9A-Fa-f]{12}','',original)
                source=folder/attachment['exportedFileName']
                if not name.endswith(source.suffix):name+=source.suffix
                if name.startswith('question-sign-') and (keep_zoom or '-inline' in name):
                    assert not attachment['isAssociatedWithFailure'],name
                    # Decimal suffixes may follow the exporter's inserted UUID.
                    suffix=source.suffix
                    if not name.endswith(suffix):name+=suffix
                    (destination/name).write_bytes(source.read_bytes())
                    mapping.append({'export':folder.name,'suggested':original,'saved':name,'device_id':attachment['deviceId']})
                match=re.fullmatch(r'question-matrix-0-38-(false|true)-(1(?:\.6)?)-(\d+)\.json',name)
                if match and int(match[3])==37:
                    assert not attachment['isAssociatedWithFailure'],name
                    rows=json.loads(source.read_text())
                    assert len(rows)==38
                    key=(match[1]=='true',float(match[2]))
                    assert key not in matrices,key
                    for row in rows:
                        assert row['dark']==key[0] and float(row['font_scale'])==key[1]
                        assert row['native_selection_confirm']=='passed'
                    matrices[key]=rows
    complete=set(matrices)=={(dark,scale) for dark in [False,True] for scale in [1.0,1.6]}
    assert partial or complete,'Missing passing iOS context'
    rows=[row for key in sorted(matrices) for row in matrices[key]]
    (BASE/('ios-question-matrix-partial.json' if partial else 'ios-question-matrix.json')).write_text(json.dumps({'date':'2026-10-19','complete':complete,'scope':'Actual 38 replacement revisions at four surface/text settings on iOS simulator; not 616 native question recordings.','rows':rows},indent=2)+'\n')
    (BASE/('ios-attachment-map-partial.json' if partial else 'ios-attachment-map.json')).write_text(json.dumps(mapping,indent=2)+'\n')
    print(len(rows),'native iOS question contexts;',len(mapping),'exact attachments')

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--export',type=Path,action='append',required=True)
    parser.add_argument('--partial',action='store_true',help='Collect diagnostic contexts without declaring the acceptance matrix complete.')
    parser.add_argument('--keep-zoom-captures',action='store_true',help='Retain repetitive zoom/return images and trees for temporary debugging; default keeps inline evidence and full matrix assertions.')
    args=parser.parse_args();collect(args.export,args.partial,args.keep_zoom_captures)
