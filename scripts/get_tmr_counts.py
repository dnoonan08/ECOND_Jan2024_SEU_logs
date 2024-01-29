import json
import pandas as pd
import numpy as np
import glob
import re

hexacontrollers = [42,43]

def countsTotal(x):
    rollOvers=(x[1:]-x[:-1]<0).sum(axis=0)
    return rollOvers*256 + x[-1]

errorCountLists=[]
hexaData={}
regNames = None
for hexaNumber in hexacontrollers:
    hexa = f'hexa{hexaNumber}'
    hexaDataFiles = glob.glob(f'../logs/{hexa}/Run*json')
    fileNames=np.array(hexaDataFiles)
    fileNames.sort()


    for fname in fileNames:
        runNum=re.findall('Run_(\w*)_test',fname)[0]
        data=json.load(open(fname))
        #beam-on test is second in list if it is a PRBS test, 3rd if not
        testNumber = 2 if 'PRBS' in fname else 3
        try:
            if regNames is None:
                regNames=data['tests'][testNumber]['metadata']['tmr_err_names']
            errCounts=data['tests'][testNumber]['metadata']['tmr_err_cnts']
            errCounts=np.array(errCounts)
            errCounts=countsTotal(errCounts).tolist()
        except:
            errCounts=[0]*53
        errorCountLists.append([runNum,hexaNumber]+errCounts)

df=pd.DataFrame(errorCountLists)
df.columns=['Run','Hexacontroller']+regNames

df.to_csv('../data/tmr_error_counts_by_run.csv',index=False)
