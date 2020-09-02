import json, csv, time
from Common import save_object

def gen_mapping_objects(source):

    start = time.time()

    with open('./_emu/emu-'+source+'.json') as json_file:
        patient_sims = json.load(json_file)

    f = open('_data/patients/'+source+'_patients_phenotype.csv', 'w', newline='')
    writer = csv.writer(f)

    patients_conditions = {}
    fn = '_data/patients/'+source+'_patients_disease.pkl'
    i = 0

    for disease in patient_sims:
        for phenotype in patient_sims[disease]['sims']:
            identifier = 'P' + str(i)
            id_arr = [identifier]
            for symptom in phenotype:
                id_arr.append(symptom)
            writer.writerow(id_arr)
            patients_conditions[identifier] = disease
            i += 1

    f.close()
    save_object(patients_conditions, fn)

    print(time.time()-start)
