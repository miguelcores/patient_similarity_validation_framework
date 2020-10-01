'''
    THIS SCRIPT IS AN EXAMPLE OF HOW TO USE THE BOXPLOT_DATA
    CLASS TO VISUALIZE A SERIES OF EXPERIMENT RESULTS
'''


import time
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

from Validation import BOXPLOT_DATA

start = time.time()

EXP_INT = 40

number_experiments = 5
exp_int = 0
source = 'orpha'
noise_ptgs = [0, .2, .4, .6]
lambs = [0, 1, 2, 3, 4, 5]

for lamb in lambs:
    EXP_ID = str(EXP_INT)
    fig, ax = plt.subplots(2, 2)
    i = 0
    for noise_ptg in noise_ptgs:
        cos_sim_r = []
        jaccard_best_avg_r = []
        resnik_best_avg_r = []
        lin_best_avg_r = []
        jc_best_avg_r = []
        for exp in range(number_experiments):
            exp_id = str(exp_int)
            print('Adding results...')
            start_time_results = time.time()
            cos_sim, jaccard_best_avg, resnik_best_avg, lin_best_avg, jc_best_avg = \
                BOXPLOT_DATA(source='orpha', EXP_ID=EXP_ID, exp_id=exp_id).get_results()
            [cos_sim_r.append(value) for value in cos_sim]
            [jaccard_best_avg_r.append(value) for value in jaccard_best_avg]
            [resnik_best_avg_r.append(value) for value in resnik_best_avg]
            [lin_best_avg_r.append(value) for value in lin_best_avg]
            [jc_best_avg_r.append(value) for value in jc_best_avg]

            amount_time_results = time.time() - start_time_results
            exp_int += 1

        rows = []
        for j in range(len(cos_sim_r)):
            rows.append({'cos_sim': cos_sim_r[j],
                         'jaccard_best_avg': jaccard_best_avg_r[j],
                        'resnik_best_avg': resnik_best_avg_r[j],
                        'lin_best_avg': lin_best_avg_r[j],
                        'jc_best_avg': jc_best_avg_r[j]})

        data = pd.DataFrame(rows)

        if i == 0:
            axis = ax[i, i]
        elif i == 1:
            axis = ax[0, i]
        elif i == 2:
            axis = ax[1, 0]
        elif i == 3:
            axis = ax[1, 1]

        sns.violinplot(data=data, orient="h", palette="Set2", ax=axis)

        axis.set(title="Lambda={} ; {}% as many noise terms added".format(
                   lamb, noise_ptg*100)
                 )

        i += 1

    plt.show()
    EXP_INT+=1

print(time.time()-start)
