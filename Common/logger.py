import os
from datetime import datetime

class Logger():
    def __init__(self, fn='logger.log', mode='a', echo=True, header=True):
        self.file = open(fn, mode)
        self.echo = echo
        if header:
            self.file.write('\n' + str(datetime.now()) + '\n\n')

    def __call__(self, *args, sep='\t'):
        line = sep.join(str(arg) for arg in args)
        if self.echo: print(line)
        self.file.write(line + '\n')
        self.file.flush()
        
    def nl(self):
        if self.echo: print()
        self.file.write('\n')
