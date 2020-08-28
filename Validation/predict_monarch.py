import os
import json
import requests

BASE_URI = 'https://api.monarchinitiative.org'

METRICS = ['phenodigm', 'jaccard', 'simGIC', 'resnik', 'symmetric_resnik']

class MonarchSim():
    def __init__(self, base_uri=BASE_URI):
        self.base_uri = BASE_URI

    def search(self, hpos, metric='phenodigm', limit=10):
        params = {
            'id': hpos,
            'metric': metric,
            'limit': limit
        }
        resp = requests.get(self.base_uri + '/api/sim/search', params=params)
        assert resp.status_code == 200, resp.status_code
        return resp

    def score(self, hpos, metric='phenodigm', limit=10):
        resp = self.search(hpos, metric=metric, limit=limit)
        results = []
        for match in resp.json()['matches']:
            results.append([match['rank'], match['score'], match['id'], match['label']])
        return results

class MonarchPredictions():
    def __init__(self, base_uri=BASE_URI):
        self.simsearch = MonarchSim(base_uri)
        self.conditions = {}

    def predict(self, hpos, top=10):
        score = self.simsearch.score(hpos, limit=top)
        for s in score:
            self.conditions[s[2]] = s[3]
        return [{ 'r': int(s[0]), 's': s[1], 'x': s[2] } for s in score]

    def predict_emu(self, name, cond):
        desc = cond['desc']
        hpos = cond['hpos']
        sims = cond['sims']
        return {
                'name': name,
                'desc': desc,
                'real': hpos,
                'sims': sims,
                'pred_real': self.predict(hpos, 5),
                'pred_sims': [self.predict(hps) for hps in sims]
            }

def predict_monarch(fn, count):
    mon = MonarchPredictions()
    with open(fn, 'r') as fp:
        conds = json.load(fp)
    preds = []
    n = 0
    for name in conds:
        if n >= count: break
        cond = conds[name]
        sz = len(cond['hpos'])
        if sz >= 4 and sz <= 16:
            rank = mon.predict_emu(name, cond)
            preds.append(rank)
            n += 1
    report = {
            'preds': preds,
            'conds': mon.conditions
        }
    return report
