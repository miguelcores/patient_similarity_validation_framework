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

def gen_patient_embeddings(source, exp_id):
    start = time.time()

    with open('./_data/patients/'+source+'_patients_phenotype.csv') as csv_file:
        patient_sims = csv.reader(csv_file)
        hpo = Hpo()
        hpo_vectors = HpoVecs(exp_id).vecs
        patients = {}
        for line in patient_sims:
            patients[line[0]] = compute_embedding_average(line[1:], hpo, hpo_vectors)

    save_object(patients, './_data/patients/'+source+'_patient_embeddings.pkl')

    print(time.time()-start)
