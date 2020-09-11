import os
import pandas as pd

from Common import TextParser, load_object, save_object, writeline

# '_data/annotations.pkl'
# '_data/phenotype_annotation.tab'
class PhenotypeAnnotationsParser():
    def __init__(self, terms_to_ignore, fn='_data/annotations/phenotype_annotation.tab'):
        ext = fn[-4:].lower()
        self.terms_to_ignore = terms_to_ignore
        if ext == '.tab':
            self.__parse(fn)
        elif ext == '.pkl':
            self.load_pkl(fn)
        else:
            raise ValueError(F'Invalid file extension: Expected .obo or .pkl, found {ext}.')

    def __parse(self, fn):
        df = pd.read_csv(fn, sep='\t', low_memory=False, usecols=['#disease-db', 'reference', 'disease-name', 'HPO-ID', 'frequencyHPO'])
        df = df[~df['HPO-ID'].isin(self.terms_to_ignore)]
        self.decipher = self.__get_annotations(df[df['#disease-db'] == 'DECIPHER'])
        self.orpha = self.__get_annotations(df[df['#disease-db'] == 'ORPHA'].groupby('reference').filter(lambda x: len(x) > 12))
        self.omim = self.__get_annotations(df[df['#disease-db'] == 'OMIM'])

    def __get_annotations(self, df):
        anns = {}
        gb = df.groupby('reference')
        # print(gb)
        for name, group in gb:
            desc = group['disease-name'].values[0]
            hpos = group['HPO-ID'].tolist()
            freqs = group['frequencyHPO'].tolist()
            anns[name] = {
                    'name': name,
                    'desc': desc,
                    'hpos': hpos,
                    'freqs': freqs
                }
        return anns

    def get_source(self, source):
        source = source.upper()
        if source == 'DECIPHER': return self.decipher
        if source == 'ORPHA': return self.orpha
        if source == 'OMIM': return self.omim
        raise ValueError(F'Invalid source: Expected DECIPHER, ORPHA or OMIM. Found {source}.')

    def get_hpos(self):
        hpos = set()
        for ann in self.decipher:
            for hpo in self.decipher[ann]['hpos']:
                hpos.add(hpo)
        for ann in self.orpha:
            for hpo in self.orpha[ann]['hpos']:
                hpos.add(hpo)
        for ann in self.omim:
            for hpo in self.omim[ann]['hpos']:
                hpos.add(hpo)
        return hpos

    def load_pkl(self, fn):
        db = load_object(fn)
        self.decipher = db['decipher']
        self.orpha = db['orpha']
        self.omim = db['omim']

    def save_pkl(self, fn):
        db = {
                'decipher': self.decipher,
                'orpha': self.orpha,
                'omim': self.omim
            }
        save_object(db, fn)
