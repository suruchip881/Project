from DEA.method import method
from twisted.trial import unittest
import pandas as pd


class TestMethod(unittest.TestCase):
    m1 = method()
    def test_compute(self):
        self.m1 = self.m1.readData()
        self.m1 = self.m1.extractDF()
        self.m1 = self.m1.normalize()
        self.m1 = self.m1.compute()
        self.assertTrue(not self.m1.resultdf.empty, "Result obtained")


        #self.assertTrue(not res.empty)

    def test_normalize(self):
        self.m1 = self.m1.readData()
        self.m1 = self.m1.extractDF()
        self.m1 = self.m1.normalize()
        df= pd.DataFrame()
        for val in self.m1.selectedDf.max():
            if not val:
                self.fail("Not normalized")
                return
        self.assertTrue("Normalized successfully")
        #self.assertTrue(m.selectedDf.between(0,1,True))

    def test_readData(self):
        #self.m1 = method()
        self.m1 = self.m1.readData()
        self.assertTrue(not self.m1.df.empty)
    def test_extractDF(self):
        selfm1 = self.m1.readData()
        print (self.m1.df.empty)
        #m = method()
        self.m1 = self.m1.extractDF()
        if self.m1.selectedDf.empty:
            self.fail("Empty extracted DF")
            return
        #ser = self.m1.selectedDf[self.m1.selectedDf.columns[0:1]]
        df1 = self.m1.selectedDf.iloc[:,0:1]
        #print( "printing df1 ",df1)
        for value in df1.values:
            print(value)
            if not value == 6.0:
                self.fail("Failed")
                return
        self.assertTrue("Success extract")

