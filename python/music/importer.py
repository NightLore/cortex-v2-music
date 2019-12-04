from os import listdir
from os.path import isfile, join

def importFiles(paths):
    files = []
    for path in paths:
        files.append([f for f in listdir(mypath) if isfile(join(mypath, f))])
    return files


if __name__ == '__main__':
    paths = ['angry', 'excited', 'focused', 'happy',  'relaxed', 'sad']
    print(importFiles(paths))
