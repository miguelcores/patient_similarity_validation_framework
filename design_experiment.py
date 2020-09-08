import os
import time
import pandas as pd

from GenPatients import generate_patients
from GenSymptomEmbeddings import genEmbeddings
from MappingObjectsGenerators import gen_mapping_objects
from GenPatientEmbeddings import gen_patient_embeddings
from Validation import ROC_AUC_EXPERIMENT

start = time.time()

EXP_ID = '18'

number_experiments = 5
exp_int = 0
source = 'orpha'
walk_length = 50
iterations = 1
conds = 200
noise_ptgs = [.15, .3, .45, .6]
patients_per_cond = 2
lamb = 1
enriched_embeddings = 'no'

print('Generating embeddings...')
start_time_symptom_embeddings = time.time()
genEmbeddings(input='_data/graph/hp-obo.edgelist', output='_data/emb/hp-obo_'+EXP_ID+'_'+str(exp_int)+'.emb', walk_length=walk_length, iter=iterations)
amount_time_symptom_embeddings = time.time()-start_time_symptom_embeddings

rows = []

for noise_ptg in noise_ptgs:
    for exp in range(number_experiments):
        exp_id = str(exp_int)

        start_time_gen_patients = time.time()
        print('Generating patients...')
        generate_patients(source=source, conds=conds, patients_per_cond=patients_per_cond, lamb=lamb, noise_ptg=noise_ptg)
        amount_time_gen_patients = time.time()-start_time_gen_patients

        print('Generating patient files...')
        gen_mapping_objects(source=source)

        print('Generating patient embeddings...')
        start_time_patient_embeddings = time.time()
        gen_patient_embeddings(source=source, enriched=enriched_embeddings, EXP_ID=EXP_ID, exp_id=str(0))
        amount_time_patient_embeddings = time.time()-start_time_patient_embeddings

        print('Generating Patient similarities...')
        start_time_similarities = time.time()
        os.chdir('patient-similarity')
        metrics = '-s jaccard -s resnik -s lin -s jc -s cos_sim '
        os.system('python -m patient_similarity --patient-file-format csv --log=ERROR '
                  + metrics +
                  '../_data/patients/'+source+'_patients_phenotype.csv '
                  '../_data/hpo/hp.obo ../_data/annotations/phenotype_annotation.tab '
                  '../_data/patients/'+source+'_patient_embeddings.pkl '
                  '../_data/results/sims/'+source+'_patient_sims_'+EXP_ID+'_'+exp_id+'.pkl')
        amount_time_similarities = time.time() - start_time_similarities
        os.chdir('../')

        print('Adding results...')
        start_time_results = time.time()
        experiment = ROC_AUC_EXPERIMENT(source=source, EXP_ID=EXP_ID, exp_id=exp_id)
        experiment_metadata, tpr, fpr = experiment.return_results()
        amount_time_results = time.time() - start_time_results

        experiment_metadata['source'] = source
        experiment_metadata['lambda'] = lamb
        experiment_metadata['exp_id'] = exp_id
        experiment_metadata['walk_length'] = walk_length
        experiment_metadata['iterations'] = iterations
        experiment_metadata['time_similarities'] = amount_time_similarities
        experiment_metadata['time_results'] = amount_time_results
        experiment_metadata['cond_number'] = conds
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


