import os
from GenPatients import generate_patients
from GenSymptomEmbeddings import genEmbeddings
from MappingObjectsGenerators import gen_mapping_objects
from GenPatientEmbeddings import gen_patient_embeddings
from Validation import ROC_AUC_EXPERIMENT

import pandas as pd

EXP_ID = '0'

rows = []
exp_int = 0
source = 'decipher'
walk_length = [i for i in range(5, 30, 5)]

for variable in walk_length:
    exp_id = str(exp_int)

    print('Generating embeddings...')
    genEmbeddings(input='_data/graph/hp-obo.edgelist', output='_data/emb/hp-obo_'+EXP_ID+'_'+exp_id+'.emb', walk_length=variable)

    print('Generating patients...')
    generate_patients(source=source)

    print('Generating patient files...')
    gen_mapping_objects(source=source)

    print('Generating patient embeddings...')
    gen_patient_embeddings(source=source, EXP_ID=EXP_ID, exp_id=exp_id)

    print('Generating Patient similarities...')
    os.chdir('PatientSimilarities')
    os.system('python -m patient_similarity --patient-file-format csv '
              '--log=INFO -s cos_sim -s jaccard -s resnik '
              '../_data/patients/'+source+'_patients_phenotype.csv '
              '../_data/hpo/hp.obo ../_data/annotations/phenotype_annotation.tab '
              '../_data/patients/'+source+'_patient_embeddings.pkl '
              '../_data/patients/'+source+'_patient_sims.pkl')
    os.chdir('../')

    print('Adding results...')
    experiment_metadata = ROC_AUC_EXPERIMENT().return_results()
    experiment_metadata['source'] = source
    experiment_metadata['exp_id'] = exp_id
    experiment_metadata['walk_length'] = variable
    rows.append(experiment_metadata)
    exp_int += 1


df = pd.DataFrame(rows, columns=[column for column in experiment_metadata])
df.to_csv('_data/results/experiment_number_'+str(EXP_ID)+'.csv', index=False)




