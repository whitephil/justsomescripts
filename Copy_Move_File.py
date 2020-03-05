from shutil import copyfile
import os
import glob

os.chdir('C:\\Users\\phwh9568\\data')

copyfile('readme.txt', 'Colorado_Microsoft_Footprints\\readme.txt')

folders = glob.glob('Colorado_Microsoft_Footprints\\*')

for folder in folders:
    try:
        copyfile('readme.txt', folder+'\\readme.txt')
    except:
        pass
