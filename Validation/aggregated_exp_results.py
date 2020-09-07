from sklearn.metrics import roc_curve, roc_auc_score
import matplotlib.pyplot as plt

from Common import load_object


class ROC_AUC_EXPERIMENT():
    def __init__(self, source, EXP_ID, exp_id):
        fn = './_data/results/sims/'+source+'_patient_sims_'+EXP_ID+'_'+exp_id+'.pkl'
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


EXP_ID = '16'

object = load_object('_data/results/experiment_number'+EXP_ID+'.pkl')

# print(object[0])

for i, row in enumerate(object):
    # print(row)
    for variable in row:
        # print(variable)
        for result in row[variable]:
            print(result)





















