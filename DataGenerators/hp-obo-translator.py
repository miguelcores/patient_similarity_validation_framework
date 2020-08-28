import pandas as pd
from Common import utils

data = pd.read_csv('/_data/hpo2int.csv')

translator = {'name2id': {}, 'id2name': {}, 'id2desc': {}}

for i in data.Id:
    name = data[data.Id==i].Name.values[0]
    desc = data[data.Id==i].desc.values[0]
    translator['name2id'][name] = i
    translator['id2name'][i] = name
    translator['id2desc'][i] = desc

utils.save_object(translator, './_data/hp-obo-translator.pkl')
