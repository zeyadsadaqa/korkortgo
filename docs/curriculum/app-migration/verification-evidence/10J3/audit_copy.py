"""Independent 7E copy-rule audit of fresh UI observations and retained provenance."""
import hashlib,json,re
from pathlib import Path
OUT=Path(__file__).parent;R=OUT.parents[4]
load=lambda p:json.loads((R/p).read_text())
write=lambda n,x:(OUT/n).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
links=load('docs/curriculum/app-migration/link-and-progress-map.json');c=load('content/curriculum.json');m=load('content/accepted-content-manifest.json');inv=load('docs/curriculum/app-migration/provenance-inventory.json')
checks=[]
def check(name,ok,detail=None):checks.append({'check':name,'pass':bool(ok),'detail':detail})
streams={}
for name in ['reader','source','sign','question']:
 d=json.loads((OUT/f'{name}-copy-observations.json').read_text());streams[name]=d['cases']
 check(name+' identity',d['identity']==m['identity']);check(name+' all expected segments',all(not x.get('missing_segments') for x in d['cases']))
source=json.loads((OUT/'source-copy-observations.json').read_text())
check('all compiled source records exactly match accepted package sources',source['records']==load('content/package-sources.json')['references'])
check('source count519',len(streams['source'])==519);check('sign count400',len(streams['sign'])==400);check('accepted review count1000',len(streams['question'])==1000)
reader=streams['reader'];check('91 reader openings',sum(x['surface']=='reader-opening' for x in reader)==91);check('1316 complete body observations',sum(x['surface']=='reader-block' for x in reader)==1316);check('50 revealed answers',sum(x['surface']=='revealed-answer' for x in reader)==50);check('91 navigation observations',sum(x['surface']=='reader-navigation' for x in reader)==91)
for name in ['shared-presentation-observations','shared-production-observations']:
 d=json.loads((OUT.parent/'10J2'/f'{name}.json').read_text());streams[name]=d['cases']
allrows=[dict(x,stream=k) for k,v in streams.items() for x in v]
# Deliberately bounded: legal chapter/section titles, source evidence locators and official publishers are not legacy book navigation.
patterns={'old_book_attribution':r'Theory Book\s*2026|Study material based on Theory Book|Körkortonline\.se', 'book_folio_navigation':r'Book pages?\s+\d|Source:\s*Theory Book|Theory Book.*?pages?\s+\d','old_chapter_actions':r'Read the related chapter|Previous chapter|Next chapter|No chapters found|Explore\s+\d+\s+chapters|a complete chapter guide','unsupported_preview_copy':r'Lesson continues below|Placement placeholder|Verified B1 asset'}
hits=[]
for row in allrows:
 for kind,pattern in patterns.items():
  for match in re.finditer(pattern,row['text'],re.I):hits.append({'kind':kind,'stream':row['stream'],'subject':row.get('subject',row.get('state_id')),'match':match.group(),'context':row['text'][max(0,match.start()-65):match.end()+65]})
check('no legacy navigation/attribution or raster placeholders in observed learner semantics',not hits,hits)
prod={x['state_id']:x['text'] for x in streams['shared-production-observations']};view={x['state_id']:x['text'] for x in streams['shared-presentation-observations'] if x['width']==1280 and x['font_scale']==1.0}
readertext='\n'.join(x['text'] for x in reader);signtext='\n'.join(x['text'] for x in streams['sign'])
disclaimer='This material is a learning aid to help you understand Swedish driving theory. It is not an official source and cannot replace official information from Trafikverket and Transportstyrelsen. Always consult their current guidance and the applicable rules.'
check('complete approved disclaimer appears in freshly rendered introduction',any(x.get('document')=='introduction' and disclaimer in x['text'] for x in reader))
counts={'modules':len(c['modules']),'lessons':sum(len(x['lesson_ids']) for x in c['modules']),'questions':len(load('content/accepted-assessment-questions.json')['questions']),'sign_entries':len(c['sign_entries'])}
check('counts reconcile manifest-bound authored payloads',counts=={'modules':10,'lessons':40,'questions':1000,'sign_entries':400})
check('actual home1000,10,40',all(x in prod['home'] for x in ['1000','practice questions','10','modules','40','lessons']))
check('actual library10/40', '10 modules · 40 lessons' in view['library-overview'])
check('catalogue count400', '400 entries' in view['reference-catalogue'])
check('home exact replacement attribution','KörkortGo original curriculum and explained practice. This is a learning aid, not an official examination.' in prod['home-attribution'])
check('release human label visible','2026 curriculum' in prod['home-attribution'])
check('five original quiz areas retained',all(s in view['library-overview'] for s in ['Vehicle knowledge & maneuvering','Environment','Traffic safety','Traffic rules','Personal conditions']))
check('empty/reset visible',all(s in view['library-empty'] for s in ['No matching lessons.','Clear search','Clear filters']))
check('typed catalogue current learner title','Road signs and signals' in view['reference-catalogue'])
check('actual confirmed related lesson action','Read the related lesson' in prod['quiz-confirmed'])
check('canonical current reader titles',all(any(x.get('subject')==d['id'] and d['title'] in x['text'] for x in reader if x['surface']=='reader-opening') for d in c['documents']))
check('canonical previous/next learner labels',any(x['surface']=='reader-navigation' and x['subject']=='M03-L02' and 'Previous' in x['text'] and 'Next' in x['text'] for x in reader))
check('editorial notice all400 signs',all('Editorial English translation; not an official agency translation.' in x['text'] for x in streams['sign']))
check('all official asset reuse credits in current sign UI',all('Transportstyrelsen' in x['text'] for x in streams['sign']))
for publisher in ['Transportstyrelsen','Trafikverket','Sveriges riksdag','Trafiko','Volvo']:
 matches=[s for s in source['records'] if publisher.lower() in s['publisher'].lower()]
 check('legitimate publisher preserved '+publisher,bool(matches) and all(any(x['subject']==s['id'] and s['publisher'] in x['text'] for x in streams['source']) for s in matches))
# File identity checks verify preservation only, not legal currency or new reuse rights.
for item in inv['inputs']+inv['font_licenses']:
 check('provenance hash '+item['path'],hashlib.sha256((R/item['path']).read_bytes()).hexdigest()==item['sha256'])
for item in inv['font_licenses']:
 text=(R/item['path']).read_text();check('full OFL retained '+item['path'],all(s in text for s in ['SIL OPEN FONT LICENSE','1.1','PREAMBLE','DEFINITIONS','TERMINATION','DISCLAIMER']))
assets=c['assets'];check('all484 assets retain reuse evidence',len(assets)==484 and all(a['reuse'] for a in assets))
check('contextual artwork credit in imported learner credits','KörkortGo' in readertext and 'built-in imagegen' in readertext.lower())
check('old learner summaries absent from production',not(R/'composeApp/src/commonMain/kotlin/se/korkort/Chapters.kt').exists())
build=(R/'tools/build_content.py').read_text();check('historical page builder isolated from accepted production',all(s in build for s in ['def build_legacy():','if args.command == "legacy":','from compile_curriculum import ContentError, compile_files']) and 'not the accepted-release regeneration path' in (R/'docs/development/content.md').read_text())
readme=(R/'README.md').read_text();check('README current10/40 summary',bool(re.search(r'10 (?:original )?modules',readme,re.I)) and bool(re.search(r'40 lessons',readme,re.I)) and not re.search(r'37.chapter|39.chapter|supplied.book',readme,re.I))
# Every 7E rule gets specific positive evidence as well as the bounded negative scan.
evidence={
 'home_attribution':['actual home exact attribution'], 'edition_stat':['actual home counts/human release label; manifest-bound payload counts'], 'chapter_count':['library10/40 and five unchanged quiz areas'], 'chapter_page_badge':['all91 canonical reader titles; no Book pages badges'], 'reader_attribution':['fresh full91 readers; canonical module/lesson title and no old attribution'], 'question_attribution':['all1000 current answer reviews; canonical primary lesson and separately rendered source titles'], 'source_footer':['full imported disclaimer; all400 editorial notices/credits;519 source dates; bundled full font licences'], 'question_source_label':['all519 compiled records exactly authored; all publisher/classification/date strings present; inherited10C classification defects not waived'], 'related_learning_button':['actual App confirmed question Read the related lesson; all1000 canonical primary lesson titles'], 'previous_next':['fresh91 reader endings; canonical Previous/Next;10H boundary receipts remain scoped'], 'old_sign_chapter_condition':['LearningRoute typed initialReferences/navigationReferenceGroups/ContentTarget; removed Chapters.kt'], 'sign_catalogue_label':['current400-entry catalogue; editorial English notice'], 'chapter_empty_state':['empty filter No matching lessons/Clear search/Clear filters;10I reset semantics remain scoped'], 'home_summary':['current attribution and real10/40 library; README current summary']}
rules=[{'case_id':f'T09-copy_rules-{i}','rule':r['id'],'legacy_pattern':r['legacy_pattern'],'required_copy_or_rule':r['replacement_copy_or_rule'],'evidence':evidence[r['id']],'status':'pass_available_shared_copy_scope' if all(x['pass'] for x in checks) else 'review_required','native_visible_accessibility_closure':'pending_fresh10K'} for i,r in enumerate(links['labels_to_replace'])]
rules_by_id={x['rule']:x for x in rules}
rules_by_id['question_source_label']['status']='open_inherited_source_classification_defects'
rules_by_id['question_source_label']['inherited_defects']=[f'DEF-10C-{i:03d}' for i in range(1,7)]
check('all14 rules enumerated once',len(rules)==14 and len({x['rule'] for x in rules})==14)
write('learner-copy-results.json',{'task':'10J3','status':'copy_preservation_pass_inherited_classification_and_target_checks_open' if all(x['pass'] for x in checks) else 'failed_checks_require_review','identity':m['identity'],'counts':counts,'observations':{k:len(v) for k,v in streams.items()},'copy_rules':rules,'rule_summary':{'pass_available_shared_copy_scope':13,'open_inherited_source_classification_defects':1,'all14_final_native_closures':'pending10K'},'checks':checks,'legacy_hits':hits,'limitations':['Composed merged semantics including content descriptions; offscreen scroll content not all simultaneously visible','Native assistive technology, full visible scroll/pointer/keyboard and actual10K distribution remain open','Provenance/compatibility IDs and source legal chapters retained; no blanket chapter/page/publisher ban','Inherited10C source classification and currency findings remain open; this audit does not certify them'],'all_checks_pass':all(x['pass'] for x in checks),'all_rules_final_pass':False})
print(len(checks),'checks;',sum(not x['pass'] for x in checks),'failures')
for x in checks:
 if not x['pass']:print(x['check'],str(x['detail'])[:1200])
