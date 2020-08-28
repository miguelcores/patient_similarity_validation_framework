import os

class TextParser():
    def __init__(self, filename):
        self.filename = filename

    def __enter__(self):
        self.file = open(self.filename, 'r')
        return self

    def next(self):
        return self.file.readline()

    def next_token(self, token):
        line = self.next()
        while line != '' and not line.startswith(token):
            line = self.next()
        return line

    def __exit__(self, type, value, traceback):
        self.file.close()
