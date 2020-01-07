from DEA.method import method
from twisted.trial import unittest
import pandas as pd


class TestMethod(unittest.TestCase):
    def test_compute(self):
        m = method()
        res = pd.DataFrame()
        res = m.compute()
        self.assertTrue(not res.empty)

    def test_normalize(self):
        m = method()
        m = m.normalize()
        self.assertTrue(m.selectedDf.all())

    def test_readData(self):
        m = method()
        m = m.readData()
        self.assertTrue(not m.df.empty)

