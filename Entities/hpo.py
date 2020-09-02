from Common import load_object

class Hpo():
    def __init__(self, fn='_data/hpo/hp-obo-translator.pkl'):
        self.__load_pkl(fn)

    def __load_pkl(self, fn_pkl):
        db = load_object(fn_pkl)
        self.name2id = db['name2id']
        self.id2name = db['id2name']
        self.id2desc = db['id2desc']

    def exists(self, name):
        return name in self.name2id

    def filter_exists(self, names):
        return list(filter(lambda x: self.exists(x), names))

    def id(self, name):
        return self.name2id[name]

    def ids(self, names):
        return [self.id(name) for name in self.filter_exists(names)]

    def name(self, id):
        return self.id2name[id]

    def names(self, ids):
        return [self.name(id) for id in ids]

    def desc(self, id):
        return self.id2desc[id]

    def all_ids(self):
        return self.id2name.keys()
