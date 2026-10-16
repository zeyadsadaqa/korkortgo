"""Focused regressions for final production overlays and shared sign examples."""
import copy
import unittest
from compile_curriculum import Validator,ContentError

class ProductionPayloadTest(unittest.TestCase):
    def setUp(self):
        self.v=Validator()
        self.overlay={'left':10,'top':20,'right':30,'bottom':40,'asset_id':'official/B1','label':[],'inset_pixels':2}
    def check(self):self.v.typed(self.overlay,'IllustrationOverlay','overlay')
    def test_exact_artwork_overlay(self):self.check()
    def test_editable_label_overlay(self):
        self.overlay['asset_id']=None;self.overlay['label']=[{'type':'text','text':'B4'}];self.check()
    def test_missing_overlay_content(self):
        self.overlay['asset_id']=None
        with self.assertRaisesRegex(ContentError,'exactly one'):self.check()
    def test_overlay_cannot_have_both_label_and_art(self):
        self.overlay['label']=[{'type':'text','text':'invented'}]
        with self.assertRaisesRegex(ContentError,'exactly one'):self.check()
    def test_overlay_cannot_invert_rectangle(self):
        self.overlay['right']=5
        with self.assertRaisesRegex(ContentError,'coordinates'):self.check()
    def test_overlay_inset_cannot_be_negative(self):
        self.overlay['inset_pixels']=-1
        with self.assertRaisesRegex(ContentError,'inset'):self.check()
    def test_composite_carries_original_region_and_ordered_overlays(self):
        value={'type':'composite_image','asset_id':'scene','region':{'left':0,'top':0,'right':100,'bottom':200,'source_width':300,'source_height':400},'overlays':[self.overlay],'caption':[{'type':'text','text':'Approved production caption.'}]}
        self.v.typed(value,'BlockPayload','scene')
    def test_sign_example_contains_registered_identity_type(self):
        self.v.typed({'type':'sign_examples','entry_ids':['sign-B1','sign-B2']},'BlockPayload','examples')
    def test_composite_rejects_invalid_region(self):
        value={'type':'composite_image','asset_id':'scene','region':{'left':0,'top':0,'right':999,'bottom':200,'source_width':300,'source_height':400},'overlays':[self.overlay],'caption':[]}
        with self.assertRaisesRegex(ContentError,'pixel bounds'):self.v.typed(value,'BlockPayload','scene')

if __name__=='__main__':unittest.main(verbosity=2)
