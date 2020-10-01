import os
import json

from Tools import PatientEmulator


def save_patients_json(objeto, path, source, n_same_time):
    if n_same_time:
        file_name = 'emu-'+source+'_'+n_same_time+'.json'
    else:
        file_name = 'emu-'+source+'.json'
    with open(os.path.join(path, file_name), 'w') as fp:
        json.dump(objeto, fp, indent=2)
    return


def generate_patients(source='orpha', path='_emu', conds=100, patients_per_cond=3, lamb=1, ancestor_prob=0.5,
                      noise_ptg=0, n_same_time=None):
    emu = PatientEmulator(conds, patients_per_cond, lamb=lamb, noise_ptg=noise_ptg)

    if source == 'decipher' or source == 'all':
        decipher_patients = emu.emulate_conditions('DECIPHER')
        save_patients_json(decipher_patients, path, source, n_same_time)

    if source == 'orpha' or source == 'all':
        orpha_patients = emu.emulate_conditions('ORPHA')
        save_patients_json(orpha_patients, path, source, n_same_time)

    if source == 'omim' or source == 'all':
        omim_patients = emu.emulate_conditions('OMIM')
        save_patients_json(omim_patients, path, source, n_same_time)

    if source == 'all':
        decipher_patients.update(orpha_patients)
        decipher_patients.update(omim_patients)
        save_patients_json(decipher_patients, path, source, n_same_time)


generate_patients(source='orpha', conds=3, patients_per_cond=2, lamb=1, noise_ptg=.3)
