from Common import utils

translator = utils.load_object('./_data/hp-obo-translator.pkl')
# print(translator['id2name'])

objeto = utils.load_object('./_data/walks/walks.pkl')

for i in objeto:
    if i[0] == '8317':
        print([translator['id2name'][int(e)] for e in i])
