from sklearn.metrics import roc_curve, roc_auc_score
import matplotlib.pyplot as plt

from Common import load_object


class ROC_AUC_EXPERIMENT():
    def __init__(self, source, EXP_ID, exp_id):
        fn = './_data/results/sims/'+source+'_patient_sims_'+EXP_ID+'_'+exp_id+'.pkl'
        # print(fn)
        fl = './_data/patients/'+source+'_patients_disease.pkl'
        self.patient_similarities = load_object(fn)
        self.patients_disease = load_object(fl)

        self.y = []

        self.sim_names = {'cos_sim', 'jaccard_best_avg', 'resnik_best_avg', 'lin_best_avg', 'jc_best_avg'}
        self.fpr = {}
        self.tpr = {}
        self.thresholds = {}
        self.roc_auc = {}
        self.cos_sim = []
        self.jaccard_best_avg = []
        self.resnik_best_avg = []
        self.lin_best_avg = []
        self.jc_best_avg = []

        self.x = len(self.patient_similarities)
        self.z = self.x-1
        """  Why is m = x*z / 2 instead of z*z/2  ??????
        """
        self.m = self.x*self.z/2

        self.get_results()

    def plot_it(self):
        plt.figure()
        lw = 2

        for sim in self.sim_names:
            plt.plot(self.fpr[sim], self.tpr[sim],
                     lw=lw, label='ROC curve for {} (area = {})'.format(sim, round(self.roc_auc[sim], 3)))

        plt.plot([0, 1], [0, 1], color='navy', lw=lw, linestyle='--')
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title('Receiver operating characteristic')
        plt.legend(loc="lower right")
        plt.show()

    def load_results(self, sim_name, sim_array):
        if self.m != (len(sim_array)+1): return
        else:
            self.fpr[sim_name], self.tpr[sim_name], self.thresholds[sim_name] = roc_curve(self.y, sim_array)
            self.roc_auc[sim_name] = roc_auc_score(self.y, sim_array)

    def append_similarity_score(self, score_array, score_dict):
        for patient_compared in score_dict:
            score_array.append(score_dict[patient_compared])
        return score_array

    def get_results(self):
        patient_similarities = self.patient_similarities
        patients_disease = self.patients_disease
        for patient in patient_similarities:
            for sim in patient_similarities[patient]:
                if sim == 'cos_sim':
                    for patient_compared in patient_similarities[patient][sim]:
                        self.cos_sim.append(patient_similarities[patient][sim][patient_compared])
                        if patients_disease[patient_compared] == patients_disease[patient]:
                            self.y.append(1)
                        else:
                            self.y.append(0)
                    self.load_results(sim, self.cos_sim)
                if sim == 'jaccard_best_avg':
                    self.jaccard_best_avg = self.append_similarity_score(self.jaccard_best_avg, patient_similarities[patient][sim])
                    self.load_results(sim, self.jaccard_best_avg)
                if sim == 'resnik_best_avg':
                    self.resnik_best_avg = self.append_similarity_score(self.resnik_best_avg, patient_similarities[patient][sim])
                    self.load_results(sim, self.resnik_best_avg)
                if sim == 'lin_best_avg':
                    self.lin_best_avg = self.append_similarity_score(self.lin_best_avg, patient_similarities[patient][sim])
                    self.load_results(sim, self.lin_best_avg)
                if sim == 'jc_best_avg':
                    self.jc_best_avg = self.append_similarity_score(self.jc_best_avg, patient_similarities[patient][sim])
                    self.load_results(sim, self.jc_best_avg)

    def return_results(self):
        return self.roc_auc, self.tpr, self.fpr
