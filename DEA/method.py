import pandas as pd
import numpy as np
from pulp import LpProblem

from DEA.Data.DataInfo import DataInfo as DI
from sklearn import preprocessing
import pulp as p


class method(object):
    name = "DEA"
    df = pd.DataFrame()  # =pd.read_csv(r'G:\BTECH\project\dataset\selected\finaldf2')
    # path=r'finaldf2.csv'
    resultdf = pd.DataFrame()
    selectedDf = pd.DataFrame()
    M = 100000

    def efficiencyscore(self, L_prob):
        # i for neg attr
        # o for post attr
        ipresent = True
        opresent = True
        if len(DI.neg_attr) == 0:
            i_is_phi = False
        if len(DI.pos_attr) == 0:
            o_is_phi = False
        isum = 0
        osum = 0
        T = 0
        for v in L_prob.variables():
            if v.name.startswith('t') & ipresent:
                isum += 1 + v.varValue
            elif v.name.startswith('B') & opresent:
                osum += 1 - v.varValue
            elif v.name.startswith('T'):
                T = v.varValue
        escore = 1 + T + isum + osum
        return escore

    def compute(self):
        self.resultdf = self.resultdf.append(self.selectedDf)
        escoreList = list()

        print(self.selectedDf.index)

        for k in self.selectedDf.index:  # compute LP and eff score for each kth DMU
            prob = p.LpProblem('Problem', p.LpMinimize)

            T = p.LpVariable("T", lowBound=0)
            B = p.LpVariable.dicts("B", DI.pos_attr, lowBound=0)
            t = p.LpVariable.dicts("t", DI.neg_attr, lowBound=0)

            Bsum = p.lpSum(B[DI.pos_attr[r]] for r in range(len(DI.pos_attr)))
            tsum = p.lpSum(t[DI.neg_attr[i]] for i in range(len(DI.neg_attr)))

            prob += T + self.M * (Bsum + tsum)  # obj function

            llist = list()
            for i in self.selectedDf.index:
                llist.append(i)
            l = p.LpVariable.dicts("l", llist, lowBound=0)

            for j in self.selectedDf.index:
                if j == k:
                    continue
                else:
                    for i in DI.neg_attr:  # cons for neg attributes
                        prob += l[j] * self.selectedDf.loc[j, DI.neg_attr[i]] - \
                                t[i] * self.selectedDf[DI.neg_attr[i]].max() <= (1 + T) * self.selectedDf.loc[
                                    k, DI.neg_attr[i]]
                    for r in range(len(DI.pos_attr)):  # cons for pos attributes
                        prob += l[j] * self.selectedDf.loc[j, DI.pos_attr[r]] >= (1 - B[DI.pos_attr[r]]) * self.selectedDf.loc[k, DI.pos_attr[r]]
            prob += p.LpConstraint(p.lpSum(l[j] for j in self.selectedDf.index), p.LpConstraintEQ, rhs=1)

            '''
            print(prob)
            print(prob.status)
            prob.solve()
            print("Status:", p.LpStatus[prob.status])
            '''
            prob.solve()
            '''for v in prob.variables():
                if v.varValue > 0:
                    print(v.name, "=", v.varValue)
            '''
            escore = self.efficiencyscore(prob)
            print("escore:", escore)
            escoreList.append(escore)

        self.resultdf['Escore'] = escoreList
        self.resultdf = self.resultdf.sort_values(by='Escore', ascending=False)
        print(self.resultdf)
        return self

    def normalize(self):
        self.selectedDf = (self.selectedDf / (self.selectedDf.mean()))
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

        print("selectedDF empty", self.selectedDf.empty)
        return self
