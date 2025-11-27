import numpy as np
import pandas as pd
import os
from tqdm import tqdm
from mfm import *

class read_file:
    def __init__(self):
        self.name= 'read_file'
        self.date= 'December 2025'
        self.author= 'Zezhen Wu / wuzezhen5577@163.com'

        np.seterr(all='ignore')

    def read_flow(self, file_path):
        # 参数file_path为txt文件的路径
        data = pd.read_csv(file_path, sep=r'\s+', header=0)

        # 提取需要的列并重命名，其中sim为模拟数据，obs为观测数据
        result = data[['YR', 'MNTH', 'DY', 'MOD_RUN', 'OBS_RUN']]
        result.columns = ['year', 'month', 'day', 'sim', 'obs']

        return result

    def read_hcdn(self, hcdn_path):
        data = pd.read_csv(hcdn_path, sep=r',', header=0)
        result = data[['hcdn_site', 'lat', 'lon']]

        return result


    """
    我晕了
    还要判断有效数据
    """

    def read_valid_data(self, waterYearMonth=10, startYear=1980, endYear=2014, minDays=100, minYears=10, site_path=None,
                   data_dir_path=None, result_path=None):

        hcdn_conus_sites = self.read_hcdn(site_path)
        mfm_valid = pd.DataFrame(index=range(len(hcdn_conus_sites)),
                                 columns=['CAMELS_site', 'lat', 'lon', 'MFM', 'PPF', 'exp(-NMAEp)', 'omega',
                                          'varphi', 'eta'])
        data_dir_names = os.listdir(data_dir_path)
        j = 0
        k = 0

        for i in tqdm(range(len(hcdn_conus_sites))):
            if hcdn_conus_sites.loc[i, 'hcdn_site'] < 10000000:
                file_name = f"0{hcdn_conus_sites.loc[i, 'hcdn_site']}_05_model_output.txt"
            else:
                file_name = f"{hcdn_conus_sites.loc[i, 'hcdn_site']}_05_model_output.txt"
                # print('j = ', j)
                # print('k = ', k)

            for j in range(k, len(data_dir_names)):
                if data_dir_names[j] == file_name:
                    mfm_valid.iloc[i, 0:3] = hcdn_conus_sites.loc[i]
                    # print(data_dir_names[j])
                    k = i
                    file_name = f"{data_dir_path}/{file_name}"
                    flows = self.read_flow(file_name)
                    # 提取去重的年份，准备制作水年
                    # 先将日期全部转换为int型
                    flows['year'] = flows['year'].astype(int)
                    flows['month'] = flows['month'].astype(int)
                    flows['day'] = flows['day'].astype(int)
                    iyUnique = flows['year'].unique()
                    # 制作水年数据，即从waterYearMonth开始计算的年份
                    # 注意这里没有考虑startYear，后面再看
                    iyWater = np.zeros(len(flows), dtype=int)
                    for m in range(0, len(flows)):
                        if flows['month'][m] >= waterYearMonth:
                            iyWater[m] = flows['year'][m] + 1
                            flows.loc[m, 'iyWater'] = iyWater[m]
                        else:
                            iyWater[m] = flows['year'][m]
                            flows.loc[m, 'iyWater'] = iyWater[m]
                    flows['iyWater'] = flows['iyWater'].astype(int)
                    nYears = len(np.unique(iyWater))
                    # print(iyWater)

                    # 制作yearsJack与yearsBoot，后续循环保存数据时会用到

                    # 筛选有效数据，即sim&obs同时>zeroVal的样本
                    # 将所有有效的索引保存到ixValid，后续使用ixValid进行metrics的计算
                    zeroVal = -1
                    ixValid = flows[(flows['obs'] > zeroVal) & (flows['sim'] > zeroVal)].index
                    good_flows = flows.loc[ixValid]
                    # print(iyWater[ixValid])

                    # 通过iyWater对有效数据分组并统计各个水年的有效天数，按升序排列，最后重设列名
                    valid_days = good_flows['iyWater'].value_counts().sort_index().reset_index()
                    valid_days.columns = ['iyWater', 'good_days']
                    valid_years = valid_days.loc[valid_days['good_days'] > minDays]
                    # 再筛选有效天数>minDays的水年
                    if startYear is not None:
                        valid_years = valid_years.loc[valid_years['iyWater'] >= startYear]
                    if endYear is not None:
                        valid_years = valid_years.loc[valid_years['iyWater'] <= endYear]
                    nyValid = len(valid_years)

                    # 当有效水年数小于minYears时，返回全为空值的errorStats
                    if nyValid < minYears:
                        print('\033[1;31mError: It is NOT a valid data! Bootjack will return an empty row.' + '\033[0m')
                        return 0

                    # 提取有效数字
                    qSimValid = flows['sim'][ixValid]
                    qObsValid = flows['obs'][ixValid]


                    mfm_temp = mfm()
                    result = mfm_temp.model_fidelity_metric(qSimValid, qObsValid)
                    mfm_valid.iloc[i, 3:] = result

        return mfm_valid

    # 测试成功

    def read_result(self, result_path):
        result = pd.read_csv(result_path, sep='\t', header=0)
        return result


