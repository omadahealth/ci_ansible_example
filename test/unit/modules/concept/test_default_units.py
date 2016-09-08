import unittest
import mock

import library.concept.concept

class DefaultConceptTestCase(unittest.TestCase):
    def setUp(self):
        print("Pre-test setup for DefaultConceptTestCase.")

    def test_equiv_operator(self):
        inst_a = library.concept.concept.ProofOfConceptClass()
        inst_b = library.concept.concept.ProofOfConceptClass()
        self.assertEquals(inst_a, inst_b)

    def test_equiv_operator_w_invalid_type(self):
        inst_a = library.concept.concept.ProofOfConceptClass()
        inst_b = object()
        with self.assertRaises(AssertionError) as e:
            inst_a == inst_b
