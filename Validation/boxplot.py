from Common import load_object

class BOXPLOT_DATA():
    def __init__(self, source, EXP_ID, exp_id, n_same_time=None):
        if n_same_time:
            fl = './_data/patients/'\
                 +source+'_patients_disease_'+n_same_time+'.pkl'
        else:
            fl = './_data/patients/'+source+'_patients_disease.pkl'

        fn = './_data/results/sims/'\
             +source+'_patient_sims_'+EXP_ID+'_'+exp_id+'.pkl'
        self.patient_similarities = load_object(fn)
        self.patients_disease = load_object(fl)

        self.cos_sim = []
        self.jaccard_best_avg = []
        self.resnik_best_avg = []
        self.lin_best_avg = []
        self.jc_best_avg = []

        self.build_patient_sim_matrix()

    def build_patient_sim_matrix(self):
        cos_sim_aux = {}
        jaccard_best_avg = {}
        resnik_best_avg = {}
        lin_best_avg = {}
        jc_best_avg = {}
        for i, patient in enumerate(self.patient_similarities):
            keys = ['P'+str(o) for o in range(0, i+1)]
            for sim in self.patient_similarities[patient]:
                try:
                    if sim == 'cos_sim':
                        self.patient_similarities[patient][sim].update(cos_sim_aux)
                        cos_sim_aux = \
                            {key: self.patient_similarities[key][sim]['P'+str(i+1)] for key in keys}
                    if sim == 'jaccard_best_avg':
                        self.patient_similarities[patient][sim].update(jaccard_best_avg)
                        jaccard_best_avg = \
                            {key: self.patient_similarities[key][sim]['P'+str(i+1)] for key in keys}
                    if sim == 'resnik_best_avg':
                        self.patient_similarities[patient][sim].update(resnik_best_avg)
                        resnik_best_avg = \
                            {key: self.patient_similarities[key][sim]['P'+str(i+1)] for key in keys}
                    if sim == 'lin_best_avg':
                        self.patient_similarities[patient][sim].update(lin_best_avg)
                        lin_best_avg = \
                            {key: self.patient_similarities[key][sim]['P'+str(i+1)] for key in keys}
                    if sim == 'jc_best_avg':
                        self.patient_similarities[patient][sim].update(jc_best_avg)
                        jc_best_avg = \
                            {key: self.patient_similarities[key][sim]['P'+str(i+1)] for key in keys}
                except KeyError:
                    pass

    def get_results(self):
        patient_similarities = self.patient_similarities
        patients_disease = self.patients_disease
        for patient in patient_similarities:
            for sim in patient_similarities[patient]:
                if sim == 'cos_sim':
                    sorted_sims = \
                        {k: v for k, v in sorted(patient_similarities[patient][sim].items(),
                                                 key=lambda item: item[1], reverse=True)}
                    for i, patient_compared in enumerate(sorted_sims):
                        if patients_disease[patient_compared] == patients_disease[patient]:
                            self.cos_sim.append(i)
                            pass
                if sim == 'jaccard_best_avg':
                    sorted_sims = \
                        {k: v for k, v in sorted(patient_similarities[patient][sim].items(),
                                                 key=lambda item: item[1], reverse=True)}
                    for i, patient_compared in enumerate(sorted_sims):
                        if patients_disease[patient_compared] == patients_disease[patient]:
                            self.jaccard_best_avg.append(i)
                            pass
                if sim == 'resnik_best_avg':
                    sorted_sims = \
                        {k: v for k, v in sorted(patient_similarities[patient][sim].items(),
                                                 key=lambda item: item[1], reverse=True)}
                    for i, patient_compared in enumerate(sorted_sims):
                        if patients_disease[patient_compared] == patients_disease[patient]:
                            self.resnik_best_avg.append(i)
                            pass
                if sim == 'lin_best_avg':
                    sorted_sims = \
                        {k: v for k, v in sorted(patient_similarities[patient][sim].items(),
                                                 key=lambda item: item[1], reverse=True)}
                    for i, patient_compared in enumerate(sorted_sims):
                        if patients_disease[patient_compared] == patients_disease[patient]:
                            self.lin_best_avg.append(i)
                            pass
                if sim == 'jc_best_avg':
                    sorted_sims = \
                        {k: v for k, v in sorted(patient_similarities[patient][sim].items(),
                                                 key=lambda item: item[1], reverse=True)}
                    for i, patient_compared in enumerate(sorted_sims):
                        if patients_disease[patient_compared] == patients_disease[patient]:
                            self.jc_best_avg.append(i)
                            pass

        return self.cos_sim, self.jaccard_best_avg, \
               self.resnik_best_avg, self.lin_best_avg,\
               self.jc_best_avg



