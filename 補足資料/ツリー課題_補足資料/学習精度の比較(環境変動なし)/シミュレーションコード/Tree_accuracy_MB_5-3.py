import csv
import datetime
import math
import numpy as np
import time

parameter = [[i,j] for i in np.arange(0.1,1.0,0.1) for j in np.arange(0.1,1.0,0.1)]
population = 10000
trial = 100
reward_1 = 3.0
reward_2 = 5.0
sd_value = 1.0

t1 = time.time() 
dt_now = datetime.datetime.now()
print(dt_now)

data_optimal_choice = np.zeros((len(parameter), trial)).tolist()

for a in range(len(parameter)):
    alpha = parameter[a][0]
    beta = parameter[a][1]
    
    """
    populationループで使用する配列を作成
    　・人数 × 試行数（[0]で0人目の全試行）の行動選択記録
    """
    pop_action_1 = np.zeros((population, trial)).tolist()
    pop_action_2 = np.zeros((population, trial)).tolist()

    for b in range(population):

        """
        trialループで使用する配列を作成
        """
        Qmb_S0A1 = [0 for i in range(trial+1)]
        Qmb_S0A2 = [0 for i in range(trial+1)]
        Qmb_S1A1 = [0 for i in range(trial+1)]
        Qmb_S1A2 = [0 for i in range(trial+1)]
        
        action_1 = [0 for i in range(trial)]
        action_2 = [0 for i in range(trial)]
        
        for c in range(trial):                
            """
            S0からスタートして、行動選択（1回目）
            　・選択確率を計算して、A1 or A2 を選択
            　・A1選択 ⇒ S1に遷移、行動選択（2回目） ⇒ 報酬獲得
            　・A2選択 ⇒ S2に遷移、報酬獲得
            """
            s0_pA1 = 1/(1 + math.exp(-beta*(Qmb_S0A1[c]-Qmb_S0A2[c])))
            s0_pA2 = 1-s0_pA1            
            s0_choice = np.random.choice(["A1","A2"],p=[s0_pA1,s0_pA2])
            action_1[c] = s0_choice
            
            if s0_choice == "A1":
                s1_pA1 = 1/(1 + math.exp(-beta*(Qmb_S1A1[c]-Qmb_S1A2[c])))
                s1_pA2 = 1-s1_pA1
                s1_choice = np.random.choice(["A1","A2"],p=[s1_pA1,s1_pA2])
                action_2[c] = s1_choice

                if s1_choice == "A1":
                    outcome = np.random.normal(reward_1, sd_value)
                    Qmb_S0A2[c+1] = Qmb_S0A2[c]
                    Qmb_S1A2[c+1] = Qmb_S1A2[c]

                    Qmb_S1A1[c+1] = Qmb_S1A1[c]+alpha*(outcome-Qmb_S1A1[c])
                    Qmb_S0A1[c+1] = max(Qmb_S1A1[c+1],Qmb_S1A2[c+1])
                   
                if s1_choice == "A2":
                    outcome = np.random.normal(reward_2, sd_value)
                    Qmb_S0A2[c+1] = Qmb_S0A2[c]
                    Qmb_S1A1[c+1] = Qmb_S1A1[c]

                    Qmb_S1A2[c+1] = Qmb_S1A2[c]+alpha*(outcome-Qmb_S1A2[c])
                    Qmb_S0A1[c+1] = max(Qmb_S1A1[c+1],Qmb_S1A2[c+1])

            if s0_choice == "A2":
                action_2[c] = "n"

                outcome = np.random.normal(reward_1, sd_value)
                Qmb_S0A1[c+1] = Qmb_S0A1[c]
                Qmb_S1A1[c+1] = Qmb_S1A1[c]
                Qmb_S1A2[c+1] = Qmb_S1A2[c]

                Qmb_S0A2[c+1] = Qmb_S0A2[c]+alpha*(outcome-Qmb_S0A2[c])


        """
        各populationにおける、全trialの行動を記録
        　・pop_action_2[0] ⇒ あるエージェントの全trialにおける行動履歴
        """
        pop_action_1[b] = action_1
        pop_action_2[b] = action_2
        
    """
    pop_action の各列を抽出して、trial毎の、全populationの行動を取得したい
    　・リスト内包表記でリストの列を取得することができる
     ・[r[0] for r in list] ⇒ list の0列目の全要素を取得できる
     ・list[:][0] と書くと、0行目を取得してしまう
    """
    optimal_count = [[r[i] for r in pop_action_2].count("A2") for i in range(trial)]
    data_optimal_choice[a] = optimal_count

    
t2 = time.time()
elapsed_time = t2-t1
print(f"経過時間：{elapsed_time}")

with open('MB_optimal_data_5-3.csv', 'w') as file:
    writer = csv.writer(file, lineterminator='\n')
    writer.writerows(data_optimal_choice)

