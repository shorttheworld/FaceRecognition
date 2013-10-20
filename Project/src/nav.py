import os
import shutil

if __name__ == '__main__':
    curPath = os.getcwd()
    if(('victim' in os.listdir(curPath)) == True):
        shutil.rmtree('victim')
    os.mkdir('victim')
