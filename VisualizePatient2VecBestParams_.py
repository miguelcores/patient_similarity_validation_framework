import time
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import auc

from Validation import ROC_AUC_EXPERIMENT

start = time.time()

EXP_ID = '27'

number_experiments = 3
exp_int = 0
source = 'orpha'
walk_length = 50
iterations = 1
conds = 200
noise_ptg = 0 #[0, .2, .4, .6]
patients_per_cond = 2
lambs = [0, 1, 2, 3]#, 3, 4, 5]
enriched_embeddings = 'no'
num_walks_list = [10, 20]#, 30]
n_same_time = str(1)


sim_names = {'cos_sim_10', 'cos_sim_20'}
fig, ax = plt.subplots(2, 2)
i = 0

for lamb in lambs:
    aucs = {'cos_sim_10': [], 'cos_sim_20': []}
    tprs = {'cos_sim_10': [], 'cos_sim_20': []}
    fprs = {'cos_sim_10': [], 'cos_sim_20': []}
    interp_tpr = {}
    mean_fpr = np.linspace(0, 1, 100)
    for exp in range(number_experiments):
        experiment_metadata_ = {'cos_sim_10': {}, 'cos_sim_20': {}}
        tpr_ = {'cos_sim_10': {}, 'cos_sim_20': {}}
        fpr_ = {'cos_sim_10': {}, 'cos_sim_20': {}}
        for num_walks in num_walks_list:
            exp_id = str(exp_int)
            print('Adding results...')
            start_time_results = time.time()
            experiment = ROC_AUC_EXPERIMENT(source=source, EXP_ID=EXP_ID, exp_id=exp_id, n_same_time=n_same_time)
            experiment_metadata, tpr, fpr = experiment.return_results()
            experiment_metadata_['cos_sim_'+str(num_walks)] = experiment_metadata['cos_sim']
            tpr_['cos_sim_'+str(num_walks)] = tpr['cos_sim']
            fpr_['cos_sim_'+str(num_walks)] = fpr['cos_sim']
            exp_int += 1

        for sim in sim_names:
            interp_tpr[sim] = np.interp(mean_fpr, fpr_[sim], tpr_[sim])
            interp_tpr[sim][0] = 0.0
            tprs[sim].append(interp_tpr[sim])
            aucs[sim].append(experiment_metadata_[sim])

        amount_time_results = time.time() - start_time_results

    if i == 0:
        axis = ax[i, i]
    elif i == 1:
        axis = ax[0, i]
    elif i == 2:
        axis = ax[1, 0]
    elif i == 3:
        axis = ax[1, 1]
    # elif i == 4:
    #     axis = ax[2, 0]
    # elif i == 5:
    #     axis = ax[2, 1]

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
        # color = next(ax._get_lines.prop_cycler)['color']

    axis.plot([0, 1], [0, 1], linestyle='--', lw=2)
    axis.set(xlim=[-0.05, 1.05], ylim=[-0.05, 1.05],
           title="Lambda={} ; {}% as many noise terms added".format(lamb, noise_ptg*100))
    axis.legend(loc="lower right")

    i += 1

plt.show()


print(time.time()-start)


