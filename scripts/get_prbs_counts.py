import json
import pandas as pd
import numpy as np
import glob
import re
from scipy import stats

hexacontrollers = [42,43]

errorCountLists=[]
hexaData={}
regNames = None
error_data = []
for hexaNumber in hexacontrollers:
    hexa = f'hexa{hexaNumber}'
    hexaDataFiles = glob.glob(f'../logs/{hexa}/Run*PRBS*json')
    fileNames=np.array(hexaDataFiles)
    fileNames.sort()


    for fname in fileNames:
        print(fname)
        runNum=re.findall('Run_(\w*)_test',fname)[0].split('_')[0]
        data=json.load(open(fname))
        #beam-on test is second in list if it is a PRBS test, 3rd if not
        testNumber = 2 if 'PRBS' in fname else 3
        try:
            d15=np.array(np.array(data['tests'][2]['metadata']['prbs_15_err_count'])[:,1].tolist())
            d7=np.array(data['tests'][2]['metadata']['prbs_7_err_count'])[:,1:].astype(int)

            data_diffs=np.array(data['tests'][2]['metadata']['daq_asic_post_beam'])
            modes=stats.mode(data_diffs,axis=1)[0]
            prbs_errs_output = (data_diffs!=modes).sum(axis=0)
            lineHasErr=(data_diffs!=modes).any(axis=1)

            data_w_err = np.vectorize(lambda x: f'{x:032b}')(data_diffs[lineHasErr])
            bit_diff = np.vectorize(lambda x: f'{x:032b}')(np.bitwise_xor(data_diffs,modes)[lineHasErr])

            nbitsDiff=np.vectorize(lambda x: x.count('1'))(bit_diff).sum(axis=1)
            N=data_w_err.shape[0]
            error_data.append(np.concatenate((np.array([runNum,hexaNumber]*N).reshape(N,-1),data_w_err,bit_diff,nbitsDiff.reshape(N,-1)),axis=1))
            #####
            ## try to implement logic to detect wrap arounds
            ##    this isn't observed at all, only one possible i2c error (all 0 outputs for one reading) so ignore for now
            # wraparound = (np.diff(d15,axis=0)<0)
            # wraparound_idx=np.where(wraparound.any(axis=1))[0]+1
            # misread = (d15[wraparound_idx]==0).all(axis=1) & (d15[wraparound_idx-1]==d15[wraparound_idx+1]).all(axis=1)
            # if wraparound:
            #     print('PRBS errors counts cleared during run')
            #     print(' HANDLING THIS HAS NOT YET BEEN IMPLEMENTED')
            #     prbs_errs_input = np.array([0]*12)
            # else:
            #     prbs_errs_input = d15[-1]
            prbs_errs_input = d15[-1]
            x=[runNum, hexaNumber]+prbs_errs_input.tolist() + prbs_errs_output.tolist()
            errorCountLists.append(x)
        except:
            print('HERE???')
            errorCountLists.append([0]*20)

df=pd.DataFrame(errorCountLists)
df.columns=['Run','Hexacontroller']+[f'eRx_{i:02d}_errors' for i in range(12)]+[f'eTx_{i:02d}_errors' for i in range(6)]

df.to_csv('../data/prbs_error_counts_by_run.csv',index=False)

df2=pd.DataFrame(np.concatenate(error_data))
df2.columns=['Run','Hexacontroller']+[f'PRBS_data_eTx{i}' for i in range(6)] + [f'BitDiff_eRx{i}' for i in range(6)]+['nBitsDiff']

df2.to_csv('../data/prbs_link_capture_errors.csv',index=False)
