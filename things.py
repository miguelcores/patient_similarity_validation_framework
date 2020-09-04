from Common import utils

# translator = utils.load_object('./_data/hp-obo-translator.pkl')
# # print(translator['id2name'])
#
# objeto = utils.load_object('./_data/walks/walks.pkl')
#
# for i in objeto:
#     if i[0] == '8317':
#         print([translator['id2name'][int(e)] for e in i])

# objeto = utils.load_object('./_data/patients/decipher_patient_sims.pkl')
# print(objeto)

from Validation import ROC_AUC_EXPERIMENT

ROC_AUC_EXPERIMENT('orpha').plot_it()
# import json
#
# with open('_emu/emu-decipher-sample.json', 'r') as file:
#     decipher = json.load(file)
#
# with open('_emu/emu-orpha-sample.json', 'r') as file:
#     orpha = json.load(file)
#
# orpha.update(decipher)
#
# with open('_emu/emu-all-sample.json', 'w') as file:
#     json.dump(orpha, file, indent=2)
