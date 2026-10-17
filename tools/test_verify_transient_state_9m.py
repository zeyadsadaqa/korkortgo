import tempfile,unittest
from pathlib import Path
import xml.etree.ElementTree as ET
import verify_transient_state_9m as report

class StateReportTest(unittest.TestCase):
    def reports(self,path,omit=None,failure=False):
        suite=ET.Element('testsuite',failures='0',errors='0')
        names=sorted({name for checks in report.CHECKS.values()for name in checks})
        for name in names:
            if name==omit:continue
            cls,method=name.rsplit('.',1)
            case=ET.SubElement(suite,'testcase',classname=cls,name=method+'[desktop]')
            if failure and name==names[0]:ET.SubElement(case,'failure',message='failed behaviour')
        ET.ElementTree(suite).write(path/'TEST-state.xml')
        return names
    def test_all_contracts_distinguish_candidate_checks_from_final_acceptance(self):
        with tempfile.TemporaryDirectory()as folder:
            path=Path(folder);self.reports(path);result=report.generate(path)
            self.assertEqual(22,len(result['contracts']))
            self.assertEqual(4,sum(r['status']=='conditional_future_scope'for r in result['contracts']))
            self.assertFalse(result['candidate']['production_start_allowed'])
            self.assertEqual(616,result['candidate']['held'])
            self.assertIn('awaiting final release verification',result['status'])
    def test_missing_required_case_cannot_be_reported_as_passed(self):
        with tempfile.TemporaryDirectory()as folder:
            path=Path(folder);names=self.reports(path);self.reports(path,omit=names[0])
            with self.assertRaises(AssertionError):report.generate(path)
    def test_failed_case_is_rejected_even_if_suite_totals_are_wrong(self):
        with tempfile.TemporaryDirectory()as folder:
            path=Path(folder);self.reports(path,failure=True)
            with self.assertRaises(AssertionError):report.generate(path)
if __name__=='__main__':unittest.main()
