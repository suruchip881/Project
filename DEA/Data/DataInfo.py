import pandas as pd
import numpy as np

class DataInfo():
    datapath=r'G:\BTECH\project\dataset\fastStorage\2013-8\Project\finaldf2.csv'
    attributes = list((pd.read_csv(datapath, sep=r'\s*,\s*')).columns.values.tolist())
    pos_attr = attributes
    neg_attr = list()
    def getdatapath(self):
        return self.datapath
    def getpos_attr(self):
        return self.pos_attr
    def getneg_attr(self):
        return self.neg_attr