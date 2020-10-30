import math
import numpy as np
import os
# calculate the normalized pupil glint vector
# Param: pupilPos -> tuple (type=int), glintPos -> tuple(type=int), IPD -> double
# Return: pgn -> tuple (type=double)
def pg_vector(pupilPos, glintPos, interPupDist=None):
    pg = pupilPos - glintPos
    if interPupDist != None:
        pgn = pg / interPupDist
        return pgn
    return pg

# calculate the IPD
# Param: position of the left and right eye -> tuple(type=int)
# Return: IPD -> double
def inter_pupil_dist(pupPosLeft, pupPosRight):
    interPupVector = pupPosRight - pupPosLeft # check if this is the right order (right>left)
    interPupDist = math.sqrt(pow(interPupDist[0],2)+pow(interPupDist[1],2))
    return interPupDist

def store_vector(storePath, posPath):
    header = "Pg-x, Pg-y"
    f = open(storePath, 'wb')
    np.savetxt(f, [], header=header)
    data = np.loadtxt(posPath)
    pupPos = data[:, :2]
    piPos = data[:, 2:]
    for i in range(len(pupPos)):
        pg = [pg_vector(pupPos[i], piPos[i])]
        print(pg)
        np.savetxt(f, pg, fmt='%.18g', delimiter=' ')
        
    f.close()

if __name__ == "__main__":
    cwd=os.getcwd()
    file='fk_cal3434_rep2'
    store_vector('pg_'+file, cwd, file)
