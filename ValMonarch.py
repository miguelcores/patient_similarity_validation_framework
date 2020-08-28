import os
import time
import json

from Validation import predict_monarch

fn = os.path.join('_emu', 'emu-orpha.json')

t0 = time.time()
preds = predict_monarch(fn, 2)
print(time.time() - t0)

with open('_vals/vals-monarch-orpha.json', 'w') as fp:
    json.dump(preds, fp, indent=2)
