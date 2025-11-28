"""
This script is the file reader of CAMELS dataset.
"""

import numpy as np
import pandas as pd
import os
from tqdm import tqdm
from mfm import *

class read_file:
    def __init__(self):
        np.seterr(all='ignore')

    def read_flow(self, file_path):
        """Read single flow data file"""
        data = pd.read_csv(file_path, sep=r'\s+', header=0)
        result = data[['YR', 'MNTH', 'DY', 'MOD_RUN', 'OBS_RUN']]
        result.columns = ['year', 'month', 'day', 'sim', 'obs']
        return result

    def read_result(self, result_path):
        """Read result file"""
        result = pd.read_csv(result_path, sep='\t', header=0)
        return result