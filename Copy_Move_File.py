from shutil import copyfile
import os
import glob

os.chdir('C:\\Users\\phwh9568\\data')

folders = glob.glob('Colorado_Microsoft_Footprints\\*')

for folder in folders:
    try:
        copyfile('readme.txt', folder+'\\readme.txt')
    except:
        pass
