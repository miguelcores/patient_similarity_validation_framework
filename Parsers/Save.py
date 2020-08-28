from Parsers import HpoParser, PhenotypeAnnotationsParser

hpos = HpoParser('_resources/hp.obo')
hpos.save_pkl('_data/hp.pkl')

anns = PhenotypeAnnotationsParser('_resources/phenotype_annotation.tab')
anns.save_pkl('_data/annotations.pkl')
