import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rcParams
rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['Hiragino Maru Gothic Pro', 'Yu Gothic', 'Meirio', 'Takao', 'IPAexGothic', 'IPAPGothic', 'Noto Sans CJK JP']

trial = 100
parameter = 9*9

"""
α,β のリストを作る
"""
para_list = [[i,j] for i in np.arange(0.1,1.0,0.1) for j in np.arange(0.1,1.0,0.1)]

for i in range(parameter):
    para_list[i][0] = round(para_list[i][0],1)
    para_list[i][1] = round(para_list[i][1],1)

"""
行動データを取得
"""

with open('MBtreeR_data_3-0.csv') as f:
    reader = csv.reader(f)
    MB_count30 = [row for row in reader]

with open('MBtreeR_data_5-3.csv') as f:
    reader = csv.reader(f)
    MB_count53 = [row for row in reader]

with open('MFtreeR_data_3-0.csv') as f:
    reader = csv.reader(f)
    MF_count30 = [row for row in reader]

with open('MFtreeR_data_5-3.csv') as f:
    reader = csv.reader(f)
    MF_count53 = [row for row in reader]

"""
最適行動を取った人数が、全体に占める割合の配列
"""
MB_rate30 = np.array(MB_count30, dtype = int) / 100
MF_rate30 = np.array(MF_count30, dtype = int) / 100
MB_rate53 = np.array(MB_count53, dtype = int) / 100
MF_rate53 = np.array(MF_count53, dtype = int) / 100

"""
100試行を通じて、最も成績が良い（最適行動を選んだ人数の合計が最大）パラメータを見つける
 → 各パラメータにおける「100試行を通じた、最適行動の合計人数」を算出
    ・MB_count_np[i,:] → i番目のパラメータ、100試行分
    ・MB_count_np[:,i] → 全パラメータ、i試行目

 → argmax 関数(配列中で一番大きい要素のインデックスを取得する)でインデックスを取得

取得したインデックスをもとに、グラフ用のデータを取得する
 → 最高成績パラにおける、各学習の最適行動の割合と、MB,MF学習の差分を取得
 → グラフ用に、10試行ごとの移動平均を取る
    ・pandas の series で、データフレームを作成
    ・データフレームに rolling を使用して、移動平均を取る

"""

#---各パラメータにおける 「100試行を通じて、最適行動を選んだ人数の合計」 を算出----------------
MB_sum_para30 = [0 for i in range(parameter)]
MF_sum_para30 = [0 for i in range(parameter)]
MB_sum_para53 = [0 for i in range(parameter)]
MF_sum_para53 = [0 for i in range(parameter)]

for i in range(81):
    MB_sum_para30[i] = np.sum(np.array(MB_count30, dtype = int)[i,:])
    MF_sum_para30[i] = np.sum(np.array(MF_count30, dtype = int)[i,:])
    MB_sum_para53[i] = np.sum(np.array(MB_count53, dtype = int)[i,:])
    MF_sum_para53[i] = np.sum(np.array(MF_count53, dtype = int)[i,:])

#---最適行動を最も多く取れたパラメータのindexを取得--------------------------------------
max_index_MB30 = np.argmax(MB_sum_para30)
max_index_MF30 = np.argmax(MF_sum_para30)
max_index_MB53 = np.argmax(MB_sum_para53)
max_index_MF53 = np.argmax(MF_sum_para53)

#---最高成績のパラメータを取得--------------------------------------------------------
print("MB学習_3-0: ",para_list[max_index_MB30])
print("MF学習_3-0: ",para_list[max_index_MF30])
print("MB学習_5-3: ",para_list[max_index_MB53])
print("MF学習_5-3: ",para_list[max_index_MF53])

#---最高成績のパラメータにおける最適行動の割合と、MB,MF学習の差分を取得---------------------
optimal_MBrate30 = MB_rate30[max_index_MB30]
optimal_MFrate30 = MF_rate30[max_index_MF30]
optimal_MBrate53 = MB_rate53[max_index_MB53]
optimal_MFrate53 = MF_rate53[max_index_MF53]

optimal_differ30 = optimal_MBrate30 - optimal_MFrate30
optimal_differ53 = optimal_MBrate53 - optimal_MFrate53

#---移動平均を取る-----------------------------------------------------------------
"""
pandas → Series → rolling を使う
"""
a = pd.Series(optimal_MBrate30)
b = pd.Series(optimal_MFrate30)
c = pd.Series(optimal_MBrate53)
d = pd.Series(optimal_MFrate53)
e = pd.Series(optimal_differ30)
f = pd.Series(optimal_differ53)

MB_graph30 = a.rolling(window=10).mean()
MF_graph30 = b.rolling(window=10).mean()
MB_graph53 = c.rolling(window=10).mean()
MF_graph53 = d.rolling(window=10).mean()

differ_graph30 = e.rolling(window=10).mean()
differ_graph53 = f.rolling(window=10).mean()

"""
付録_図B1
　・MB,MFの最適行動の割合グラフ（MB30,MF30,MB53,MF53）
　・MB,MFの差分のグラフ
"""

fig = plt.figure(figsize=(12, 4))

x = list(range(1,101))
y1 = optimal_MBrate30
y2 = optimal_MFrate30
y3 = optimal_MBrate53
y4 = optimal_MFrate53

y5 = optimal_differ30
y6 = optimal_differ53

ax1 = fig.add_subplot(121, title="B1.1図：各学習システムの成績(環境変動有)", ylim=(0,100), xlabel="試行数", ylabel="課題成績(%)")
ax2 = fig.add_subplot(122, title="B1.2図：学習システム間の成績差(環境変動有)", ylim=(-5,20), xlabel="試行数", ylabel="課題成績の差分(%)") 

ax1.plot(x, y1, label="MB_報酬：3 vs 0条件")
ax1.plot(x, y2, label="MF_報酬：3 vs 0条件")
ax1.plot(x, y3, label="MB_報酬：5 vs 3条件")
ax1.plot(x, y4, label="MF_報酬：5 vs 3条件")

ax2.plot(x, y5, label="報酬：3 vs 0条件")
ax2.plot(x, y6, label="報酬：5 vs 3条件")

ax1.hlines([20],0,100,linestyles='dotted',color='lightslategray')
ax1.hlines([40],0,100,linestyles='dotted',color='lightslategray')   
ax1.hlines([60],0,100,linestyles='dotted',color='lightslategray')
ax1.hlines([80],0,100,linestyles='dotted',color='lightslategray')
ax1.hlines([100],0,100,linestyles='dotted',color='lightslategray')

ax2.hlines([0],0,100,linestyles='dotted',color='lightslategray')
ax2.hlines([5],0,100,linestyles='dotted',color='lightslategray')
ax2.hlines([10],0,100,linestyles='dotted',color='lightslategray')   
ax2.hlines([15],0,100,linestyles='dotted',color='lightslategray')
ax2.hlines([20],0,100,linestyles='dotted',color='lightslategray')

ax1.legend()
ax2.legend()

file_name = "付録_図B1.png"
plt.savefig(file_name,bbox_inches="tight",dpi=200)
