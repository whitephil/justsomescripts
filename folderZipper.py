import os
import glob
from zipfile import ZipFile

os.chdir('C://users/phwh9568//data//colorado_microsoft_footprints//')

folders = glob.glob('*')

# pass is here because there are other things in the folder that aren't folders
for folder in folders:
    try:
        os.chdir(folder)
        zipFolder = ZipFile(os.path.join(os.pardir,folder + '.zip'), 'w')
        files = glob.glob('*')
        for file in files:
            zipFolder.write(file)
        zipFolder.close()
        os.chdir('../')
    except:
        pass
