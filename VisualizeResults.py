import time
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import auc

from Validation import ROC_AUC_EXPERIMENT

start = time.time()

EXP_ID = '22'

number_experiments = 5
exp_int = 0
source = 'orpha'
walk_length = 50
iterations = 3
conds = 150
noise_ptgs = [.15, .3, .45, .6]
patients_per_cond = 2
lamb = 4
enriched_embeddings = 'no'


sim_names = {'cos_sim', 'jaccard_best_avg', 'resnik_best_avg', 'lin_best_avg', 'jc_best_avg'}
fig, ax = plt.subplots(2, 2)
i = 0

for noise_ptg in noise_ptgs:
    aucs = {'cos_sim': [], 'jaccard_best_avg': [], 'resnik_best_avg': [], 'lin_best_avg': [], 'jc_best_avg': []}
    tprs = {'cos_sim': [], 'jaccard_best_avg': [], 'resnik_best_avg': [], 'lin_best_avg': [], 'jc_best_avg': []}
    fprs = {'cos_sim': [], 'jaccard_best_avg': [], 'resnik_best_avg': [], 'lin_best_avg': [], 'jc_best_avg': []}
    interp_tpr = {}
    mean_fpr = np.linspace(0, 1, 100)
    for exp in range(number_experiments):
        exp_id = str(exp_int)
        print('Adding results...')
        start_time_results = time.time()
        experiment = ROC_AUC_EXPERIMENT(source=source, EXP_ID=EXP_ID, exp_id=exp_id)
        experiment_metadata, tpr, fpr = experiment.return_results()
        for sim in sim_names:
            interp_tpr[sim] = np.interp(mean_fpr, fpr[sim], tpr[sim])
            interp_tpr[sim][0] = 0.0
            tprs[sim].append(interp_tpr[sim])
            aucs[sim].append(experiment_metadata[sim])

        amount_time_results = time.time() - start_time_results
        exp_int += 1

    if i == 0:
        axis = ax[i, i]
    elif i == 1:
        axis = ax[0, i]
    elif i == 2:
        axis = ax[1, 0]
    elif i == 3:
        axis = ax[1, 1]

    mean_tpr = {}
    mean_auc = {}
    std_auc = {}
    std_tpr = {}
    tprs_upper = {}
    tprs_lower = {}

    for sim in sim_names:
        mean_tpr[sim] = np.mean(tprs[sim], axis=0)
        mean_tpr[sim][-1] = 1.0
        mean_auc[sim] = auc(mean_fpr, mean_tpr[sim])
        std_auc[sim] = np.std(aucs[sim])
        std_tpr[sim] = np.std(tprs[sim], axis=0)
        tprs_upper[sim] = np.minimum(mean_tpr[sim] + std_tpr[sim], 1)
        tprs_lower[sim] = np.maximum(mean_tpr[sim] - std_tpr[sim], 0)
        axis.plot(mean_fpr, mean_tpr[sim],
                label='{} $\pm$ 1 SD (AUC = {} $\pm$ {})'.format(sim, round(mean_auc[sim], 3), round(std_auc[sim], 3)),
                lw=2, alpha=.8)
        axis.fill_between(mean_fpr, tprs_lower[sim], tprs_upper[sim], alpha=.2)#,
                        # label=r'$\pm$ 1 std. dev.')
        color = next(axis._get_lines.prop_cycler)['color']

    axis.plot([0, 1], [0, 1], linestyle='--', lw=2)
    axis.set(xlim=[-0.05, 1.05], ylim=[-0.05, 1.05],
           title="{}% as many noise terms added".format(noise_ptg*100))
    axis.legend(loc="lower right")

    i += 1

plt.show()


print(time.time()-start)


