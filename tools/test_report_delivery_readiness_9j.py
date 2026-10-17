import copy,json,tempfile,unittest
from pathlib import Path
import report_delivery_readiness_9j as report

class DeliveryReadinessTest(unittest.TestCase):
    def proof(self):
        identity=report.read(report.ROOT/'content/content-manifest.json')['identity']
        questions=report.read(report.ROOT/'content/assessment-questions.json')['questions']
        rows=[]
        for q in questions:
            if q['acceptance']['eligibility']!='held':continue
            count=sum(image is not None for image in [q['image']]+[o['image'] for o in q['options']])
            for dark in [False,True]:
                for scale in [1.0,1.6]:rows.append(dict(question_id=q['key']['question_id'],revision=q['key']['revision'],dark=dark,font_scale=scale,image_occurrences=count,zoom_returns=count))
        return dict(package=f"ContentPackageIdentity(contentVersion={identity['content_version']}, manifestSha256=Sha256(value={identity['manifest_sha256']}))",rows=rows)
    def build(self,value):
        with tempfile.TemporaryDirectory(dir=report.ROOT/'composeApp/build') as folder:
            path=Path(folder)/'delivery.json';path.write_text(json.dumps(value));return report.build(path)
    def test_complete_matrix_never_promotes_questions_or_native_acceptance(self):
        result=self.build(self.proof())
        self.assertEqual(2464,result['totals']['desktop_question_runs'])
        self.assertTrue(all(q['eligibility']=='held' and q['native_reader_acceptance']=='pending' for q in result['questions']))
    def test_missing_or_duplicate_surface_text_row_is_rejected(self):
        proof=self.proof()
        for rows in [proof['rows'][:-1],proof['rows']+[proof['rows'][0]]]:
            with self.assertRaises(AssertionError):self.build(dict(proof,rows=rows))
    def test_wrong_package_or_revision_is_rejected(self):
        proof=self.proof();wrong=copy.deepcopy(proof);wrong['rows'][0]['revision']='another-r2'
        for value in [dict(proof,package='another package'),wrong]:
            with self.assertRaises(AssertionError):self.build(value)
    def test_unchecked_image_occurrence_is_rejected(self):
        proof=self.proof();proof['rows'][0]['zoom_returns']=0
        with self.assertRaises(AssertionError):self.build(proof)
if __name__=='__main__':unittest.main()
