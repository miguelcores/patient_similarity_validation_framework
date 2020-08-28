import pandas as pd
import json
import numpy as np

from Entities import Hpo, HpoVecs
from Common import save_object, load_object

def get_patient_embedding_average(phenotype):
    hpo = Hpo()
    hpoVecs = HpoVecs().vecs
    lenght = len(phenotype)
    suma = 0
    for symptom in phenotype:
        id = hpo.id(symptom)
        vector_id = hpoVecs[id]
        suma += vector_id
    return suma/lenght


with open('./_emu/emu-decipher_un_decimo.json') as json_file:
    patient_sims = json.load(json_file)

patients = []
for disease in patient_sims:
    for phenotype in patient_sims[disease]['sims']:
        patients.append({
         "disease-identifier": disease,
         "disease-name": patient_sims[disease]['desc'],
         "patient_embedding": get_patient_embedding_average(phenotype)
            })

save_object(patients, './_data/pruebaEmb.pkl')
