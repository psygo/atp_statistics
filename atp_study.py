import json
import numpy as np
import matplotlib.pyplot as plt

# Opening the Data
N = 1500
date = '2018-08-27'
name = 'atp_python_' + date + '_1-' + str(N) + '.json'

with open(name) as d:
    players = [json.loads(line) for line in d]


# Getting the Usable Data
study = []

for i in range(0, len(players)):
    if 'height' in players[i].keys():
        if 'weight' in players[i].keys():
            if 'prize' in players[i].keys():
                rank = i + 1
                height = players[i]['height']
                weight = players[i]['weight']
                prize = players[i]['prize']

                # Taking out the weird zeros
                if height >= 50 and weight >= 50:
                    study.append([rank, height, weight, prize])

# Prize vs Rank

# With the filthy rich
prize = [i/10**6 for _,_,_,i in study]
weight = [j for _,_,j,_ in study]
rank = [k for k,_,_,_ in study]

plt.scatter(rank, prize, color = ['blue'])
plt.xlabel('Rank')
plt.ylabel('Prize (US\$) ($10^{-6}$)')
plt.title('Prize x Rank')
plt.savefig('prize_vs_rank_with_rich.jpeg')
plt.close()

# Getting the filthy rich out
cap = 40*10**6
study_NFR = [[i,j,k,l] for i,j,k,l in study if l < cap]

prize = [i/10**6 for _,_,_,i in study_NFR]
weight = [j for _,_,j,_ in study_NFR]
rank = [k for k,_,_,_ in study_NFR]

plt.scatter(rank, prize, color = ['blue'])
plt.xlabel('Rank')
plt.ylabel('Prize (US\$) ($10^{-6}$)')
plt.title('Prize x Rank')
plt.savefig('prize_vs_rank.jpeg')
plt.close()

# Sum of Prizes vs Rank

def prize_sum(n):
    prize_sum = 0
    for i in range(0, n+1):
        prize_sum += study[i][3]
    return prize_sum

def find_player_sum(percentile, prize_list):
    for i in range(0, len(prize_list)):
        if prize_list[i] >= percentile*prize_list[-1]:
            return i
    return i

prize_sum_all = []
for i in range(0,len(study)):
    prize_sum_all.append(prize_sum(i))

cap_99 = 0.99*prize_sum_all[-1]
player_99 = find_player_sum(0.99, prize_sum_all)
cap_95 = 0.95*prize_sum_all[-1]
player_95 = find_player_sum(0.95, prize_sum_all)
cap_50 = 0.50*prize_sum_all[-1]
player_50 = find_player_sum(0.5, prize_sum_all)

rank = [k for k,_,_,_ in study]

main_curve = plt.scatter(rank, prize_sum_all, color = ['blue'], \
                         label = 'Prizes x Rank')
curve_99 = plt.axhline(y = cap_99, label = f'99%, \
                       player = {player_99}')
curve_95 = plt.axhline(y = cap_95, label = f'95%, \
                       player = {player_95}', color = 'y')
curve_50 = plt.axhline(y = cap_50, label = f'50%, \
                       player = {player_50}', color = 'r')
plt.legend(handles = [main_curve, curve_99, curve_95, curve_50])
plt.xlabel('Rank')
plt.ylabel('Sum of Prizes (Billion US$)')
plt.title(f'Sum of Prizes x Rank (Total Sum = {round(prize_sum_all[-1]/10**9,2)} billion)')
plt.savefig('sum_prize_vs_rank.jpeg')
plt.close()

# Histogram of Weight and Height

height = [i for _,i,_,_ in study]
weight = [j for _,_,j,_ in study]
rank = [k for k,_,_,_ in study]

n_bins = 20

height_hist = plt.hist(height, bins = n_bins, color = ['blue'], label = 'Height')
weight_hist = plt.hist(weight, bins = n_bins, color = ['orange'], label = 'Weight')
# plt.legend(handles = [height_hist, weight_hist])
plt.title('Histograms of Weight and Height')
plt.xlabel('Weight (orange/left) and Height (blue/right)')
plt.ylabel('Number of Players')
plt.savefig('histogram_weight_height.jpeg')
plt.close()

# Scatter of Weight and Height

height = [i for _,i,_,_ in study]
weight = [j for _,_,j,_ in study]
rank = [k for k,_,_,_ in study]

plt.scatter(height, weight, color = ['blue'])
plt.xlabel('Height (cm)')
plt.ylabel('Weight (kg)')
plt.title('Scatter of Weight x Height')
plt.savefig('scatter_weight_height.jpeg')
plt.close()

# Scatter of Weight and Height with Millionaires

big_prize = 1*10**6

height_M = [i for _,i,_,k in study if k >= big_prize]
weight_M = [i for _,_,i,k in study if k >= big_prize]

height_NM = [i for _,i,_,k in study if k < big_prize]
weight_NM = [i for _,_,i,k in study if k < big_prize]

labels = ['>1M' if k >= 10**6 else '<1M' for _,_,_,k in study]

millionaires = plt.scatter(height_M, weight_M, color = ['red'],
                           marker = ',', label = 'Millionaires')
n_millionaires = plt.scatter(height_NM, weight_NM, color = ['blue'],
                             marker = '.', label = 'Non-millionaires')
plt.legend(handles = [millionaires, n_millionaires])
plt.xlabel('Height (cm)')
plt.ylabel('Weight (kg)')
plt.title('Scatter of Weight x Height')
plt.savefig('scatter_weight_height_millionaires.jpeg')
plt.close()

# 2D Histogram of Weight and Height

fig, ax = plt.subplots(tight_layout=True)
hist = ax.hist2d(height_M, weight_M)
plt.title('2D Histogram of Weight x Height')
plt.xlabel('Height')
plt.ylabel('Weight')
plt.savefig('2D_histogram_weight_height.jpeg')
plt.close()
