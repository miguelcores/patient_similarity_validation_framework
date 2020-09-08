import os
import copy
from scipy.stats import poisson
from random import random, sample, randint

from Parsers import HpoParser, PhenotypeAnnotationsParser


class PatientEmulator():
    def __init__(self, conds=200, patients_per_cond=3, lamb=3, ancestor_prob=0.5, noise_ptg=0.5):
        self.hpos = HpoParser()
        self.anns = PhenotypeAnnotationsParser()
        self.eligibles = list(self.__build_eligibles(self.hpos, self.anns))
        self.ancestor_prob = ancestor_prob
        self.lamb = lamb
        self.conds = conds
        self.patients_per_cond = patients_per_cond
        self.noise_prob = noise_ptg

    def __build_eligibles(self, hpos, anns):
        eligibles = anns.get_hpos()
        for hpo in list(eligibles):
            for ancestor in hpos.get_ancestors_(hpo):
                eligibles.add(ancestor)
        return eligibles

    def __random_hpos(self, count):
        hpos = []
        for n in range(count):
            ix = int(random() * len(self.eligibles_now))
            hpos.append(self.eligibles_now[ix])
        return hpos

    def __random_ancestor(self, hpo, prob):
        if random() <= prob:
            ancestors = self.hpos.get_ancestors(hpo)
            ix = int(random() * len(ancestors))
            return ancestors[ix]
        return hpo

    def __poisson_ancestor(self, hpo, lamb, aux=None):
        ancestors = self.hpos.get_ancestors(hpo)
        level = poisson.rvs(mu=lamb, size=1)[0]
        hpo_root = [
            'HP:0000118', # Phenotypic Abnormality
            'HP:0000001' # All
        ]
        if aux is None:
            self.remove_ancestors_from_eligibles(ancestors)
            self.remove_descendants_from_eligibles([descendant for descendant in self.hpos.get_descendants(hpo)])
        try:
            ancestor = ancestors[level][randint(0, len(ancestors[level])-1)]
            if ancestor not in hpo_root:
                return ancestor
            else:
                return self.__poisson_ancestor(hpo, lamb, aux='1')
        except IndexError:
            ancestor = self.manage_index_error(ancestors, level)
            if ancestor not in hpo_root:
                return ancestor
            else:
                return self.__poisson_ancestor(hpo, lamb, aux='1')

    def __random_ancestors(self, hpos, prob):
        return [self.__random_ancestor(hpo, prob) for hpo in hpos]

    def __poisson_ancestors(self, hpos, lamb):
        return [self.__poisson_ancestor(hpo, lamb) for hpo in hpos]

    def get_condition(self, source, name, describe=False):
        cond = self.anns.get_source(source)[name]
        # cond = copy.copy(cond)
        if describe: cond = self.describe(cond)
        return cond

    def get_symptoms_by_frequency(self, source, name, tries):
        cond = self.get_condition(source, name)
        patient_symptoms = []
        for i, freq in enumerate(cond['freqs']):
            if freq == 'HP:0040280':    # Obligate
                patient_symptoms.append(cond['hpos'][i])
            elif freq == 'HP:0040281':  # Very frequent:
                if random() <= 0.895:    # (0.99 + 0.80) / 2
                    patient_symptoms.append(cond['hpos'][i])
            elif freq == 'HP:0040282':  # Frequent:
                if random() <= 0.545:    # (0.79 + 0.30) / 2
                    patient_symptoms.append(cond['hpos'][i])
            elif freq == 'HP:0040283':  # Occasional:
                if random() <= 0.17:     # (0.05 + 0.29) / 2
                    patient_symptoms.append(cond['hpos'][i])
            elif freq == 'HP:0040284':  # Very rare:
                if random() <= 0.025:    # (0.01 + 0.04) / 2
                    patient_symptoms.append(cond['hpos'][i])
        tries += 1
        if len(patient_symptoms) >= 3:
            return patient_symptoms
        elif tries <= 100:
            return self.get_symptoms_by_frequency(source, name, tries)
        else:
            raise ValueError('This condition must be eliminated: {}'.format(cond))

    def emulate_condition(self, source, name, describe=False):
        self.eligibles_now = self.eligibles
        cond = {}
        # hpos = self.__random_ancestors(cond['hpos'], self.ancestor_prob)
        tries = 0
        hpos = self.get_symptoms_by_frequency(source, name, tries)
        hpos = self.__poisson_ancestors(hpos, self.lamb)
        hpos.extend(self.__random_hpos(int(len(hpos) * self.noise_prob)))
        cond['hpos'] = hpos
        if describe: cond = self.describe(cond)
        return cond

    def emulate_conditions(self, source, describe=False):
        conds = {}
        names = sample([name for name in self.anns.get_source(source)], k=self.conds)
        for name in names:
            real = self.get_condition(source, name, describe=describe)
            cond = {
                    'desc': real['desc'],
                    'hpos': real['hpos'],
                    'freqs': real['freqs'],
                    'sims': []
                }
            for n in range(self.patients_per_cond):
                emul = self.emulate_condition(source, name, describe=describe)
                unique_terms_in_phenotype = list(dict.fromkeys(emul['hpos']))
                cond['sims'].append(unique_terms_in_phenotype)
            conds[name] = cond

        return conds

    def describe(self, cond):
        hpdescs = []
        for hpo in cond['hpos']:
            hpdescs.append(self.hpos[hpo]['desc'])
        cond['hpo_descs'] = hpdescs
        return cond

    def manage_index_error(self, ancestors, ix):
        try:
            return ancestors[ix-1][randint(0, len(ancestors[ix-1])-1)]
        except IndexError:
            return self.manage_index_error(ancestors, ix-1)

    def remove_ancestors_from_eligibles(self, ancestors):
        for level in ancestors:
            for ancestor in level:
                try:
                    self.eligibles_now.remove(ancestor)
                except ValueError:
                    pass

    def remove_descendants_from_eligibles(self, descendants):
        for descendant in descendants:
            try:
                self.eligibles_now.remove(descendant)
            except ValueError:
                pass
