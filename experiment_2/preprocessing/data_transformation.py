import csv
import nest_asyncio
import numpy as np
import pandas as pd
from scipy.stats import skew 
from scipy.stats import kurtosis 
import os

nest_asyncio.apply()


def filter_by_percentage(y):
  y_nonzero_num = np.count_nonzero(y==1)
  y_zero_num = np.count_nonzero(y==0)
  y_total_num = y_nonzero_num + y_zero_num
  y_total_10_percent = (0.2/100) * y_total_num
  label = 0

  if y_nonzero_num >= y_total_10_percent:
    label = 1

  return label


dfs = pd.DataFrame()

for file in os.listdir():
  if file.endswith(".csv") and file != 'full_capture20110818.csv' :
    print(f'[+] Processing {file} ...')

    chunk_df = pd.read_csv(file, parse_dates=['frame.time'])
    
    chunk_df['Class'] = 0

    chunk_df['Class'] = np.where((chunk_df['ip.src'] == '147.32.84.165') |
                                 (chunk_df['ip.src'] == '147.32.84.191') |
                                 (chunk_df['ip.src'] == '147.32.84.192') |
                                 (chunk_df['ip.src'] == '147.32.84.193') |
                                 (chunk_df['ip.src'] == '147.32.84.204') |
                                 (chunk_df['ip.src'] == '147.32.84.205') |
                                 (chunk_df['ip.src'] == '147.32.84.206') |
                                 (chunk_df['ip.src'] == '147.32.84.207') |
                                 (chunk_df['ip.src'] == '147.32.84.208') |
                                 (chunk_df['ip.src'] == '147.32.84.209') |
                                 (chunk_df['ip.dst'] == '147.32.84.165') |
                                 (chunk_df['ip.dst'] == '147.32.84.191') |
                                 (chunk_df['ip.dst'] == '147.32.84.192') |
                                 (chunk_df['ip.dst'] == '147.32.84.193') |
                                 (chunk_df['ip.dst'] == '147.32.84.204') |
                                 (chunk_df['ip.dst'] == '147.32.84.205') |
                                 (chunk_df['ip.dst'] == '147.32.84.206') |
                                 (chunk_df['ip.dst'] == '147.32.84.207') |
                                 (chunk_df['ip.dst'] == '147.32.84.208') |
                                 (chunk_df['ip.dst'] == '147.32.84.209'), 1, chunk_df['Class'])
    
    
    chunk_df = chunk_df.drop(columns=['ip.src', 'ip.dst', 'frame.protocols'])

    chunk_df = chunk_df.set_index('frame.time')

    window_sz = '1s'

    data = pd.DataFrame()

    data['frame_len_skew'] = chunk_df['frame.len'].resample(window_sz).agg(skew)
    data['frame_len_kurt'] = chunk_df['frame.len'].resample(window_sz).agg(kurtosis)
    data['frame_time_delta_skew'] = chunk_df['frame.time_delta'].resample(window_sz).agg(skew)
    data['frame_time_delta_kurt'] = chunk_df['frame.time_delta'].resample(window_sz).agg(kurtosis)
    data['tcp_window_size_skew'] = chunk_df['tcp.window_size'].resample(window_sz).agg(skew)
    data['tcp_window_size_kurt'] = chunk_df['tcp.window_size'].resample(window_sz).agg(kurtosis)
    data['Class'] = chunk_df['Class'].resample(window_sz).max()

    dfs = dfs.append(data) 

dfs.to_csv('./full_capture20110818_preprocessed_frame_delta_time_pre_attack.csv', index_label='frame.time')

