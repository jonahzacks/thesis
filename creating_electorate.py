import numpy as np
import matplotlib.pyplot as plt
import random
D = 2


def create_candidates():
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
def create_voters():
    electorate = np.zeros((201, D))
    electorate[:, 0] = np.random.normal(0,6,(1,201))
    for j in range(201):
        for i in range(D-1):
            electorate[j,(i+1)] = np.random.normal(0,1.4) + electorate[j,i]

    distances = np.zeros((201, 4))
    candidates = create_candidates()
    for i in range(201):
        for j in range(4):
            distances[i, j] = euclidean_distance(electorate[i], candidates[j])

    o_list = np.argsort(distances, axis = 1)

    r_max = np.mean(distances, axis = 1)


    return electorate, distances, o_list, candidates, r_max

electorate, distances, o_list, candidates, r_max  = create_voters()
