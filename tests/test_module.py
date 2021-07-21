import unittest

import stactools.lila_hkh_glacier


class TestModule(unittest.TestCase):
    def test_version(self):
        self.assertIsNotNone(stactools.lila_hkh_glacier.__version__)
