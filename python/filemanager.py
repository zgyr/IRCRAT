import os
import shutil

PWD = ''

def pwd():
    PWD = os.getcwd()
    return PWD

def list():
    result = []
    with os.scandir() as it:
        for entry in it:
            result.append(str(entry.is_file() + 0) + entry.name)
    return ':'.join(result)

def cd(path='.'):
    os.chdir(path)