"""Verify imported compatibility records against frozen 7E and exact approved assets."""
import hashlib
import unittest
from pathlib import Path
from build_navigation import ROOT,BASE,read,aliases,legacy_sources,generate

class NavigationImportTest(unittest.TestCase):
    def test_exact_alias_counts_and_no_production_retirement(self):
        a=aliases();self.assertEqual([],a['tombstones'])
        counts={kind:sum(r['lookup']['type']==kind for r in a['aliases']) for kind in ['question','chapter','page','topic','sign']}
        self.assertEqual({'question':1000,'chapter':39,'page':361,'topic':178,'sign':343},counts)
        self.assertEqual(1921,len({str(r['lookup']) for r in a['aliases']}))
    def test_alias_targets_are_exact_frozen_records(self):
        m=read(BASE);a=aliases()['aliases'];position=0
        for key in ['question_routes','chapter_aliases','legacy_page_aliases','unused_topic_routes','sign_routes']:
            for row in m[key]:
                item=a[position];position+=1;outcome=item['outcome']
                expected=row.get('target_ids',[row['target_id']] if row.get('target_id') else [])
                actual=[outcome['target']['content_id']] if outcome['type']=='content' else [t['content_id'] for t in outcome['targets']] if outcome['type']=='chooser' else []
                self.assertEqual(expected,actual)
    def test_missing_sign_urls_are_separate_retained_compatibility_evidence(self):
        m=read(BASE);extra=legacy_sources();a=aliases()['aliases'];self.assertEqual(3,len(extra['references']))
        self.assertEqual([],extra['destinations'])
        for gap,reference in zip(m['unresolved_destinations'],extra['references']):
            self.assertEqual(gap['legacy_external_url'],reference['url'])
            self.assertEqual('REF-'+hashlib.sha256(reference['url'].encode()).hexdigest()[:16],reference['id'])
            alias=next(r for r in a if r['lookup'].get('code')==gap['legacy_code'])
            self.assertEqual('unavailable',alias['outcome']['type']);self.assertEqual(reference['id'],alias['outcome']['official_reference_id'])
            self.assertTrue(all(v is None for v in reference['evidence'][0]['dates'].values()))
    def test_all_400_sign_bindings_reuse_exact_official_bytes(self):
        curriculum=read(Path('content/curriculum.json'));assets={a['id']:a for a in curriculum['assets']}
        self.assertEqual(400,len(curriculum['sign_entries']))
        for sign in curriculum['sign_entries']:
            a=assets[sign['asset_id']]
            self.assertEqual(a['original']['sha256'],a['bundled']['sha256'])
            self.assertEqual(a['bundled']['sha256'],hashlib.sha256((ROOT/a['bundled']['path']).read_bytes()).hexdigest())
    def test_generation_is_byte_exact_and_scoped(self):
        files=generate()
        for path,content in files.items():self.assertEqual(content,(ROOT/path).read_text(),path)
        self.assertEqual({'content/legacy-aliases.json','content/legacy-sources.json'},{str(p) for p in files if p.suffix=='.json'})
    def test_all_legacy_page_assignments_and_sources_share_guard(self):
        text=(ROOT/'composeApp/src/commonMain/kotlin/se/korkort/App.kt').read_text()
        self.assertNotRegex(text,r'page\s*=\s*Page\.')
        self.assertIn('QuizNavigationGuard.exitDecision',text)
        self.assertIn('LocalOpenSource provides ::openSource',text)
        self.assertEqual(1,text.count('uri.openUri(url)'))
if __name__=='__main__':unittest.main()
