import os
import zipfile
import glob

dirs = glob.glob(r'D:/*.zip')

def size_checker(dirs):
    '''
    '''
    total = 0
    bad_dir = []
    for dir in dirs:
        try:
            zp = zipfile.ZipFile(dir)
            size = sum([zinfo.file_size for zinfo in zp.filelist])
            #total += size
        except Exception:
            bad_dir.append(dir)
            pass
        total += size
    return(total, bad_dir)

total_size, prob_dirs = size_checker(dirs)
size_gb = total_size * 0.000000001

print(size_gb)
print(prob_dirs)
