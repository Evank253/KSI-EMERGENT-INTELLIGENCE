import unittest

from runner.evidence.epistemic import EpistemicState, can_advance


class TestEpistemicState(unittest.TestCase):
    def test_qualification_does_not_authorize(self):
        self.assertTrue(can_advance(EpistemicState.REPLICATED, EpistemicState.QUALIFIED))
        self.assertNotEqual(EpistemicState.QUALIFIED.value, "AUTHORIZED")
