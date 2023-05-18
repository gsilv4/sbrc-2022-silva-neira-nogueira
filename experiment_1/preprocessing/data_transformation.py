import numpy as np
import pandas as pd
from scipy.stats import skew 
from scipy.stats import kurtosis 

num_of_rows = 1024
TextFileReader = pd.read_csv('full_capture20110818.csv', header=None, chunksize=num_of_rows, parse_dates=['frame.time'])

dfs = []
for chunk_df in TextFileReader:
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

    data = pd.DataFrame()

    data['frame_len_skew'] = chunk_df['frame.len'].resample('15s').agg(skew).bfill()
    data['frame_len_kurt'] = chunk_df['frame.len'].resample('15s').agg(kurtosis).bfill()
    data['tcp_time_delta_skew'] = chunk_df['tcp.time_delta'].resample('15s').agg(skew).bfill()
    data['tcp_time_delta_kurt'] = chunk_df['tcp.time_delta'].resample('15s').agg(kurtosis).bfill()
    data['tcp_window_size_skew'] = chunk_df['tcp.window_size'].resample('15s').agg(skew).bfill()
    data['tcp_window_size_kurt'] = chunk_df['tcp.window_size'].resample('15s').agg(kurtosis).bfill()
    data['Class'] = chunk_df['Class'].resample('15s').agg(max)

    dfs.append(chunk_df)
    
df = pd.concat(dfs,sort=False)

data.to_csv('./full_capture20110818_preprocessed.csv', index_label='frame.time')

