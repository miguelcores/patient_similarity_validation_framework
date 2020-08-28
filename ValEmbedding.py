import os
import time
import json

from Validation import predict_embedding

fn = os.path.join('_emu', 'emu-orpha.json')

t0 = time.time()
preds = predict_embedding(fn, 'orpha', 2)
print(time.time() - t0)

with open('_vals/vals-emd-orpha.json', 'w') as fp:
    json.dump(preds, fp, indent=2)
