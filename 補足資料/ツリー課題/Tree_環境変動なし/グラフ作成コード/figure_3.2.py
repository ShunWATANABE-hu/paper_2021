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
with open('MBtree_data_3-0.csv') as f:
    reader = csv.reader(f)
    MB_count30 = [row for row in reader]

with open('MBtree_data_5-3.csv') as f:
    reader = csv.reader(f)
    MB_count53 = [row for row in reader]

with open('MFtree_data_3-0.csv') as f:
    reader = csv.reader(f)
    MF_count30 = [row for row in reader]

with open('MFtree_data_5-3.csv') as f:
    reader = csv.reader(f)
    MF_count53 = [row for row in reader]


"""
最適行動を取った人数が、全体に占める割合の配列
"""
MB_rate30 = np.array(MB_count30, dtype = int) / 100
MF_rate30 = np.array(MF_count30, dtype = int) / 100
MB_rate53 = np.array(MB_count53, dtype = int) / 100
MF_rate53 = np.array(MF_count53, dtype = int) / 100

differ_30 = MB_rate30 - MF_rate30
differ_53 = MB_rate53 - MF_rate53

"""
移動平均を取る
"""
MB30_runave = [[0 for i in range(trial)] for j in range(parameter)]
MF30_runave = [[0 for i in range(trial)] for j in range(parameter)]
MB53_runave = [[0 for i in range(trial)] for j in range(parameter)]
MF53_runave = [[0 for i in range(trial)] for j in range(parameter)]

differ30_runave = [[0 for i in range(trial)] for j in range(parameter)]
differ53_runave = [[0 for i in range(trial)] for j in range(parameter)]

for i in range(parameter):
    a = pd.Series(MB_rate30[i])
    b = pd.Series(MB_rate53[i])
    c = pd.Series(MF_rate30[i])
    d = pd.Series(MF_rate53[i])
    e = pd.Series(differ_30[i])
    f = pd.Series(differ_53[i])

    a01 = a.rolling(window=10).mean()
    a02 = a01.tolist()
    MB30_runave[i] = a02

    b01 = b.rolling(window=10).mean()
    b02 = b01.tolist()
    MB53_runave[i] = b02

    c01 = c.rolling(window=10).mean()
    c02 = c01.tolist()
    MF30_runave[i] = c02

    d01 = d.rolling(window=10).mean()
    d02 = d01.tolist()
    MF53_runave[i] = d02

    e01 = e.rolling(window=10).mean()
    e02 = e01.tolist()
    differ30_runave[i] = e02

    f01 = f.rolling(window=10).mean()
    f02 = f01.tolist()
    differ53_runave[i] = f02

"""
図3.2
　・β=0.9,α=0.1-0.9における、MB,MFの最適行動の割合グラフ（MB30,MF30,MB53,MF53）
　・β=0.9,α=0.1-0.9における、MB,MFの差分のグラフ
"""

fig = plt.figure(figsize=(11,12))

x = list(range(1,101))
#報酬3-0, MF, β=0.9
y1 = MF_rate30[8]
y2 = MF_rate30[8+9*2]
y3 = MF_rate30[8+9*4]
y4 = MF_rate30[8+9*6]
y5 = MF_rate30[8+9*8]

#報酬3-0, MB, β=0.9
y6 = MB_rate30[8]
y7 = MB_rate30[8+9*2]
y8 = MB_rate30[8+9*4]
y9 = MB_rate30[8+9*6]
y10 = MB_rate30[8+9*8]

#報酬5-3, MF, β=0.9
y11 = MF_rate53[8]
y12 = MF_rate53[8+9*2]
y13 = MF_rate53[8+9*4]
y14 = MF_rate53[8+9*6]
y15 = MF_rate53[8+9*8]

#報酬5-3, MB, β=0.9
y16 = MB_rate53[8]
y17 = MB_rate53[8+9*2]
y18 = MB_rate53[8+9*4]
y19 = MB_rate53[8+9*6]
y20 = MB_rate53[8+9*8]

#報酬3-0, 差分, β=0.9
y21 = differ_30[8]
y22 = differ_30[8+9*2]
y23 = differ_30[8+9*4]
y24 = differ_30[8+9*6]
y25 = differ_30[8+9*8]

#報酬5-3, 差分, β=0.9
y26 = differ_53[8]
y27 = differ_53[8+9*2]
y28 = differ_53[8+9*4]
y29 = differ_53[8+9*6]
y30 = differ_53[8+9*8]


ax1 = fig.add_subplot(321, title="A図：課題成績(MF,報酬3 vs 0条件)", ylim=(0,100), xlabel="試行数", ylabel="課題成績(%)")
ax2 = fig.add_subplot(322, title="B図：課題成績(MB,報酬3 vs 0条件)", ylim=(0,100)) 
ax3 = fig.add_subplot(323, title="C図：課題成績(MF,報酬5 vs 3条件)", ylim=(0,100), xlabel="試行数", ylabel="課題成績(%)")
ax4 = fig.add_subplot(324, title="D図：課題成績(MB,報酬5 vs 3条件)", ylim=(0,100)) 
ax5 = fig.add_subplot(325, title="E図：学習アルゴリズム間の成績差(報酬3 vs 0条件)", ylim=(-5,30), xlabel="試行数", ylabel="課題成績の差分(%)")
ax6 = fig.add_subplot(326, title="F図：学習アルゴリズム間の成績差(報酬5 vs 3条件)", ylim=(-5,30)) 

ax1.plot(x, y1, label="α=0.1")
ax1.plot(x, y2, label="α=0.3")
ax1.plot(x, y3, label="α=0.5")
ax1.plot(x, y4, label="α=0.7")
ax1.plot(x, y5, label="α=0.9")

ax2.plot(x, y6, label="α=0.1")
ax2.plot(x, y7, label="α=0.3")
ax2.plot(x, y8, label="α=0.5")
ax2.plot(x, y9, label="α=0.7")
ax2.plot(x, y10, label="α=0.9")

ax3.plot(x, y11, label="α=0.1")
ax3.plot(x, y12, label="α=0.3")
ax3.plot(x, y13, label="α=0.5")
ax3.plot(x, y14, label="α=0.7")
ax3.plot(x, y15, label="α=0.9")

ax4.plot(x, y16, label="α=0.1")
ax4.plot(x, y17, label="α=0.3")
ax4.plot(x, y18, label="α=0.5")
ax4.plot(x, y19, label="α=0.7")
ax4.plot(x, y20, label="α=0.9")

ax5.plot(x, y21, label="α=0.1")
ax5.plot(x, y22, label="α=0.3")
ax5.plot(x, y23, label="α=0.5")
ax5.plot(x, y24, label="α=0.7")
ax5.plot(x, y25, label="α=0.9")

ax6.plot(x, y26, label="α=0.1")
ax6.plot(x, y27, label="α=0.3")
ax6.plot(x, y28, label="α=0.5")
ax6.plot(x, y29, label="α=0.7")
ax6.plot(x, y30, label="α=0.9")

ax1.hlines([20],0,100,linestyles='dotted',color='lightslategray')
ax1.hlines([40],0,100,linestyles='dotted',color='lightslategray')   
ax1.hlines([60],0,100,linestyles='dotted',color='lightslategray')
ax1.hlines([80],0,100,linestyles='dotted',color='lightslategray')
ax1.hlines([100],0,100,linestyles='dotted',color='lightslategray')

ax2.hlines([20],0,100,linestyles='dotted',color='lightslategray')
ax2.hlines([40],0,100,linestyles='dotted',color='lightslategray')   
ax2.hlines([60],0,100,linestyles='dotted',color='lightslategray')
ax2.hlines([80],0,100,linestyles='dotted',color='lightslategray')
ax2.hlines([100],0,100,linestyles='dotted',color='lightslategray')

ax3.hlines([20],0,100,linestyles='dotted',color='lightslategray')
ax3.hlines([40],0,100,linestyles='dotted',color='lightslategray')   
ax3.hlines([60],0,100,linestyles='dotted',color='lightslategray')
ax3.hlines([80],0,100,linestyles='dotted',color='lightslategray')
ax3.hlines([100],0,100,linestyles='dotted',color='lightslategray')

ax4.hlines([20],0,100,linestyles='dotted',color='lightslategray')
ax4.hlines([40],0,100,linestyles='dotted',color='lightslategray')   
ax4.hlines([60],0,100,linestyles='dotted',color='lightslategray')
ax4.hlines([80],0,100,linestyles='dotted',color='lightslategray')
ax4.hlines([100],0,100,linestyles='dotted',color='lightslategray')

ax5.hlines([0],0,100,linestyles='dotted',color='lightslategray')
ax5.hlines([5],0,100,linestyles='dotted',color='lightslategray')
ax5.hlines([10],0,100,linestyles='dotted',color='lightslategray')   
ax5.hlines([15],0,100,linestyles='dotted',color='lightslategray')
ax5.hlines([20],0,100,linestyles='dotted',color='lightslategray')
ax5.hlines([25],0,100,linestyles='dotted',color='lightslategray')

ax6.hlines([0],0,100,linestyles='dotted',color='lightslategray')
ax6.hlines([5],0,100,linestyles='dotted',color='lightslategray')
ax6.hlines([10],0,100,linestyles='dotted',color='lightslategray')   
ax6.hlines([15],0,100,linestyles='dotted',color='lightslategray')
ax6.hlines([20],0,100,linestyles='dotted',color='lightslategray')
ax6.hlines([25],0,100,linestyles='dotted',color='lightslategray')

ax1.legend()
ax2.legend()
ax3.legend()
ax4.legend()
ax5.legend()
ax6.legend()

file_name = "論文_図3.2.png"
plt.tight_layout()
plt.savefig(file_name,bbox_inches="tight",dpi=200)


"""
図3.2（3分割）
　・β=0.9,α=0.1-0.9における、MB,MFの最適行動の割合グラフ（MB30,MF30,MB53,MF53）
　・β=0.9,α=0.1-0.9における、MB,MFの差分のグラフ
"""

fig = plt.figure(figsize=(11,4))

x = list(range(1,101))
#報酬3-0, MF, β=0.9
y1 = MF_rate30[8]
y2 = MF_rate30[8+9*2]
y3 = MF_rate30[8+9*4]
y4 = MF_rate30[8+9*6]
y5 = MF_rate30[8+9*8]

#報酬3-0, MB, β=0.9
y6 = MB_rate30[8]
y7 = MB_rate30[8+9*2]
y8 = MB_rate30[8+9*4]
y9 = MB_rate30[8+9*6]
y10 = MB_rate30[8+9*8]

#報酬5-3, MF, β=0.9
y11 = MF_rate53[8]
y12 = MF_rate53[8+9*2]
y13 = MF_rate53[8+9*4]
y14 = MF_rate53[8+9*6]
y15 = MF_rate53[8+9*8]

#報酬5-3, MB, β=0.9
y16 = MB_rate53[8]
y17 = MB_rate53[8+9*2]
y18 = MB_rate53[8+9*4]
y19 = MB_rate53[8+9*6]
y20 = MB_rate53[8+9*8]

#報酬3-0, 差分, β=0.9
y21 = differ_30[8]
y22 = differ_30[8+9*2]
y23 = differ_30[8+9*4]
y24 = differ_30[8+9*6]
y25 = differ_30[8+9*8]

#報酬5-3, 差分, β=0.9
y26 = differ_53[8]
y27 = differ_53[8+9*2]
y28 = differ_53[8+9*4]
y29 = differ_53[8+9*6]
y30 = differ_53[8+9*8]


ax1 = fig.add_subplot(121, title="A図：課題成績(MF,報酬3 vs 0条件)", ylim=(0,100), xlabel="試行数", ylabel="課題成績(%)")
ax2 = fig.add_subplot(122, title="B図：課題成績(MB,報酬3 vs 0条件)", ylim=(0,100)) 

ax1.plot(x, y1, label="α=0.1")
ax1.plot(x, y2, label="α=0.3")
ax1.plot(x, y3, label="α=0.5")
ax1.plot(x, y4, label="α=0.7")
ax1.plot(x, y5, label="α=0.9")

ax2.plot(x, y6, label="α=0.1")
ax2.plot(x, y7, label="α=0.3")
ax2.plot(x, y8, label="α=0.5")
ax2.plot(x, y9, label="α=0.7")
ax2.plot(x, y10, label="α=0.9")

ax1.hlines([20],0,100,linestyles='dotted',color='lightslategray')
ax1.hlines([40],0,100,linestyles='dotted',color='lightslategray')   
ax1.hlines([60],0,100,linestyles='dotted',color='lightslategray')
ax1.hlines([80],0,100,linestyles='dotted',color='lightslategray')
ax1.hlines([100],0,100,linestyles='dotted',color='lightslategray')

ax2.hlines([20],0,100,linestyles='dotted',color='lightslategray')
ax2.hlines([40],0,100,linestyles='dotted',color='lightslategray')   
ax2.hlines([60],0,100,linestyles='dotted',color='lightslategray')
ax2.hlines([80],0,100,linestyles='dotted',color='lightslategray')
ax2.hlines([100],0,100,linestyles='dotted',color='lightslategray')

ax1.legend()
ax2.legend()

file_name = "論文_図3.2.1.png"
plt.tight_layout()
plt.savefig(file_name,bbox_inches="tight",dpi=200)


"""
"""
fig = plt.figure(figsize=(11,4))
plt.clf()

ax3 = fig.add_subplot(121, title="C図：課題成績(MF,報酬5 vs 3条件)", ylim=(0,100), xlabel="試行数", ylabel="課題成績(%)")
ax4 = fig.add_subplot(122, title="D図：課題成績(MB,報酬5 vs 3条件)", ylim=(0,100)) 

ax3.plot(x, y11, label="α=0.1")
ax3.plot(x, y12, label="α=0.3")
ax3.plot(x, y13, label="α=0.5")
ax3.plot(x, y14, label="α=0.7")
ax3.plot(x, y15, label="α=0.9")

ax4.plot(x, y16, label="α=0.1")
ax4.plot(x, y17, label="α=0.3")
ax4.plot(x, y18, label="α=0.5")
ax4.plot(x, y19, label="α=0.7")
ax4.plot(x, y20, label="α=0.9")

ax3.hlines([20],0,100,linestyles='dotted',color='lightslategray')
ax3.hlines([40],0,100,linestyles='dotted',color='lightslategray')   
ax3.hlines([60],0,100,linestyles='dotted',color='lightslategray')
ax3.hlines([80],0,100,linestyles='dotted',color='lightslategray')
ax3.hlines([100],0,100,linestyles='dotted',color='lightslategray')

ax4.hlines([20],0,100,linestyles='dotted',color='lightslategray')
ax4.hlines([40],0,100,linestyles='dotted',color='lightslategray')   
ax4.hlines([60],0,100,linestyles='dotted',color='lightslategray')
ax4.hlines([80],0,100,linestyles='dotted',color='lightslategray')
ax4.hlines([100],0,100,linestyles='dotted',color='lightslategray')

ax3.legend()
ax4.legend()

file_name = "論文_図3.2.2.png"
plt.tight_layout()
plt.savefig(file_name,bbox_inches="tight",dpi=200)

"""
"""
fig = plt.figure(figsize=(11,4))
plt.clf()

ax5 = fig.add_subplot(121, title="E図：学習アルゴリズム間の成績差(報酬3 vs 0条件)", ylim=(-5,30), xlabel="試行数", ylabel="課題成績の差分(%)")
ax6 = fig.add_subplot(122, title="F図：学習アルゴリズム間の成績差(報酬5 vs 3条件)", ylim=(-5,30)) 

ax5.plot(x, y21, label="α=0.1")
ax5.plot(x, y22, label="α=0.3")
ax5.plot(x, y23, label="α=0.5")
ax5.plot(x, y24, label="α=0.7")
ax5.plot(x, y25, label="α=0.9")

ax6.plot(x, y26, label="α=0.1")
ax6.plot(x, y27, label="α=0.3")
ax6.plot(x, y28, label="α=0.5")
ax6.plot(x, y29, label="α=0.7")
ax6.plot(x, y30, label="α=0.9")

ax5.hlines([0],0,100,linestyles='dotted',color='lightslategray')
ax5.hlines([5],0,100,linestyles='dotted',color='lightslategray')
ax5.hlines([10],0,100,linestyles='dotted',color='lightslategray')   
ax5.hlines([15],0,100,linestyles='dotted',color='lightslategray')
ax5.hlines([20],0,100,linestyles='dotted',color='lightslategray')
ax5.hlines([25],0,100,linestyles='dotted',color='lightslategray')

ax6.hlines([0],0,100,linestyles='dotted',color='lightslategray')
ax6.hlines([5],0,100,linestyles='dotted',color='lightslategray')
ax6.hlines([10],0,100,linestyles='dotted',color='lightslategray')   
ax6.hlines([15],0,100,linestyles='dotted',color='lightslategray')
ax6.hlines([20],0,100,linestyles='dotted',color='lightslategray')
ax6.hlines([25],0,100,linestyles='dotted',color='lightslategray')

ax5.legend()
ax6.legend()

file_name = "論文_図3.2.3.png"
plt.tight_layout()
plt.savefig(file_name,bbox_inches="tight",dpi=200)
