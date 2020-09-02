import os
import pandas as pd
from Common import TextParser, load_object, save_object, writeline

# '_data/hp.pkl'
# '_data/hp.obo'

class HpoParser():
    def __init__(self, fn='_data/hpo/hp.obo'):
        ext = fn[-4:].lower()
        if ext == '.obo':
            self.hpos = self.__parse(fn)
            self.__build_children(self.hpos)
        elif ext == '.pkl':
            self.hpos = load_object(fn)
        else:
            raise ValueError('Invalid file extension: Expected .obo or .pkl, found {}'.format(ext))

    def __parse(self, fn):
        with TextParser(fn) as parser:
            hpos = {}
            line = parser.next_token('[Term]')
            while line != '':
                name = parser.next_token('id:')[3:].strip()
                desc = parser.next_token('name:')[5:].strip()
                parents = []
                line = parser.next()
                while line != '\n':
                    if line.startswith('is_a:'):
                        parents.append(line[6:16])
                    line = parser.next()
                hpos[name] = {
                        'desc': desc,
                        'parents': parents,
                        'children': []
                    }
                line = parser.next_token('[Term]')
        return hpos

    def __build_children(self, hpos):
        for name in hpos:
            hpo = hpos[name]
            for parent in hpo['parents']:
                hpos[parent]['children'].append(name)

    def __getitem__(self, name):
        return self.hpos[name]

    def get_ancestors(self, items):
        parents = []
        if not isinstance(items, list):
            items = [items]
        for item in items:
            hpo = self.hpos[item]
            parents.extend(hpo['parents'])
        return parents

    def get_children(self, items):
        children = []
        if not isinstance(items, list):
            items = [items]
        for item in items:
            hpo = self.hpos[item]
            children.extend(hpo['children'])
        return children

    def get_descendants(self, item, cache=None):
        if cache is None: cache = []
        hpo = self.hpos[item]
        for name in hpo['children']:
            if not name in cache:
                cache.append(name)
                yield name
                for item in self.get_descendants(name, cache):
                    yield item

    def save_pkl(self, fn):
        save_object(self.hpos, fn)

    def save_csv(self, fn, parent=None):
        with open(fn, 'w') as file:
            writeline(file, ['Name', 'Parent', 'Desc', 'ParentDesc'])
            hpos = self.hpos
            if not parent is None:
                hpos = self.get_descendants(parent)
            for name in hpos:
                hpo = self.hpos[name]
                desc = hpo['desc']
                parents = hpo['parents']
                for par in parents:
                    par_desc = self.hpos[par]['desc']
                    writeline(file, [name, par, desc, par_desc])

    def generate_hpo2int_file(self, fn):
        with TextParser(fn) as parser:
            hpos = []
            df_cols = ['Name', 'desc', 'Id']
            i = 0
            line = parser.next_token('[Term]')
            while line != '':
                name = parser.next_token('id:')[3:].strip()
                desc = parser.next_token('name:')[5:].strip()
                hpos.append({
                        'Name': name,
                        'desc': desc,
                        'Id': i
                })
                line = parser.next_token('[Term]')
                i+=1
            hpo2int = pd.DataFrame(hpos, columns = df_cols)
            hpo2int.to_csv('./_data/hpo2int.csv', index=False)
        return


# HpoParser().generate_hpo2int_file('_data/hp.obo')
