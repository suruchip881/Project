import pandas as pd
import numpy as np

from DEA.Data.DataInfo import DataInfo as DI


class method(object):
    name = "ARAS"
    df = pd.DataFrame()  # =pd.read_csv(r'G:\BTECH\project\dataset\selected\finaldf2')
    # path=r'finaldf2.csv'
    resultdf = pd.DataFrame()
    selectedDf = pd.DataFrame()

    def normalize(self):
        newrow = list()

        for attr in DI.attributes:  #
            if DI.neg_attr.__contains__(attr):
                val = self.selectedDf[attr].min()
                newrow.append(val)
            elif DI.pos_attr.__contains__(attr):
                val = self.selectedDf[attr].max()
                newrow.append(val)
        self.resultdf = self.selectedDf #keeping a copy of the original values
        #print(newrow)
        #print(self.selectedDf)
        #self.selectedDf = self.selectedDf.append(newrow, ignore_index=True)
        self.selectedDf.loc[-1] = newrow
        #print(self.selectedDf)
        #print(newrow)

        self.selectedDf = self.selectedDf.div((self.selectedDf.sum(axis=0)), axis='columns')
        #print(self.selectedDf)
        return self
    def readData(self):
        self.df = pd.read_csv(DI.datapath, sep=r'\s*,\s*')
        return self

    def extractDF(self):
        noCores = input("Enter number of cores:")
        attr = DI.attributes[0]
        print(attr)
        self.selectedDf = self.df[self.df[attr].isin([noCores])]
        # self.selectedDf = self.selectedDf[attr] == noCores
        # self.selectedDf = self.df[self.df[attr] == noCores]
        #return self
        print("selectedDF empty", self.selectedDf.empty)
        return self

    def compute(self):
        for attr in DI.attributes: # multiply df by weights obtained from AHP
            self.selectedDf.loc[:, attr] *= 1

        sumlist = self.selectedDf.sum(axis=1)
        sumlist = sumlist/(sumlist.max())

        #self.selectedDf['score'] = sumlist

        lastrow = len(self.selectedDf)
        #self.selectedDf = self.selectedDf.drop(self.selectedDf.index[lastrow-1])

        sumlist = sumlist[:lastrow]
        self.resultdf['score'] = sumlist
        self.resultdf = self.resultdf.sort_values("score")
        self.resultdf = self.resultdf.drop(self.resultdf.index[lastrow-1])

        #self.resultdf = self.selectedDf
        print(self.resultdf)
        return self

