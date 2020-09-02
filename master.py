import os
from GenPatients import generate_patients
from GenSymptomEmbeddings import genEmbeddings
from MappingObjectsGenerators import gen_mapping_objects
from GenPatientEmbeddings import gen_patient_embeddings

exp_int = 0
exp_id = str(exp_int)
source = 'decipher'

print('Generating embeddings...')
genEmbeddings(input='_data/graph/hp-obo.edgelist', output='_data/emb/hp-obo_'+exp_id+'.emb')

print('Generating patients...')
generate_patients(source=source)

print('Generating patient files...')
gen_mapping_objects(source=source)

print('Generating patient embeddings...')
gen_patient_embeddings(source=source, exp_id=exp_id)

print('Generating Patient similarities...')
os.chdir('PatientSimilarities')
os.system('python -m patient_similarity --patient-file-format csv '
          '--log=INFO ../_data/patients/'+source+'_patients_phenotype.csv '
          '../_data/hpo/hp.obo ../_data/annotations/phenotype_annotation.tab '
          '../_data/patients/'+source+'_patient_embeddings.pkl '
          '../_data/patients/'+source+'_patient_sims.pkl')

