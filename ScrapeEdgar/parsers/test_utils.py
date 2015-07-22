import os

def load_file_contents(name):
    path = os.path.realpath(__file__)
    f = open(os.path.join(os.path.dirname(path), name), "r")
    contents = f.read()
    f.close()
    return contents