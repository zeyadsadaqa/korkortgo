"""Reproduce the question-to-book audit from reviewed decisions and PDF text.

Run with the bundled Python (pypdf required). This audits the supplied book,
not the legal correctness of the bank. Scenario decisions below are editorial
review findings; sign locations are exact code entries, never topic similarity.
"""
import hashlib
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BOOK = ROOT / 'docs/curriculum/pdf-production/korkortgo-curriculum-review.pdf'
BANK = ROOT / 'content/questions.json'
OUT = ROOT / 'docs/curriculum/question-book-review'

# Question number: supporting PDF pages. Multiple pages are complementary.
COVERED = {
    1:[44],2:[38,89],3:[38,94],4:[38,94],5:[86],6:[86,95],7:[86],
    8:[89,92],9:[89,104],10:[44,46,96],11:[60],12:[130],
    14:[47],15:[47],16:[46],17:[106],18:[106],19:[108],20:[108,112],
    21:[108],22:[114],23:[114,118],24:[114,116,117],25:[146],26:[146,156],
    27:[144],28:[146],29:[146],30:[145],31:[147],32:[151,152],33:[150,156],
    34:[150,156],35:[188,194],36:[190],37:[188],38:[183],39:[73,186],
    40:[196],41:[196,208],42:[134],43:[136],44:[136,138],46:[27,96],
    47:[308],48:[21],49:[308],50:[10,128],51:[11,16,308],52:[196],
    53:[12,16,232],54:[12],55:[10,11],56:[10],57:[8],58:[8],59:[8],
    60:[8,228],61:[8,9],63:[228],64:[228,230],65:[228],66:[8,228],
    67:[228],72:[78],74:[78,228],80:[274],81:[274],
    87:[272,274],89:[274,275],91:[274],93:[260,272],95:[277,279],
    96:[280],97:[285],100:[73,78,308],101:[73,172],102:[101],103:[91],
    108:[73,128,201,209],109:[130],110:[183,186],111:[183],112:[210,216],
    113:[224,226],115:[73,220,221],118:[128,129],120:[128,129],121:[128],
    122:[128,130],123:[301,303],124:[301,303],125:[301],127:[302],128:[294],
    130:[25],133:[25],134:[25,26],137:[78],139:[78,224],140:[225],
    141:[225],142:[225],143:[225],144:[225,274],147:[225],
    151:[260],155:[224,260],160:[251],161:[246],162:[246],163:[243,245,265],
    164:[243,251],166:[251],167:[23,221,222],168:[21,23],169:[21],
    170:[258],171:[258],175:[21,22],176:[258],177:[258,265],178:[258],
}

# Specific missing knowledge, rather than an unsupported topic-only page match.
GAPS = {
    13:'The 50 km/h threshold is taught, but the bus yielding duty above it is not explained.',
    45:'The book refers to prohibited lighting combinations without naming dipped headlights plus front fog lights.',
    62:'Stimulant drugs masking fatigue and producing overconfidence are not explained.',
    68:'Microsleep is not defined.',
    69:'Fatigue and stopping/rest planning are covered, but restorative sleep as the remedy for sleep deprivation is not taught.',
    70:'Central vision and its role in reading fine detail are not explained.',
    71:'Peripheral vision and movement detection are not explained.',
    73:'The single-headlight illusion and the possibility of a wider vehicle with a failed lamp are not taught.',
    75:'Speed adaptation after prolonged high-speed driving and the speedometer check are not taught.',
    76:'The mechanism linking fossil carbon, carbon dioxide and climate change is not explained.',
    77:'Catalytic-converter warm-up and cold-start effectiveness are not taught.',
    78:'The distinction between catalytic pollutant removal and remaining fossil CO2 emissions is not taught.',
    79:'Engine heaters and timer use are not covered.',
    82:'Air-conditioning energy demand and its safe, economical use are not taught.',
    83:'Car washing, wastewater treatment and preferred wash facilities are not covered.',
    84:'Carbon monoxide and its effect on oxygen transport are not explained.',
    85:'Nitrogen oxides, acidification, airway irritation and ground-level ozone are not explained.',
    86:'Wear particles are mentioned, but respiratory health effects are not explained.',
    88:'The high suitable gear principle for a conventional manual car is not taught; vehicle instructions are deferred to.',
    90:'Engine braking in a conventional manual car is not defined.',
    92:'The electric-car distinction between no tailpipe exhaust and production/energy-supply impacts is not taught explicitly.',
    94:'Plug-in hybrids are mentioned, but external charging versus a non-plug-in hybrid is not explained.',
    98:'Local studded-tyre restrictions and wear particles are mentioned separately; the specific studs/road-wear/air-quality link is not taught.',
    99:'Removing roof equipment is taught, but unnecessary carried mass and its energy cost are not explained.',
    104:'Keeping front wheels straight while waiting for a left turn is not taught.',
    105:'The safer country-road left-turn alternative of continuing, turning around and returning for a right turn is not taught.',
    106:'A timed gap is mentioned without the fixed-point counting method or the three-second guideline.',
    107:'Increasing the forward gap to manage a tailgater and avoiding sudden braking are not taught.',
    114:'Bridge cooling from above and below, and earlier freezing, are not explained.',
    116:'Freezing rain forming a nearly invisible ice layer is not explained.',
    117:'First rain after a dry spell mixing with road residues is not explained.',
    119:'Guide dogs and avoiding distraction of a working dog are not covered.',
    126:'Wildlife risks at dusk/dawn, habitats and fence openings are not taught.',
    129:'Vision Zero and its no-death/no-serious-injury goal are not defined.',
    131:'Head-restraint adjustment is mentioned without explaining neck protection or rear-impact head movement.',
    132:'Rear-facing seats are recommended without explaining young children’s head/neck support and crash-force distribution.',
    135:'The general definition of a bicycle as a vehicle is not taught explicitly.',
    136:'The road-speed-limit treatment of a light lorry versus the heavy-lorry cap is not taught.',
    138:'The square-of-speed braking-distance relationship is not taught.',
    145:'Wheel imbalance as a cause of speed-dependent steering vibration is not covered.',
    146:'Temporary spare-wheel use and its speed/distance/pressure limits are not taught.',
    148:'Best-grip tyres are recommended at the rear, but the reason involving rear grip loss and the tail swinging out is not explained.',
    149:'Oversteer and rear-axle loss of grip are not defined.',
    150:'Understeer and front-axle loss of grip are not defined.',
    152:'Aquaplaning and water separating tyre contact from the road are not defined.',
    153:'The aquaplaning response is not taught; generic smooth-input advice does not establish the specific recovery action.',
    154:'Separate brake circuits and retained braking after a circuit failure are not explained.',
    156:'ABS pedal pulsation and maintaining firm pressure during an emergency stop are not taught.',
    157:'A sinking brake pedal and hydraulic leaks/faults are not explained.',
    158:'Air in a hydraulic brake system and a springy/spongy pedal are not explained.',
    159:'Controlled deformation/crumple zones and crash-energy absorption are not explained.',
    165:'Excess towball load unloading the front axle and reducing steering grip is not explained.',
    172:'Inspection intervals are taught, but automatic prohibition following a missed deadline is not stated.',
    173:'Electrical fuses and protection against excessive current are not explained.',
    174:'Hot pressurised coolant and the burn risk from opening its cap are not explained.',
}

# Explicitly identify answers that apply or combine principles rather than repeat text.
APPLICATION = {4,9,10,46,48,49,50,51,52,53,56,60,67,69,74,81,87,93,
               95,97,100,102,103,108,113,115,118,120,121,122,124,127,
    139,144,151,155,175,176,177}

def main():
    from pypdf import PdfReader
    questions = json.loads(BANK.read_text())
    # Always extract the actual PDF, so an edited book cannot silently reuse old text.
    reader = PdfReader(BOOK)
    pages = [p.extract_text() or '' for p in reader.pages]
    assert len(questions) == 1000
    assert len({q['id'] for q in questions}) == 1000
    assert set(COVERED).isdisjoint(GAPS)
    assert set(COVERED) | set(GAPS) == set(range(1,179))
    entries = []
    for position, q in enumerate(questions, 1):
        entry = dict(question_id=q['id'], question_number=position,
                     category=q['category'], prompt=q['prompt'],
                     options=q['options'], correct_option_index=q['correct'],
                     correct_answer=q['options'][q['correct']]['text'],
                     question_explanation=q['explanation'],
                     question_image=q.get('image',''),
                     original_source_page=q.get('page'))
        ident = q['id']
        support = []
        if ident.startswith('situation-'):
            number = int(ident.split('-')[1])
            if number in COVERED:
                refs = COVERED[number]
                status = 'covered'
                basis = 'application_of_book_principles' if number in APPLICATION else 'book_teaches_answer'
                reason = 'The cited lesson text supplies the answer or the principles needed to select it.'
            else:
                refs = []
                status = 'not_covered'
                basis = 'missing_specific_knowledge'
                reason = GAPS[number]
        elif ident.startswith('sign-'):
            code = ident.split('-',2)[2]
            pattern = re.compile(r'(?:^|\n)'+re.escape(code)+r' · ([^\n]+)\n')
            refs = []
            for i,text in enumerate(pages[:470]):
                match = pattern.search(text)
                if match:
                    refs.append(i+1)
                    start = match.start()
                    following = re.search(r'\n[A-Z]+\d+(?:[a-z]|-\d+)? · |\nContents\n',text[match.end():])
                    end = match.end()+following.start() if following else len(text)
                    support.append(dict(pdf_page=i+1, excerpt=' '.join(text[start:end].split())))
            status = 'covered' if refs else 'not_covered'
            basis = 'illustrated_sign_entry' if refs else 'missing_sign_entry'
            reason = (f'The book illustrates and explains {code}; English labels may differ from the bank.'
                      if refs else f'No illustrated or explanatory entry for {code} appears in this PDF. A family overview is insufficient for recognition.')
            entry['sign_code'] = code
        elif ident.startswith(('reaction-','gap-')):
            refs = [78]
            status = 'covered'
            basis = 'application_of_book_calculation'
            reason = 'Apply speed ÷ 3.6 × seconds, using the unit conversion and assumed-delay example on page 78. The same distance/time calculation applies to a timed following gap.'
        elif ident.startswith('disc-'):
            refs = [155]
            status = 'covered'
            basis = 'application_of_book_rule'
            reason = 'Page 155 teaches setting the parking disc to the next half-hour after arrival.'
        elif ident.startswith('load-'):
            refs = [246]
            status = 'covered'
            basis = 'application_of_book_calculation'
            reason = 'Page 246 defines maximum load as total weight minus defined ready weight. Use the figures supplied and do not count the driver twice.'
        elif ident.startswith('stopping-'):
            refs = []
            status = 'prompt_only'
            basis = 'formula_supplied_by_question_not_book'
            reason = 'The question supplies both formulas, so arithmetic can answer it. This PDF does not teach the rough reaction model or the 0.4 braking coefficient; “the book’s rough dry-road model” points to the old book.'
        elif ident.startswith('braking-'):
            refs = []
            status = 'not_covered'
            basis = 'missing_specific_knowledge'
            reason = 'The answer requires the square-of-speed braking-distance relationship. Neither the PDF nor the question prompt supplies this relationship.'
        elif ident.startswith('fuel-'):
            refs = []
            status = 'prompt_only'
            basis = 'ordinary_proportional_arithmetic'
            reason = 'The supplied litres-per-100-km and distance allow distance × rate ÷ 100. The book discusses efficient travel but does not teach this calculation, so no supporting book page is assigned.'
        else:
            raise ValueError(ident)
        for n in refs:
            assert 1 <= n <= len(pages)
        entry.update(status=status, answerable_from_book=status=='covered',
                     basis=basis, rationale=reason, book_pages=refs,
                     primary_book_page=refs[0] if refs else None)
        if support:
            entry['evidence'] = support
        else:
            entry['evidence'] = [dict(pdf_page=n, section=pages[n-1].splitlines()[0],
                page_text=re.sub(r'\nContents\nSources\nPrevious page\n\d+\nNext page\n?$', '',pages[n-1]).strip()) for n in refs]
        entries.append(entry)
    counts = Counter(e['status'] for e in entries)
    metadata = dict(schema_version='1.0',review_date='2026-10-07',
        book_path=str(BOOK.relative_to(ROOT)),book_sha256=hashlib.sha256(BOOK.read_bytes()).hexdigest(),
        questions_path=str(BANK.relative_to(ROOT)),questions_sha256=hashlib.sha256(BANK.read_bytes()).hexdigest(),
        book_page_count=len(pages),page_numbering='One-based PDF page number including cover; matches the visible footer on sampled pages. Not the original question page field.',
        criterion='Can a learner select the bank’s keyed answer from explanations/illustrations in this PDF, with ordinary application and arithmetic? Does not require every distractor explanation to be taught.',
        status_definitions=dict(covered='Book supplies answer or necessary principle/formula.',not_covered='Specific required knowledge or illustration missing.',prompt_only='Solvable from supplied numbers/formulas but not taught by this book.'),
        method='All 1000 records checked. Scenario answers reviewed against full relevant pages; sign pairs matched by exact illustrated code entry across the PDF, excluding the lookup and bibliography; every calculation instance classified by its method. Complete PDF text extracted and searched. Representative visual checks on pages 78 and 327. No external linked sources counted as book coverage. This is a curriculum coverage review, not a legal or medical accuracy audit.',
        totals=dict(total=len(entries),**counts,not_answerable_from_book=counts['not_covered']+counts['prompt_only']))
    OUT.mkdir(parents=True,exist_ok=True)
    def save(name, data):
        (OUT/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
    save('question-page-map.json',dict(metadata=metadata,questions=[e for e in entries if e['status']=='covered']))
    save('question-coverage-gaps.json',dict(metadata=metadata,questions=[e for e in entries if e['status']!='covered']))
    save('all-question-coverage.json',dict(metadata=metadata,questions=entries))
    by_family = Counter()
    for e in entries:
        family = ('sign' if e['question_id'].startswith('sign-') else
                  'situation' if e['question_id'].startswith('situation-') else
                  'fuel-saving' if e['question_id'].startswith('fuel-saving-') else e['question_id'].split('-')[0])
        by_family[(family,e['status'])]+=1
    report = ['# Question coverage review','',
              f'Reviewed all {len(entries)} questions against the supplied {len(pages)}-page curriculum PDF.',
              '',f'- Covered by book study: **{counts["covered"]}**.',
              f'- Missing required knowledge/illustrations: **{counts["not_covered"]}**.',
              f'- Solvable from the question’s numbers/formulas alone, but not taught in the book: **{counts["prompt_only"]}**.',
              f'- Total without adequate book support: **{counts["not_covered"]+counts["prompt_only"]}**.','',
              '| Question family | Covered | Missing knowledge | Prompt-only |','|---|---:|---:|---:|']
    for family in dict.fromkeys(key[0] for key in by_family):
        report.append(f'| {family} | {by_family[(family,"covered")]} | {by_family[(family,"not_covered")]} | {by_family[(family,"prompt_only")]} |')
    report += ['', '## Files', '',
        '- `question-page-map.json`: only supported questions, retaining prompts, options, answers, IDs and exact supporting pages.',
        '- `question-coverage-gaps.json`: every unsupported question, with a specific reason and prompt-only distinctions.',
        '- `all-question-coverage.json`: complete 1,000-record audit in original order.', '',
        'Page numbers are one-based PDF positions, including the cover. The existing `page` in the bank belongs to the original source book and is retained only as `original_source_page`. `book_pages` lists actual support; `primary_book_page` is the first useful lesson page. Sign records also contain extracted entry evidence.', '',
        'A broad chapter on a topic, a bibliography link or a code lookup does not establish answer coverage. Reasonable applications are labelled separately. Some supported questions have more detailed explanations than the PDF; the criterion is selecting the keyed answer, not reproducing every explanation.', '',
        'The audit evaluates this PDF only. It does not verify the law, medical claims, the bank’s answer accuracy or external source content. Representative sign and calculation pages were visually inspected; this is not a visual inspection of every illustration.', '',
        '## Scenario gaps', '', '| ID | Missing teaching |','|---|---|']
    for number,reason in sorted(GAPS.items()):
        report.append(f'| situation-{number:03d} | {reason} |')
    absent = [e['sign_code'] for e in entries if e.get('sign_code') and e['status']=='not_covered' and e['question_id'].startswith('sign-meaning-')]
    report += ['', '## Missing sign entries', '',
               f'{len(absent)} sign codes are absent; each affects both a meaning and a recognition question:', '', ', '.join(absent), '',
               '## Calculation gaps', '',
               'All braking-factor questions need a square-of-speed explanation. All rough stopping-distance questions supply their own formulas but attribute them to a book that does not contain them. Fuel and fuel-saving questions are ordinary proportional arithmetic, with no teaching page in this PDF.', '',
               'Suggested curriculum additions: the missing sign entries; vision, perception and fatigue details; environment and powertrain explanations; vehicle faults and braking/steering behaviour; specific winter-surface mechanisms; selected safety-system and crash-protection explanations; and worked braking, stopping and fuel calculations. The JSON lists each affected question individually.']
    (OUT/'review.md').write_text('\n'.join(report)+'\n')
    print(json.dumps(metadata['totals'],indent=2))
    print('Missing signs:',len(absent))
    for family in dict.fromkeys(key[0] for key in by_family):
        print(family,{s:by_family[(family,s)] for s in ('covered','not_covered','prompt_only')})
    # Validate a disjoint, exhaustive partition and every stored page reference.
    covered=json.loads((OUT/'question-page-map.json').read_text())['questions']
    gaps=json.loads((OUT/'question-coverage-gaps.json').read_text())['questions']
    assert {e['question_id'] for e in covered}.isdisjoint(e['question_id'] for e in gaps)
    assert {e['question_id'] for e in covered+gaps}=={q['id'] for q in questions}
    assert all(e['book_pages'] for e in covered)
    assert all(not e['book_pages'] for e in gaps)
    print('PASS: 1000 unique IDs, exhaustive partition, valid page references.')

if __name__ == '__main__':
    main()
