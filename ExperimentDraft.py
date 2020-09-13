'''
    THIS SCRIPT IS AN EXAMPLE OF HOW TO USE THIS PATIENT SIMILARITY
     VALIDATION FRAMEWORK TO DESIGN SERIES OF EXPERIMENTS
'''

import os
import time
import pandas as pd

from GenPatients import generate_patients
# from GenSymptomEmbeddings import genEmbeddings
from MappingObjectsGenerators import gen_mapping_objects
from GenPatientEmbeddings import gen_patient_embeddings
from Validation import ROC_AUC_EXPERIMENT

start = time.time()

'''UNIQUE EXPERIMENT ID'''
EXP_INT = 40

'''EXPERIMENT PARAMETERS'''
# UNIQUE ID FOR EACH ITERATION
exp_int = 0
# SOURCE CAN BE ANY IN [OMIM, DECIPHER, ORPHA, ALL]
source = 'orpha'
# NUMBER OF CONDITIONS
conds = 150
patients_per_cond = 2
number_iterations = 5
# LIST OF NOISE LEVELS TO GENERATE PATIENTS
noise_ptgs = [0, .2, .4, .6]
# LIST OF IMPRECISION LAMBDAS TO GENERATE PATIENTS
lambs = [0, 1, 2, 3, 4, 5]
# ASSIGN A STRING TO THIS VARIABLE TO MAKE MULTIPLE EXPERIMENTS AT ONCE
n_same_time = None

'''NODE2VEC DEFAULT PARAMS'''
num_walks = 15
walk_length = 50
p = 1
q = .05
graph = 'hp-obo-all-under-000118-linked.edgelist'
enriched_embeddings = 'no'

""" UNCOMMENT THIS PART IF YOU WANT TO TRAIN YOUR OWN SYMPTOM EMBEDDINGS

'''GENERATE SYMPTOM EMBEDDINGS'''
print('Generating embeddings...')
start_time_symptom_embeddings = time.time()
genEmbeddings(
    input='_data/graph/'+graph, 
    output='_data/emb/hp-obo_'+int(EXP_INT)+'_'+str(exp_int)+'.emb',
    walk_length=walk_length, num_walks=num_walks
    )
amount_time_symptom_embeddings = time.time()-start_time_symptom_embeddings
"""

for lamb in lambs:
    '''DO ONE EXPERIMENT FOR EACH IMPRECISION LEVEL'''
    EXP_ID = str(EXP_INT)
    rows = []
    for noise_ptg in noise_ptgs:
        '''DO ONE SET OF ITERATIONS FOR EACH NOISE PERCENTAGE'''
        for exp in range(number_iterations):
            '''DO ONE ITERATION FOR '''
            exp_id = str(exp_int)

            '''GENERATE PATIENTS ACCORDING TO INPUT PARAMETERS'''
            start_time_gen_patients = time.time()
            print('Generating patients...')
            generate_patients(source=source, conds=conds, lamb=lamb,
                              patients_per_cond=patients_per_cond,
                              noise_ptg=noise_ptg, n_same_time=n_same_time)
            amount_time_gen_patients = time.time()-start_time_gen_patients

            '''GENERATE UNIQUE ID PER PATIENT'''
            print('Generating patient files...')
            gen_mapping_objects(source=source, n_same_time=n_same_time)

            '''COMPUTE THE AVERAGE OF ALL SYMPTOM EMBEDDINGS IN THE PHENOTYPE OF 
            THE PATIENT TO GET ONE EMBEDDING PER PATIENT'''
            print('Generating patient embeddings...')
            start_time_patient_embeddings = time.time()
            gen_patient_embeddings(source=source, EXP_ID='60',
                                   exp_id=str(0), n_same_time=n_same_time)
            amount_time_patient_embeddings = \
                time.time()-start_time_patient_embeddings

            '''COMPUTE PAIRWISE PATIENT SIMILARITY FOR EACH METRIC IN METRICS'''
            print('Generating Patient similarities...')
            start_time_similarities = time.time()
            os.chdir('patient-similarity')
            metrics = '-s jaccard -s resnik -s lin -s jc -s cos_sim '
            os.system(
                'python -m patient_similarity --patient-file-format csv '
                '--log=ERROR '
                + metrics +
                '../_data/patients/'+source+'_patients_phenotype.csv '
                '../_data/hpo/hp.obo '
                '../_data/annotations/phenotype_annotation.tab '
                '../_data/patients/'+source+'_patient_embeddings.pkl '
                '../_data/results/sims/'
                +source+'_patient_sims_'+EXP_ID+'_'+exp_id+'.pkl'
            )
            amount_time_similarities = time.time() - start_time_similarities
            os.chdir('../')

            '''SORT RESULTS BY DECREASING PATIENT SIMILARITY 
            TO COMPUTE TPR AND FPR'''
            print('Adding results...')
            start_time_results = time.time()
            experiment = ROC_AUC_EXPERIMENT(
                source=source, EXP_ID=EXP_ID,
                exp_id=exp_id, n_same_time=n_same_time
            )
            experiment_metadata, tpr, fpr = experiment.return_results()
            amount_time_results = time.time() - start_time_results

            '''GET METADATA FOR THIS ITERATION'''
            experiment_metadata['source'] = source
            experiment_metadata['lambda'] = lamb
            experiment_metadata['exp_id'] = exp_id
            experiment_metadata['walk_length'] = walk_length
            experiment_metadata['time_similarities'] = amount_time_similarities
            experiment_metadata['time_results'] = amount_time_results
            experiment_metadata['cond_number'] = conds
            experiment_metadata['noise_ptg'] = noise_ptg
            experiment_metadata['patients_per_cond'] = patients_per_cond
            experiment_metadata['time_symptom_embeddings'] = 'N/A'
            experiment_metadata['graph'] = graph
            experiment_metadata['p'] = p
            experiment_metadata['q'] = q
            experiment_metadata['num_walks'] = num_walks
            experiment_metadata['time_patient_embeddings'] = \
                amount_time_patient_embeddings
            experiment_metadata['time_gen_patients'] = amount_time_gen_patients
            experiment_metadata['enriched_embeddings'] = enriched_embeddings
            rows.append(experiment_metadata)
            exp_int += 1
    EXP_INT += 1

    '''SAVE EXPERIMENT METADATA'''
    df = pd.DataFrame(rows, columns=[column for column in experiment_metadata])
    df.to_csv('_data/results/experiment_number_'+EXP_ID+'.csv', index=False)

print(time.time()-start)


