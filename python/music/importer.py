from os import listdir
from os.path import isfile, join
import random

def importFiles(paths):
    files = []
    for path in paths:
        files.append([f for f in listdir(path) if isfile(join(path, f))])
    return files

def getRandom(files):
    return files[random.randrange(len(files))]
    

if __name__ == '__main__':
    paths = ['angry', 'excited', 'focused', 'happy',  'relaxed', 'sad']
    print(importFiles(paths))
