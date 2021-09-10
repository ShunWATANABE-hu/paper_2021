import csv
import datetime
import math
import numpy as np
import time

parameter = [[i,j] for i in np.arange(0.1,1.0,0.1) for j in np.arange(0.1,1.0,0.1)]
population = 10000
trial = 100
reward_1 = 5.0
reward_2 = 3.0
sd_value = 1.0
lambda_value = 0.5
state_p1 = 0.5
state_p2 = 1-state_p1

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
        Qmf_S1A1 = [0 for i in range(trial+1)]
        Qmf_S1A2 = [0 for i in range(trial+1)]
        Qmf_S2A3 = [0 for i in range(trial+1)]
        Qmf_S2A4 = [0 for i in range(trial+1)]
        Qmf_S3A5 = [0 for i in range(trial+1)]
        Qmf_S4A6 = [0 for i in range(trial+1)]
        
        action_1 = [0 for i in range(trial)]
        action_2 = [0 for i in range(trial)]
        
        for c in range(trial):                
            state_1 = np.random.choice(["S1","S2"],p=[state_p1,state_p2])

            if state_1 == "S1":
                s1_pA1 = 1/(1 + math.exp(-beta*(Qmf_S1A1[c]-Qmf_S1A2[c])))
                s1_pA2 = 1-s1_pA1            
                s1_choice = np.random.choice(["A1","A2"],p=[s1_pA1,s1_pA2])

                if s1_choice == "A1":
                    Qmf_S1A1[c] = Qmf_S1A1[c] + alpha*(Qmf_S3A5[c]-Qmf_S1A1[c])

                    outcome = np.random.normal(reward_1, sd_value)

                    Qmf_S1A2[c+1] = Qmf_S1A2[c] 
                    Qmf_S2A3[c+1] = Qmf_S2A3[c]
                    Qmf_S2A4[c+1] = Qmf_S2A4[c]
                    Qmf_S4A6[c+1] = Qmf_S4A6[c]
                   
                    Qmf_S3A5[c+1] = Qmf_S3A5[c] + alpha*(outcome-Qmf_S3A5[c]) 
                    Qmf_S1A1[c+1] = Qmf_S1A1[c] + alpha*lambda_value*(outcome-Qmf_S1A1[c])

                    action_1[c] = s1_choice
                    action_2[c] = "A5"
                  
                if s1_choice == "A2":
                    Qmf_S1A2[c] = Qmf_S1A2[c] + alpha*(Qmf_S4A6[c]-Qmf_S1A2[c])

                    outcome = np.random.normal(reward_2, sd_value)

                    Qmf_S1A1[c+1] = Qmf_S1A1[c] 
                    Qmf_S2A3[c+1] = Qmf_S2A3[c]
                    Qmf_S2A4[c+1] = Qmf_S2A4[c]
                    Qmf_S3A5[c+1] = Qmf_S3A5[c]
                   
                    Qmf_S4A6[c+1] = Qmf_S4A6[c] + alpha*(outcome-Qmf_S4A6[c]) 
                    Qmf_S1A2[c+1] = Qmf_S1A2[c] + alpha*lambda_value*(outcome-Qmf_S1A2[c])

                    action_1[c] = s1_choice
                    action_2[c] = "A6"
                
            if state_1 == "S2":
                s2_pA3 = 1/(1 + math.exp(-beta*(Qmf_S2A3[c]-Qmf_S2A4[c])))
                s2_pA4 = 1-s2_pA3            
                s2_choice = np.random.choice(["A3","A4"],p=[s2_pA3,s2_pA4])
               
                if s2_choice == "A3":
                    Qmf_S2A3[c] = Qmf_S2A3[c] + alpha*(Qmf_S3A5[c]-Qmf_S2A3[c])

                    outcome = np.random.normal(reward_1, sd_value)

                    Qmf_S1A1[c+1] = Qmf_S1A1[c] 
                    Qmf_S1A2[c+1] = Qmf_S1A2[c] 
                    Qmf_S2A4[c+1] = Qmf_S2A4[c]
                    Qmf_S4A6[c+1] = Qmf_S4A6[c]
                   
                    Qmf_S3A5[c+1] = Qmf_S3A5[c] + alpha*(outcome-Qmf_S3A5[c]) 
                    Qmf_S2A3[c+1] = Qmf_S2A3[c] + alpha*lambda_value*(outcome-Qmf_S2A3[c])

                    action_1[c] = s2_choice
                    action_2[c] = "A5"
                    
                if s2_choice == "A4":
                    Qmf_S2A4[c] = Qmf_S2A4[c] + alpha*(Qmf_S4A6[c]-Qmf_S2A4[c])

                    outcome = np.random.normal(reward_2, sd_value)

                    Qmf_S1A1[c+1] = Qmf_S1A1[c] 
                    Qmf_S1A2[c+1] = Qmf_S1A2[c] 
                    Qmf_S2A3[c+1] = Qmf_S2A3[c]
                    Qmf_S3A5[c+1] = Qmf_S3A5[c]
                  
                    Qmf_S4A6[c+1] = Qmf_S4A6[c] + alpha*(outcome-Qmf_S4A6[c]) 
                    Qmf_S2A4[c+1] = Qmf_S2A4[c] + alpha*lambda_value*(outcome-Qmf_S2A4[c])

                    action_1[c] = s2_choice
                    action_2[c] = "A6"

        """
        各trialにおける、全populationの行動を記録
        """
        pop_action_1[b] = action_1
        pop_action_2[b] = action_2
        
    """
    pop_action の各列を抽出して、trial毎の、全populationの行動を取得したい
    　・リスト内包表記でリストの列を取得することができる
     ・[r[0] for r in list] ⇒ list の0列目の全要素を取得できる
     ・list[:][0] と書くと、0行目を取得してしまう
    """
    optimal_count = [[r[i] for r in pop_action_2].count("A5") for i in range(trial)]
    data_optimal_choice[a] = optimal_count


    
t2 = time.time()
elapsed_time = t2-t1
print(f"経過時間：{elapsed_time}")

with open('MF_optimal_data_5-3.csv', 'w') as file:
    writer = csv.writer(file, lineterminator='\n')
    writer.writerows(data_optimal_choice)

