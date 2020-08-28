import os
import json

from Tools import PatientEmulator

def generate_patients(path='_emu', count=3, ancestor_prob=0.5, noise_prob=0):
    emu = PatientEmulator(ancestor_prob=ancestor_prob, noise_prob=noise_prob)

    conds = emu.emulate_conditions('DECIPHER')
    with open(os.path.join(path, 'emu-decipher.json'), 'w') as fp:
        json.dump(conds, fp, indent=2)

    conds = emu.emulate_conditions('ORPHA')
    with open(os.path.join(path, 'emu-orpha.json'), 'w') as fp:
        json.dump(conds, fp, indent=2)

    conds = emu.emulate_conditions('OMIM')
    with open(os.path.join(path, 'emu-omim.json'), 'w') as fp:
        json.dump(conds, fp, indent=2)

generate_patients()
