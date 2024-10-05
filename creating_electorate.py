import numpy as np
import matplotlib.pyplot as plt
import random

def create_candidates(D):
    candidate_set = np.zeros((4,D))

    w = 1
    #setting values for the centrist and two extreme candidates
    candidate_set[0] = np.random.normal(0,1,D) #centrist
    candidate_set[1] = np.random.normal(-1*w,1, D) #left wing
    candidate_set[2] = np.random.normal(w, 1, D) #right wing

    #setting values for the spikey candidate
    candidate_set[3] = np.random.normal(0, 1, D)
    dir = random.randint(0,1)*2 - 1
    candidate_set[3, D-1] = np.random.normal(w*dir, 1) #value 3 is the spike

    return candidate_set

def euclidean_distance(voter, candidate):
    sum_sq = np.sum(np.square(voter - candidate))
    return np.sqrt(np.sqrt(sum_sq))
def create_voters(D, candidates):
    electorate = np.zeros((201, D))
    electorate[:, 0] = np.random.normal(0,6,(1,201))
    for j in range(201):
        for i in range(D-1):
            electorate[j,(i+1)] = np.random.normal(0,1.4) + electorate[j,i]

    distances = np.zeros((201, 4))
    for i in range(201):
        for j in range(4):
            distances[i, j] = euclidean_distance(electorate[i], candidates[j])

    o_list = np.argsort(distances, axis = 1)

    r_max = np.mean(distances, axis = 1)


    return electorate, distances, o_list, r_max

#these functions generate strings for each file name in a consistent way
def candidate_file_name(D, j):
    return "candidates_D" + str(D) + "_C" + str(j).zfill(3) + ".csv"

def electorate_file_name(D, i, j):
    return "electorate_D" + str(D) + "_C" + str(j).zfill(3) + "_E" + str(i) + "csv"


def save_file(name, data):
        np.savetxt(name, data, delimiter=",", fmt='%f')

def make_files(D, j):
    candidates = create_candidates(D)
    #save_file(candidate_file_name(D), candidates)
    print(candidate_file_name(D, j))
    for i in range(5):
        electorate, distances, o_list, r_max = create_voters(D, candidates)
        #save_file(electorate_file_name(D, i), electorate)
        print(electorate_file_name(D,i,j))

for D in range(2,9):
    for j in range(200):
        make_files(D, j)
        print ("-------------------------")