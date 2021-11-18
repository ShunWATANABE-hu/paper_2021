import csv
import datetime
import math
import numpy as np
import time


parameter = [[i,j] for i in np.arange(0.1,1.0,0.1) for j in np.arange(0.1,1.0,0.1)]
population = 10000
trial = 100
reward_1 = 0.0
reward_2 = 3.0
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
    pop_stpair = np.zeros((population, trial)).tolist()

    for b in range(population):
        """
        trialループで使用する配列を作成
        """
        Qmb_S0A1 = [0 for i in range(trial+1)]
        Qmb_S0A2 = [0 for i in range(trial+1)]
        Qmb_S1A1 = [0 for i in range(trial+1)]
        Qmb_S1A2 = [0 for i in range(trial+1)]
        
        action_record = [0 for i in range(trial)]
        

        """ S0からスタートして、行動選択（1回目） """
        for c in range(trial): 
            s0_pA1 = 1/(1 + math.exp(-beta*(Qmb_S0A1[c]-Qmb_S0A2[c])))
            s0_pA2 = 1-s0_pA1            
            s0_choice = np.random.choice(["A1","A2"],p=[s0_pA1,s0_pA2])
            action_1 = "S0" + s0_choice

            """ S0A1の場合は、S1に遷移して行動選択（2回目） """
            if s0_choice == "A1":               
                s1_pA1 = 1/(1 + math.exp(-beta*(Qmb_S1A1[c]-Qmb_S1A2[c])))
                s1_pA2 = 1-s1_pA1
                s1_choice = np.random.choice(["A1","A2"],p=[s1_pA1,s1_pA2])
                action_2 = "S1" + s1_choice

                """ S1A1の場合_S0A1→S1A1 """                    
                if s1_choice == "A1":
                
                    if c < (trial/2):
                        outcome = np.random.normal(reward_1, sd_value)
                    if c >= (trial/2):
                        outcome = np.random.normal(reward_2, sd_value)
                    
                    Qmb_S0A2[c+1] = Qmb_S0A2[c]
                    Qmb_S1A2[c+1] = Qmb_S1A2[c]
                    
                    Qmb_S1A1[c+1] = Qmb_S1A1[c]+alpha*(outcome-Qmb_S1A1[c])
                    Qmb_S0A1[c+1] = max(Qmb_S1A1[c+1],Qmb_S1A2[c+1])
                    action_record[c] = action_1 + action_2
                      
                """ S1A2の場合_S0A1→S1A2 """
                if s1_choice == "A2":
                
                    if c < (trial/2):
                        outcome = np.random.normal(reward_2, sd_value)
                    if c >= (trial/2):
                        outcome = np.random.normal(reward_1, sd_value)
                    
                    Qmb_S0A2[c+1] = Qmb_S0A2[c]
                    Qmb_S1A1[c+1] = Qmb_S1A1[c]
                    
                    Qmb_S1A2[c+1] = Qmb_S1A2[c]+alpha*(outcome-Qmb_S1A2[c])
                    Qmb_S0A1[c+1] = max(Qmb_S1A1[c+1],Qmb_S1A2[c+1])
                    action_record[c] = action_1 + action_2


            """ S0A2の場合は、S2に遷移して終了 """
            if s0_choice == "A2":               
                s2_action = "--"
                action_2 = "S2" + s2_action
                 
                outcome = np.random.normal(reward_1, sd_value)
                 
                Qmb_S0A1[c+1] = Qmb_S0A1[c]
                Qmb_S1A1[c+1] = Qmb_S1A1[c]
                Qmb_S1A2[c+1] = Qmb_S1A2[c]
                
                Qmb_S0A2[c+1] = Qmb_S0A2[c]+alpha*(outcome-Qmb_S0A2[c])              
                action_record[c] = action_1 + action_2

        """
        pop_stpair → pop * trialのリスト
        pop_stpair[i] → ある1人の、全trialの行動履歴
        """
        pop_stpair[b] = action_record

       
    """
    pop_stpairの列：1試行ごとの全popの行動履歴
        listの列を取得する → [r[i] for r in list]
        ※list[:][0] と書くと、0行目を取得してしまう
    """
    optimal_count1 = [[r[i] for r in pop_stpair].count("S0A1S1A2") for i in range(int(trial/2))]
    optimal_count2 = [[r[i] for r in pop_stpair].count("S0A1S1A1") for i in range(int(trial/2), trial, 1)]
      
    data_optimal_choice[a] = optimal_count1 + optimal_count2
    
t2 = time.time()
elapsed_time = t2-t1
print(f"経過時間：{elapsed_time}")

with open('MBtreeR_data_3-0.csv', 'w') as file:
    writer = csv.writer(file, lineterminator='\n')
    writer.writerows(data_optimal_choice)
