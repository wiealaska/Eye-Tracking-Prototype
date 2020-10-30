import os
from FK_FrameExtraction_190620 import *
from FK_EyeFeatures_020720 import *
from FK_PGVector_070520 import *

directory = input('Video directory? (entire path): ')
basename = input('Video basename? ')
files = glob.glob(directory + '/' + basename + '*.h264')
#eye = input('Which eye? left of right? ')
eyes = ('left', 'right')
#fileFormat = path.split('.')[1]
#baseName = path.split('.')[0]
#print(baseName)

# extracts frames, detectes eye features and stores the pg-vector
for file in files:
    print('Currently analized file:', file)
    convert(file)
    part = file.split('.')[0]
    frame_capture(part + '.mp4', 1)
    for eye in eyes:
        print('Currently analized eye:', eye)
        name = os.path.basename(file)
        name = name.split('.')[0]
        #print(name)
        initials, cal, rep = name.split('_')

        storeDirectory = 'C:/Users/ZVSL/Desktop/Franziska/Study2/EyeFeatures/'

        # name the final pos data file
        posFile = storeDirectory+'Positions/'+initials+'_'+cal+ '_eyemark_blur_'+eye+'_'+rep+'.dat'
        print('pos file path: ', posFile)
        # name the final pg data file
        pgFile = storeDirectory+'Vector/pg_'+initials+'_'+cal+ '_eyemark_blur_'+eye+'_'+rep+'.dat'
        print('pg file path: ', pgFile)

        searchDirectory = 'C:/Users/ZVSL/Desktop/Franziska/Study2/Frames/' + name
         
        # store pupil pos and pg pos in a .dat file
        store_pos(posFile, searchDirectory, name, eye)
        store_vector(pgFile, posFile)

