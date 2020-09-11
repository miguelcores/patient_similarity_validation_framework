import os
import time
import pandas as pd

from GenPatients import generate_patients
from GenSymptomEmbeddings import genEmbeddings
from MappingObjectsGenerators import gen_mapping_objects
from GenPatientEmbeddings import gen_patient_embeddings
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
lambs = [0, 1, 2, 3, 4, 5]
enriched_embeddings = 'no'
num_walks_list = [10, 20]
n_same_time = str(1)
p = 1
q = .05
graph = 'hp-obo-all-under-000118-linked.edgelist'

rows = []

for lamb in lambs:
    for exp in range(number_experiments):
        start_time_gen_patients = time.time()
        print('Generating patients...')
        generate_patients(source=source, conds=conds, patients_per_cond=patients_per_cond, lamb=lamb, noise_ptg=noise_ptg,
                          n_same_time=n_same_time)
        amount_time_gen_patients = time.time()-start_time_gen_patients
        print(amount_time_gen_patients)

        print('Generating patient files...')
        gen_mapping_objects(source=source, n_same_time=n_same_time)

        for num_walks in num_walks_list:
            exp_id = str(exp_int)

            print('Generating embeddings with {} walks'.format(num_walks))
            start_time_symptom_embeddings = time.time()
            genEmbeddings(input='_data/graph/'+graph, p=p, q=q,
                          output='_data/emb/hp-obo_'+EXP_ID+'_'+exp_id+'_'+str(num_walks)+'.emb',
                          walk_length=walk_length, iter=iterations, num_walks=num_walks)
            amount_time_symptom_embeddings = time.time()-start_time_symptom_embeddings
            print('amount_time_symptom_embeddings: {}'.format(amount_time_symptom_embeddings))

            print('Generating patient embeddings...')
            start_time_patient_embeddings = time.time()
            gen_patient_embeddings(source=source, enriched=enriched_embeddings, EXP_ID=EXP_ID, exp_id=exp_id,
                                   exp_variable=str(num_walks), n_same_time=n_same_time)
            amount_time_patient_embeddings = time.time()-start_time_patient_embeddings

            print('Generating Patient similarities...')
            start_time_similarities = time.time()
            os.chdir('patient-similarity')
            metrics = '-s cos_sim ' #'-s jaccard -s resnik -s lin -s jc -s cos_sim '
            os.system('python -m patient_similarity --patient-file-format csv --log=ERROR '
                      + metrics +
                      '../_data/patients/'+source+'_patients_phenotype_'+n_same_time+'.csv '
                      '../_data/hpo/hp.obo ../_data/annotations/phenotype_annotation.tab '
                      '../_data/patients/'+source+'_patient_embeddings_'+n_same_time+'.pkl '
                      '../_data/results/sims/'+source+'_patient_sims_'+EXP_ID+'_'+exp_id+'.pkl')
            amount_time_similarities = time.time() - start_time_similarities
            os.chdir('../')

            print('Adding results...')
            start_time_results = time.time()
            experiment = ROC_AUC_EXPERIMENT(source=source, EXP_ID=EXP_ID, exp_id=exp_id, n_same_time=n_same_time)
            experiment_metadata, tpr, fpr = experiment.return_results()
            amount_time_results = time.time() - start_time_results

            experiment_metadata['source'] = source
            experiment_metadata['lambda'] = lamb
            experiment_metadata['exp_id'] = exp_id
            experiment_metadata['walk_length'] = walk_length
            experiment_metadata['iterations'] = iterations
            experiment_metadata['num_walks'] = num_walks
            experiment_metadata['p'] = p
            experiment_metadata['q'] = q
            experiment_metadata['embeddings from graph'] = graph
            experiment_metadata['number_experiments'] = number_experiments
            experiment_metadata['time_similarities'] = amount_time_similarities
            experiment_metadata['time_results'] = amount_time_results
            experiment_metadata['amount_conditions'] = conds
            experiment_metadata['noise_ptg'] = noise_ptg
            experiment_metadata['patients_per_cond'] = patients_per_cond
            experiment_metadata['time_symptom_embeddings'] = amount_time_symptom_embeddings  # 'N/A'
            experiment_metadata['time_patient_embeddings'] = amount_time_patient_embeddings
            experiment_metadata['time_gen_patients'] = amount_time_gen_patients
            experiment_metadata['enriched_embeddings'] = enriched_embeddings
            rows.append(experiment_metadata)
            exp_int += 1


df = pd.DataFrame(rows, columns=[column for column in experiment_metadata])
df.to_csv('_data/results/experiment_number_'+EXP_ID+'.csv', index=False)

print(time.time()-start)


