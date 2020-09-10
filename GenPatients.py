import os
import json

from Tools import PatientEmulator


def generate_patients(source='orpha', path='_emu', conds=100, patients_per_cond=3, lamb=1, ancestor_prob=0.5,
                      noise_ptg=0, number_experiments_same_time=None):
    emu = PatientEmulator(conds, patients_per_cond, lamb=lamb, ancestor_prob=ancestor_prob, noise_ptg=noise_ptg)

    if source == 'decipher' or source == 'all':
        decipher_patients = emu.emulate_conditions('DECIPHER')
        with open(os.path.join(path, 'emu-decipher.json'), 'w') as fp:
            json.dump(decipher_patients, fp, indent=2)

    if source == 'orpha' or source == 'all':
        orpha_patients = emu.emulate_conditions('ORPHA')
        if number_experiments_same_time:
            with open(os.path.join(path, 'emu-orpha_'+number_experiments_same_time+'.json'), 'w') as fp:
                json.dump(orpha_patients, fp, indent=2)
        else:
            with open(os.path.join(path, 'emu-orpha.json'), 'w') as fp:
                json.dump(orpha_patients, fp, indent=2)

    if source == 'omim' or source == 'all':
        omim_patients = emu.emulate_conditions('OMIM')
        with open(os.path.join(path, 'emu-omim.json'), 'w') as fp:
            json.dump(omim_patients, fp, indent=2)

    if source == 'all':
        decipher_patients.update(orpha_patients)
        decipher_patients.update(omim_patients)
        with open(os.path.join(path, 'emu-all.json'), 'w') as fp:
            json.dump(decipher_patients, fp, indent=2)
