import os
import time
import pandas as pd

from GenPatients import generate_patients
from GenSymptomEmbeddings import genEmbeddings
from MappingObjectsGenerators import gen_mapping_objects
from GenPatientEmbeddings import gen_patient_embeddings
from Validation import ROC_AUC_EXPERIMENT

start = time.time()

EXP_ID = '1'

rows = []
exp_int = 0
source = 'orpha'
walk_length = [i for i in range(5, 30, 5)]
conds = 100
patients_per_cond = 3

print('Generating patients...')
generate_patients(source=source, conds=conds, patients_per_cond=patients_per_cond)

print('Generating patient files...')
gen_mapping_objects(source=source)

for variable in walk_length:
    exp_id = str(exp_int)

    print('Generating embeddings...')
    genEmbeddings(input='_data/graph/hp-obo.edgelist', output='_data/emb/hp-obo_'+EXP_ID+'_'+exp_id+'.emb', walk_length=variable)

    print('Generating patient embeddings...')
    gen_patient_embeddings(source=source, EXP_ID=EXP_ID, exp_id=exp_id)

    start_time_similarities = time.time()
    print('Generating Patient similarities...')
    os.chdir('PatientSimilarities')
    os.system('python -m patient_similarity --patient-file-format csv '
              '-s jaccard -s resnik -s lin -s jc -s cos_sim '
              '../_data/patients/'+source+'_patients_phenotype.csv '
              '../_data/hpo/hp.obo ../_data/annotations/phenotype_annotation.tab '
              '../_data/patients/'+source+'_patient_embeddings.pkl '
              '../_data/patients/'+source+'_patient_sims.pkl')
    os.chdir('../')
    amount_time_similarities = time.time() - start_time_similarities

    start_time_results = time.time()
    print('Adding results...')
    experiment_metadata = ROC_AUC_EXPERIMENT().return_results()
    amount_time_results = time.time() - start_time_results

    experiment_metadata['source'] = source
    experiment_metadata['exp_id'] = exp_id
    experiment_metadata['walk_length'] = variable
    experiment_metadata['time_similarities'] = amount_time_similarities
    experiment_metadata['time_results'] = amount_time_results
    experiment_metadata['cond_number'] = conds
    experiment_metadata['patients_per_cond'] = patients_per_cond
    rows.append(experiment_metadata)
    exp_int += 1


df = pd.DataFrame(rows, columns=[column for column in experiment_metadata])
df.to_csv('_data/results/experiment_number_'+str(EXP_ID)+'.csv', index=False)

print(time.time()-start)



