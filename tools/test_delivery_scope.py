"""Release proof cannot silently omit a target or misrepresent physical iOS evidence."""
import copy
import json
import unittest
from pathlib import Path
from compile_curriculum import ROOT, ContentError, delivery_platforms

class DeliveryScopeTest(unittest.TestCase):
    def test_original_scope_still_requires_physical_ios(self):
        self.assertEqual({'android','desktop','ios_device','ios_simulator','wasm_js'},delivery_platforms())
    def test_explicit_user_scope_requires_all_four_remaining_targets(self):
        policy=json.loads((ROOT/'content/delivery-targets.json').read_text())
        self.assertEqual({'android','desktop','ios_simulator','wasm_js'},delivery_platforms(policy))
        self.assertNotIn('ios_device',delivery_platforms(policy))
    def test_missing_target_unknown_scope_and_unbound_authorization_are_rejected(self):
        policy=json.loads((ROOT/'content/delivery-targets.json').read_text())
        for field,value in [('required_platforms',['android','desktop']),('ios_scope','device'),('authorization','assumed')]:
            with self.subTest(field=field):
                changed=copy.deepcopy(policy);changed[field]=value
                with self.assertRaises(ContentError):delivery_platforms(changed)
        changed=copy.deepcopy(policy);changed['physical_ios_passed']=True
        with self.assertRaises(ContentError):delivery_platforms(changed)

if __name__=='__main__':unittest.main()
