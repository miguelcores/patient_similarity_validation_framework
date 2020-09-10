import csv, time

from Entities import Hpo, HpoVecs
from Common import save_object

def compute_embedding_average(phenotype, hpo, hpo_vectors):
    lenght = len(phenotype)
    suma = 0
    for symptom in phenotype:
        hpo_id = hpo.id(symptom)
        vector_id = hpo_vectors[hpo_id]
        suma += vector_id
    return suma/lenght

def gen_patient_embeddings(source, enriched, EXP_ID, exp_id, n_same_time=None, exp_variable=None):
    start = time.time()

    if n_same_time:
        patients_phenotypes = './_data/patients/'+source+'_patients_phenotype_'+n_same_time+'.csv'
        patient_embeddings = './_data/patients/'+source+'_patient_embeddings_'+n_same_time+'.pkl'
    else:
        patients_phenotypes = './_data/patients/'+source+'_patients_phenotype.csv'
        patient_embeddings = './_data/patients/'+source+'_patient_embeddings.pkl'

    with open(patients_phenotypes) as csv_file:
        patient_sims = csv.reader(csv_file)
        hpo = Hpo()
        hpo_vectors = HpoVecs(enriched, EXP_ID, exp_id, exp_variable=exp_variable).vecs
        patients = {}
        for line in patient_sims:
            patients[line[0]] = compute_embedding_average(line[1:], hpo, hpo_vectors)

    save_object(patients, patient_embeddings)

    print(time.time()-start)
