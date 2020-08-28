import json
import pickle

def R2(v): return "{:n}".format(v) if type(v) is int else "{:4.2f}".format(v)
def R4(v): return "{:n}".format(v) if type(v) is int else "{:6.4f}".format(v)
def R6(v): return "{:n}".format(v) if type(v) is int else "{:8.6f}".format(v)

def load_object(fn):
    with open(fn, 'rb') as file:
        return pickle.load(file)

def save_object(obj, fn):
    with open(fn, 'wb') as file:
        pickle.dump(obj, file)

def save_json(obj, fn):
    with open(fn, 'w') as file:
        json.dump(obj, file)

def save_text(txt, fn):
    with open(fn, 'w') as file:
        file.write(txt)

def writeline(file, args, sep='\t'):
    line = sep.join([str(r) for r in args])
    file.write(line + '\n')
