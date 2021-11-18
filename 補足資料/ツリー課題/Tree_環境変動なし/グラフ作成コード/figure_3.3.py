import numpy as np
import csv
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rcParams

rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['Hiragino Maru Gothic Pro', 'Yu Gothic', 'Meirio', 'Takao', 'IPAexGothic', 'IPAPGothic', 'Noto Sans CJK JP']

trial = 100
parameter = 9*9

with open('cohen_h_30.csv') as f:
    reader = csv.reader(f)
    cohen_h_30 = [row for row in reader]

with open('cohen_h_53.csv') as f:
    reader = csv.reader(f)
    cohen_h_53 = [row for row in reader]

cohen_h30 = np.array(cohen_h_30, dtype = float)
cohen_h30 = np.abs(cohen_h30)

cohen_h53 = np.array(cohen_h_53, dtype = float)
cohen_h53 = np.abs(cohen_h53)

"""
np.abs で絶対値を取っている

cohen_h[0] = α=0.1, β=0.1
cohen_h[1] = α=0.1, β=0.2

cohen_h[8] = α=0.1, β=0.9   
cohen_h[9] = α=0.2, β=0.1 

cohen_h[17] = α=0.2, β=0.9
"""

"""
移動平均を取る
"""
cohen30_runave = [[0 for i in range(trial)] for j in range(parameter)]
cohen53_runave = [[0 for i in range(trial)] for j in range(parameter)]

for i in range(parameter):
    a = pd.Series(cohen_h30[i])
    b = pd.Series(cohen_h53[i])

    a01 = a.rolling(window=10).mean()
    a02 = a01.tolist()
    cohen30_runave[i] = a02

    b01 = b.rolling(window=10).mean()
    b02 = b01.tolist()
    cohen53_runave[i] = a02


"""
図3.3
　・MB,MFの最適行動の差分の効果量グラフ
"""

fig = plt.figure(figsize=(11, 4))

x = list(range(1,101))
y1 = cohen_h30[8]
y2 = cohen_h30[8+9*2]
y3 = cohen_h30[8+9*4]
y4 = cohen_h30[8+9*6]
y5 = cohen_h30[8+9*8]

y6 = cohen_h53[8]
y7 = cohen_h53[8+9*2]
y8 = cohen_h53[8+9*4]
y9 = cohen_h53[8+9*6]
y10 = cohen_h53[8+9*8]


ax1 = fig.add_subplot(121, title="A図：cohenのh(報酬3 vs 0条件)", ylim=(-0.1,0.5), xlabel="試行数", ylabel="効果量の大きさ")
ax2 = fig.add_subplot(122, title="B図：cohenのh(報酬5 vs 3条件)", ylim=(-0.1,0.5), xlabel="試行数") 

ax2.axes.yaxis.set_visible(False)

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

ax1.hlines([0],0,100,linestyles='dotted',color='lightslategray')
ax1.hlines([0.1],0,100,linestyles='dotted',color='lightslategray')   
ax1.hlines([0.2],0,100,linestyles='dotted',color='lightslategray')
ax1.hlines([0.3],0,100,linestyles='dotted',color='lightslategray')
ax1.hlines([0.4],0,100,linestyles='dotted',color='lightslategray')

ax2.hlines([0],0,100,linestyles='dotted',color='lightslategray')
ax2.hlines([0.1],0,100,linestyles='dotted',color='lightslategray')   
ax2.hlines([0.2],0,100,linestyles='dotted',color='lightslategray')
ax2.hlines([0.3],0,100,linestyles='dotted',color='lightslategray')
ax2.hlines([0.4],0,100,linestyles='dotted',color='lightslategray')

ax1.legend()
ax2.legend()

file_name = "論文_図3.3.png"
plt.tight_layout()
plt.savefig(file_name,bbox_inches="tight",dpi=200)


