import pandas as pd

from Common import load_object, save_object

class AnnotationsCache():
    def __init__(self, fn='_data/annotations_cache.pkl', hpmap=None):
        ext = fn[-4:].lower()
        if ext == '.tab':
            assert not hpmap is None, 'Parameter hpmap must be set for .tab files.'
            self.__load_tab(hpmap, fn)
        elif ext == '.pkl':
            self.__load_pkl(fn)
        else:
            raise ValueError(F'Invalid file extension: Expected .csv or .pkl, found {ext}.')

    def get_source(self, source):
        source = source.upper()
        if source == 'DECIPHER': return self.decipher
        if source == 'ORPHA': return self.orpha
        if source == 'OMIM': return self.omim
        raise ValueError(F'Invalid source: Expected DECIPHER, ORPHA or OMIM. Found {source}.')

    def get_desc(self, source, id):
        source = source.upper()
        if source == 'DECIPHER': return (F'DECIPHER:{id}', self.decipher_desc[id])
        if source == 'ORPHA': return (F'ORPHA:{id}', self.orpha_desc[id])
        if source == 'OMIM': return (F'OMIM:{id}', self.omim_desc[id])
        raise ValueError(F'Invalid source: Expected DECIPHER, ORPHA or OMIM. Found {source}.')

    def __load_tab(self, hpmap, filename_tab):
        df = pd.read_csv(filename_tab, sep='\t')
        df = df[['DBReference', 'HPO', 'Name', 'Frequency']]
        self.decipher, self.decipher_desc = self.__get_annotations(hpmap, df[df['DBReference'].str.startswith('DECIPHER:')])
        self.orpha, self.orpha_desc = self.__get_annotations(hpmap, df[df['DBReference'].str.startswith('ORPHA:')])
        self.omim, self.omim_desc = self.__get_annotations(hpmap, df[df['DBReference'].str.startswith('OMIM:')])

    def __get_annotations(self, hpmap, df):
        dic = {}
        dic_desc = {}
        gb = df.groupby('DBReference')
        for name, group in gb:
            key = name[name.index(':') + 1:]
            hpos = group['HPO'].values
            hpos = hpmap.ids(hpos)
            dic[key] = hpos
            desc = group['Name'].values
            dic_desc[key] = desc[0]
        return dic, dic_desc

    def __load_pkl(self, filename_pkl):
        db = load_object(filename_pkl)
        self.decipher = db['decipher']
        self.decipher_desc = db['decipher_desc']
        self.orpha = db['orpha']
        self.orpha_desc = db['orpha_desc']
        self.omim = db['omim']
        self.omim_desc = db['omim_desc']

    def save_pkl(self, filename):
        db = {}
        db['decipher'] = self.decipher
        db['decipher_desc'] = self.decipher_desc
        db['orpha'] = self.orpha
        db['orpha_desc'] = self.orpha_desc
        db['omim'] = self.omim
        db['omim_desc'] = self.omim_desc
        save_object(db, filename)
