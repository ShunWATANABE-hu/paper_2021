import numpy as np
import math
import csv

"""
行動データを取得
"""
with open('MBRocket_data_3-0.csv') as f:
    reader = csv.reader(f)
    MB_count30 = [row for row in reader]

with open('MBRocket_data_5-3.csv') as f:
    reader = csv.reader(f)
    MB_count53 = [row for row in reader]

with open('MFRocket_data_3-0.csv') as f:
    reader = csv.reader(f)
    MF_count30 = [row for row in reader]

with open('MFRocket_data_5-3.csv') as f:
    reader = csv.reader(f)
    MF_count53 = [row for row in reader]


#2次元配列のまま演算できるよう ndarray に変換
MB_count30_np = np.array(MB_count30,dtype = float)
MF_count30_np = np.array(MF_count30,dtype = float)
MB_count53_np = np.array(MB_count53,dtype = float)
MF_count53_np = np.array(MF_count53,dtype = float)

#人数を割合に変換
MB_rate30 = MB_count30_np/10000
MF_rate30 = MF_count30_np/10000

MB_rate53 = MB_count53_np/10000
MF_rate53 = MF_count53_np/10000

#計算のために変形
MB30_reshape = np.reshape(MB_rate30,(8100,1))
MF30_reshape = np.reshape(MF_rate30,(8100,1))

MB53_reshape = np.reshape(MB_rate53,(8100,1))
MF53_reshape = np.reshape(MF_rate53,(8100,1))

#ルートを計算
MB30_root = [0 for i in range(8100)]
MF30_root = [0 for i in range(8100)]
MB53_root = [0 for i in range(8100)]
MF53_root = [0 for i in range(8100)]

for i in range(8100):
    MB30_root[i] = math.sqrt(MB30_reshape[i])
    MF30_root[i] = math.sqrt(MF30_reshape[i])
    MB53_root[i] = math.sqrt(MB53_reshape[i])
    MF53_root[i] = math.sqrt(MF53_reshape[i])

#cohen's_h を計算
cohen_h30 = [0 for i in range(8100)]
cohen_h53 = [0 for i in range(8100)]

for j in range(8100):
    cohen_h30[j] = round(2*(math.asin(MB30_root[j]) - math.asin(MF30_root[j])),4)    
    cohen_h53[j] = round(2*(math.asin(MB53_root[j]) - math.asin(MF53_root[j])),4)    

cohen_h_reshape30 = np.reshape(cohen_h30,(81,100))
cohen_h_reshape53 = np.reshape(cohen_h53,(81,100))


with open('cohen_h_30.csv', 'w') as file:
    writer = csv.writer(file, lineterminator='\n')
    writer.writerows(cohen_h_reshape30)

with open('cohen_h_53.csv', 'w') as file:
    writer = csv.writer(file, lineterminator='\n')
    writer.writerows(cohen_h_reshape53)