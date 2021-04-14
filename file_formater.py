
import sys
import os
from os import listdir
from os.path import isfile, join
from shutil import copyfile
from pathlib import Path

dir = sys.argv[1] #pass the video sequence path as an command line argument
ext_ = ".bmp" #change the extension here, e.g., .jpg, .jpeg, .png

files = [f for f in listdir(dir) if isfile(join(dir, f))]
extracted_files = []
indices = []

for file in files:
    raw_name, extension = os.path.splitext(file)
    if extension == ext_:
        #algorithm based on '2021-01-28 16-02-17.924_Cam 1_737_0'
        index = raw_name.split("_")[-2]
        indices.append(index)
        extracted_files.append(file)


sorted_ = [x for _, x in sorted(zip(indices, extracted_files))]

reformat_dir = Path(f"{dir}/reformatted")
os.mkdir(reformat_dir)

for index, file in enumerate(sorted_):
    file = Path(f"{dir}/{file}")
    dst = Path(f"{reformat_dir}/frame_{index}{ext_}")
    copyfile(file, dst)


print("succesfully reformated")
