import csv
import numpy as np
import seaborn as sns
from matplotlib.colors import ListedColormap, BoundaryNorm
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

with open('cohen_h_30.csv') as f:
    reader = csv.reader(f)
    cohen_h_30 = [row for row in reader]

with open('cohen_h_53.csv') as f:
    reader = csv.reader(f)
    cohen_h_53 = [row for row in reader]

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
cohen's h
"""
cohen_h30 = np.array(cohen_h_30, dtype = float)
cohen_h30 = np.abs(cohen_h30)

cohen_h53 = np.array(cohen_h_53, dtype = float)
cohen_h53 = np.abs(cohen_h53)

"""
図3.4
　・4条件の100試行終了時の全パラメータ成績
　・100試行終了時の全パラメータの成績差 + 効果量
"""

cmap = ListedColormap(['white','white','white','white'])
bounds = np.linspace(0,100,5)
norm = BoundaryNorm(bounds,cmap.N)

label = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]

fig = plt.figure(figsize=(10, 12))

ax1 = fig.add_subplot(321, title="A図：課題成績一覧(MB,報酬3 vs 0条件)", xlabel="β", ylabel="α")
ax2 = fig.add_subplot(322, title="B図：課題成績一覧(MF,報酬3 vs 0条件)", xlabel="β", ylabel="α")
ax3 = fig.add_subplot(323, title="C図：課題成績一覧(MB,報酬5 vs 3条件)", xlabel="β", ylabel="α")
ax4 = fig.add_subplot(324, title="D図：課題成績一覧(MF,報酬5 vs 3条件)", xlabel="β", ylabel="α")
ax5 = fig.add_subplot(325, title="E図：成績差の一覧と効果量(報酬3 vs 0条件)", xlabel="β", ylabel="α")
ax6 = fig.add_subplot(326, title="F図：成績差の一覧と効果量(報酬5 vs 3条件)", xlabel="β", ylabel="α")



sns.heatmap(np.reshape(MB_rate30[:,99],(9,9)), cmap='RdBu_r', vmax=100,vmin=0,
            xticklabels = label, yticklabels = label, linewidths=0.01,
            annot=True, fmt='.1f', ax=ax1, square=True)
        
sns.heatmap(np.reshape(MF_rate30[:,99],(9,9)), cmap='RdBu_r', vmax=100,vmin=0,
            xticklabels = label, yticklabels = label, linewidths=0.01,
            annot=True, fmt='.1f', ax=ax2, square=True, cbar=False)
 
sns.heatmap(np.reshape(MB_rate53[:,99],(9,9)), cmap='RdBu_r', vmax=100,vmin=0,
            xticklabels = label, yticklabels = label, linewidths=0.01,
            annot=True, fmt='.1f', ax=ax3, square=True)

sns.heatmap(np.reshape(MF_rate53[:,99],(9,9)), cmap='RdBu_r', vmax=100,vmin=0,
            xticklabels = label, yticklabels = label, linewidths=0.01,
            annot=True, fmt='.1f', ax=ax4, square=True, cbar=False)
 
sns.heatmap(np.reshape(cohen_h30[:,99],(9,9)), cmap=cmap, 
            xticklabels = False, yticklabels = False,   
            annot=True, fmt='.2f', cbar = False, linewidths=0.01, ax=ax5)

sns.heatmap(np.reshape(differ_30[:,99],(9,9)), cmap='RdBu_r', vmax=20,vmin=-20,
            xticklabels = label, yticklabels = label, linewidths=0.01,
            ax=ax5, square=True)

sns.heatmap(np.reshape(cohen_h53[:,99],(9,9)), cmap=cmap, 
            xticklabels = False, yticklabels = False, annot=True, 
            fmt='.2f', cbar = False, linewidths=0.01, ax=ax6)

sns.heatmap(np.reshape(differ_53[:,99],(9,9)), cmap='RdBu_r', vmax=20,vmin=-20,
            xticklabels = label, yticklabels = label, linewidths=0.01,
            ax=ax6, square=True, cbar=False)
      
ax1.set_xlabel("β")
ax1.set_ylabel("α")

ax2.set_xlabel("β")
ax2.set_ylabel("α")

ax3.set_xlabel("β")
ax3.set_ylabel("α")

ax4.set_xlabel("β")
ax4.set_ylabel("α")

ax5.set_xlabel("β")
ax5.set_ylabel("α")

ax6.set_xlabel("β")
ax6.set_ylabel("α")

file_name = "論文_図3.4.png"
plt.tight_layout()
plt.savefig(file_name,bbox_inches="tight",dpi=200)



"""
図3.4（3分割）
　・4条件の100試行終了時の全パラメータ成績
　・100試行終了時の全パラメータの成績差 + 効果量
"""

cmap = ListedColormap(['white','white','white','white'])
bounds = np.linspace(0,100,5)
norm = BoundaryNorm(bounds,cmap.N)

label = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]

fig = plt.figure(figsize=(10, 4))

ax1 = fig.add_subplot(121, title="A図：課題成績一覧(MB,報酬3 vs 0条件)", xlabel="β", ylabel="α")
ax2 = fig.add_subplot(122, title="B図：課題成績一覧(MF,報酬3 vs 0条件)", xlabel="β", ylabel="α")

sns.heatmap(np.reshape(MB_rate30[:,99],(9,9)), cmap='RdBu_r', vmax=100,vmin=0,
            xticklabels = label, yticklabels = label, linewidths=0.01,
            annot=True, fmt='.1f', ax=ax1, square=True)
        
sns.heatmap(np.reshape(MF_rate30[:,99],(9,9)), cmap='RdBu_r', vmax=100,vmin=0,
            xticklabels = label, yticklabels = label, linewidths=0.01,
            annot=True, fmt='.1f', ax=ax2, square=True, cbar=False)
        
ax1.set_xlabel("β")
ax1.set_ylabel("α")

ax2.set_xlabel("β")
ax2.set_ylabel("α")

file_name = "論文_図3.4.1.png"
plt.tight_layout()
plt.savefig(file_name,bbox_inches="tight",dpi=200)

"""
"""
cmap = ListedColormap(['white','white','white','white'])
bounds = np.linspace(0,100,5)
norm = BoundaryNorm(bounds,cmap.N)

label = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]

fig = plt.figure(figsize=(10, 4))
plt.clf()

ax3 = fig.add_subplot(121, title="C図：課題成績一覧(MB,報酬5 vs 3条件)", xlabel="β", ylabel="α")
ax4 = fig.add_subplot(122, title="D図：課題成績一覧(MF,報酬5 vs 3条件)", xlabel="β", ylabel="α")
      
sns.heatmap(np.reshape(MB_rate53[:,99],(9,9)), cmap='RdBu_r', vmax=100,vmin=0,
            xticklabels = label, yticklabels = label, linewidths=0.01,
            annot=True, fmt='.1f', ax=ax3, square=True)

sns.heatmap(np.reshape(MF_rate53[:,99],(9,9)), cmap='RdBu_r', vmax=100,vmin=0,
            xticklabels = label, yticklabels = label, linewidths=0.01,
            annot=True, fmt='.1f', ax=ax4, square=True, cbar=False)


ax3.set_xlabel("β")
ax3.set_ylabel("α")

ax4.set_xlabel("β")
ax4.set_ylabel("α")

file_name = "論文_図3.4.2.png"
plt.tight_layout()
plt.savefig(file_name,bbox_inches="tight",dpi=200)

"""
"""
cmap = ListedColormap(['white','white','white','white'])
bounds = np.linspace(0,100,5)
norm = BoundaryNorm(bounds,cmap.N)

label = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]

fig = plt.figure(figsize=(10,4))
plt.clf()

ax5 = fig.add_subplot(121, title="E図：成績差の一覧と効果量(報酬3 vs 0条件)", xlabel="β", ylabel="α")
ax6 = fig.add_subplot(122, title="F図：成績差の一覧と効果量(報酬5 vs 3条件)", xlabel="β", ylabel="α")

sns.heatmap(np.reshape(cohen_h30[:,99],(9,9)), cmap=cmap, 
            xticklabels = False, yticklabels = False,   
            annot=True, fmt='.2f', cbar = False, linewidths=0.01, ax=ax5)

sns.heatmap(np.reshape(differ_30[:,99],(9,9)), cmap='RdBu_r', vmax=20,vmin=-20,
            xticklabels = label, yticklabels = label, linewidths=0.01,
            ax=ax5, square=True)

sns.heatmap(np.reshape(cohen_h53[:,99],(9,9)), cmap=cmap, 
            xticklabels = False, yticklabels = False, annot=True, 
            fmt='.2f', cbar = False, linewidths=0.01, ax=ax6)

sns.heatmap(np.reshape(differ_53[:,99],(9,9)), cmap='RdBu_r', vmax=20,vmin=-20,
            xticklabels = label, yticklabels = label, linewidths=0.01,
            ax=ax6, square=True, cbar=False)

ax5.set_xlabel("β")
ax5.set_ylabel("α")

ax6.set_xlabel("β")
ax6.set_ylabel("α")

file_name = "論文_図3.4.3.png"
plt.tight_layout()
plt.savefig(file_name,bbox_inches="tight",dpi=200)
