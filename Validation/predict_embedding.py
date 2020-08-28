import os
import json

from Entities import Hpo, HpoVecs, AnnotationsCache

class EmbeddingSim():
    def __init__(self):
        self.hpo = Hpo()
        self.vec = HpoVecs()
        self.anns = AnnotationsCache()
        print(self.anns)

    def score(self, source, hpos, limit=10):
        vec = self.vec
        anns = self.anns
        hpos = self.hpo.ids(hpos)
        conds = anns.get_source(source)

        scores = []
        for name in conds:
            ann = conds[name]
            if len(ann) > 0:
                score = vec.calc_score(hpos, ann)
                scores.append([score, name])

        preds = []
        for p in sorted(scores)[:limit]:
            name = anns
            preds.append([round(p[0], 2), *anns.get_desc(source, p[1])])

        results = []
        rank = 0
        last = -1
        for pred in sorted(preds):
            score = pred[0]
            if score > last:
                rank += 1
                last = score
            results.append([rank] + pred)
        return results


class EmbeddingPredictions():
    def __init__(self):
        self.emdsim = EmbeddingSim()
        self.conditions = {}

    def predict(self, source, hpos, top=10):
        score = self.emdsim.score(source, hpos, limit=top)
        for s in score:
            self.conditions[s[2]] = s[3]
        return [{ 'r': int(s[0]), 's': s[1], 'x': s[2] } for s in score]

    def predict_emu(self, source, name, cond):
        desc = cond['desc']
        hpos = cond['hpos']
        sims = cond['sims']
        return {
                'name': name,
                'desc': desc,
                'real': hpos,
                'sims': sims,
                'pred_real': self.predict(source, hpos, 5),
                'pred_sims': [self.predict(source, hps) for hps in sims]
            }

def predict_embedding(fn, source, count):
    emd = EmbeddingPredictions()
    with open(fn, 'r') as fp:
        conds = json.load(fp)
    preds = []
    n = 0
    for name in conds:
        if n >= count: break
        cond = conds[name]
        sz = len(cond['hpos'])
        if sz >= 4 and sz <= 16:
            rank = emd.predict_emu(source, name, cond)
            preds.append(rank)
            n += 1
    report = {
            'preds': preds,
            'conds': emd.conditions
        }
    return report

