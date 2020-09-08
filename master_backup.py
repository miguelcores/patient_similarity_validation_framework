import os
import time
import pandas as pd

import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import auc

from GenPatients import generate_patients
from GenSymptomEmbeddings import genEmbeddings
from MappingObjectsGenerators import gen_mapping_objects
from GenPatientEmbeddings import gen_patient_embeddings
from Validation import ROC_AUC_EXPERIMENT
from Common import load_object, save_object

start = time.time()

EXP_ID = '17'

number_experiments = 5
exp_int = 0
source = 'orpha'
walk_length = 50
iterations = 3
conds = 200
noise_ptgs = [.15, .3, .45, .6]
patients_per_cond = 2
lamb = 4
enriched_embeddings = 'no'

# print('Generating embeddings...')
# start_time_symptom_embeddings = time.time()
# genEmbeddings(input='_data/graph/hp-obo.edgelist', output='_data/emb/hp-obo_'+EXP_ID+'_'+str(exp_int)+'.emb', walk_length=walk_length, iter=iterations)
# amount_time_symptom_embeddings = time.time()-start_time_symptom_embeddings

rows = []
metadata_list = []
save_object(metadata_list, '_data/results/experiment_number'+EXP_ID+'.pkl')
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

        # print('Generating patients...')
        # generate_patients(source=source, conds=conds, patients_per_cond=patients_per_cond, lamb=lamb, noise_ptg=noise_ptg)
        #
        # print('Generating patient files...')
        # gen_mapping_objects(source=source)
        #
        # print('Generating patient embeddings...')
        # start_time_patient_embeddings = time.time()
        # gen_patient_embeddings(source=source, enriched=enriched_embeddings, EXP_ID=EXP_ID, exp_id=str(0))
        # amount_time_patient_embeddings = time.time()-start_time_patient_embeddings
        #
        # print('Generating Patient similarities...')
        # start_time_similarities = time.time()
        # os.chdir('patient-similarity')
        # # if exp_int == 0:
        # metrics = '-s jaccard -s resnik -s lin -s jc -s cos_sim '
        # # else:
        # #     metrics = '-s cos_sim '
        # os.system('python -m patient_similarity --patient-file-format csv --log=ERROR '
        #           + metrics +
        #           '../_data/patients/'+source+'_patients_phenotype.csv '
        #           '../_data/hpo/hp.obo ../_data/annotations/phenotype_annotation.tab '
        #           '../_data/patients/'+source+'_patient_embeddings.pkl '
        #           '../_data/results/sims/'+source+'_patient_sims_'+EXP_ID+'_'+exp_id+'.pkl')
        # amount_time_similarities = time.time() - start_time_similarities
        # os.chdir('../')

        print('Adding results...')
        start_time_results = time.time()
        experiment = ROC_AUC_EXPERIMENT(source=source, EXP_ID=EXP_ID, exp_id=exp_id)
        experiment_metadata, tpr, fpr = experiment.return_results()
        for sim in sim_names:
            interp_tpr[sim] = np.interp(mean_fpr, fpr[sim], tpr[sim])
            interp_tpr[sim][0] = 0.0
            tprs[sim].append(interp_tpr[sim])
            aucs[sim].append(experiment_metadata[sim])
        # experiment.plot_it()
        # metadata_list = load_object('_data/results/experiment_number'+EXP_ID+'.pkl')
        # metadata_list.append({noise_ptg: {'auc': experiment_metadata, 'tpr': tpr, 'fpr': fpr}})
        # save_object(metadata_list, '_data/results/experiment_number'+EXP_ID+'.pkl')

        amount_time_results = time.time() - start_time_results

        # if exp == 0:
        #     save_object(experiment_metadata, './other_sims_.pkl')
        # else:
        #     other_sims = load_object('./other_sims.pkl')
        #     other_sims.pop('cos_sim')
        #     experiment_metadata.update(other_sims)

#         experiment_metadata['source'] = source
#         experiment_metadata['lambda'] = lamb
#         experiment_metadata['exp_id'] = exp_id
#         experiment_metadata['walk_length'] = walk_length
#         experiment_metadata['iterations'] = iterations
#         experiment_metadata['time_similarities'] = amount_time_similarities
#         experiment_metadata['time_results'] = amount_time_results
#         experiment_metadata['cond_number'] = conds
#         experiment_metadata['noise_ptg'] = noise_ptg
#         experiment_metadata['patients_per_cond'] = patients_per_cond
#         experiment_metadata['time_symptom_embeddings'] = amount_time_symptom_embeddings # 'N/A'
#         experiment_metadata['time_patient_embeddings'] = amount_time_patient_embeddings
#         experiment_metadata['enriched_embeddings'] = enriched_embeddings
#         rows.append(experiment_metadata)
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

    axis.plot([0, 1], [0, 1], linestyle='--', lw=2)
    axis.set(xlim=[-0.05, 1.05], ylim=[-0.05, 1.05],
           title="{}% as many noise terms added".format(noise_ptg*100))
    axis.legend(loc="lower right")

    i += 1

plt.show()

    # tpr_cos_sim = []
    # tpr_jaccard_best_avg = []
    # tpr_jc_best_avg = []
    # tpr_lin_best_avg = []
    # tpr_resnik_best_avg = []
    # for tpr in tprs:
    #     tpr_cos_sim.append(tpr['cos_sim'])
    #     tpr_jaccard_best_avg.append(tpr['jaccard_best_avg'])
    #     tpr_jc_best_avg.append(tpr['jc_best_avg'])
    #     tpr_lin_best_avg.append(tpr['lin_best_avg'])
    #     tpr_resnik_best_avg.append(tpr['resnik_best_avg'])
    # print(np.mean(tpr_cos_sim))
# df = pd.DataFrame(rows, columns=[column for column in experiment_metadata])
# df.to_csv('_data/results/experiment_number_'+EXP_ID+'.csv', index=False)

print(time.time()-start)


