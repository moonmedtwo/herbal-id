import glob
import os

dirs = glob.glob('raw/*')

for d in dirs:
    files = glob.glob(d + '/*')
    classname = d.split('\\')[-1]
    for i,f in enumerate(files):
        out = f'out/{classname}/{i}.jpg'
        in_file = f.replace('\\', '/')
        cmd = f'cp {in_file} {out}'
        print(cmd)
        os.system(cmd)
