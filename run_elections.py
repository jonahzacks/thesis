import numpy as np
import matplotlib.pyplot as plt

#these two functions create the file names that are used to load in the CSVs where the data are stored
def candidate_file_name(D, j):
    return "candidates_D" + str(D) + "_C" + str(j).zfill(3) + ".csv"
def electorate_file_name(D, i, j):
    return "electorate_D" + str(D) + "_C" + str(j).zfill(3) + "_E" + str(i) + ".csv"
#needed to calculate the distances between voters and candidates
def euclidean_distance(voter, candidate):
    sum_sq = np.sum(np.square(voter - candidate))
    return np.sqrt(np.sqrt(sum_sq))
#calculates ditances, ordered preference lists(o_lst) and r_max for each voter
def get_vars(candidate, electorate):
    distances = np.zeros((201, 4))
    for i in range(201):
        for j in range(4):
            distances[i, j] = euclidean_distance(electorate[i], candidates[j])

    o_list = np.argsort(distances, axis = 1)

    r_max = np.mean(distances, axis = 1)

    return distances, o_list, r_max

#-------------election functions-----------------
def plurality(o_list):
    votes = np.zeros(4)
    for i in range(4):
        votes[i] = np.count_nonzero(o_list[:, 0] == i)
    return votes

def plurality_runoff(o_list):
    votes = plurality(o_list)
    first = np.argmax(votes)
    votes[first] = 0
    second = np.argmax(votes)
    runoff = [first, second]
    first_votes = np.count_nonzero(o_list[first, :] > o_list[second, :])
    second_votes = np.count_nonzero(o_list[first, :] > o_list[second, :])

    if first_votes > second_votes:
        return first
    else:
        return second

def borda(o_list):
    first = np.zeros(4)
    second = np.zeros(4)
    third = np.zeros(4)
    for i in range(4):
        first[i] = 4*np.count_nonzero(o_list[:, 0] == i)
        second[i] = 3*np.count_nonzero(o_list[:, 1] == i)
        third[i] = 2*np.count_nonzero(o_list[:, 2] == i)
    votes = np.zeros(4)
    for i in range(4):
        votes[i] = first[i] + second[i] + third[i]
    return votes

def hare(votes, num_winners=1):
    num_voters, num_candidates = votes.shape

    # Initialize vote counts for each candidate
    vote_counts = np.zeros(num_candidates, dtype=int)

    # Majority quota
    quota = num_voters // (num_winners + 1) + 1

    # Track eliminated candidates and elected candidates
    eliminated = np.zeros(num_candidates, dtype=bool)
    elected = []

    # Function to count first-preference votes for non-eliminated candidates
    def count_votes():
        vote_counts[:] = 0
        for voter_prefs in votes:
            for pref in voter_prefs:
                if not eliminated[pref - 1]:
                    vote_counts[pref - 1] += 1
                    break

    while len(elected) < num_winners:
        # Count votes based on the current first preferences
        count_votes()

        # Check if any candidate meets or exceeds the quota
        for candidate in range(num_candidates):
            if not eliminated[candidate] and vote_counts[candidate] >= quota:
                elected.append(candidate + 1)
                eliminated[candidate] = True

                # Redistribute surplus votes for elected candidate
                surplus = vote_counts[candidate] - quota
                if surplus > 0:
                    redistribute_surplus(votes, candidate, surplus)
                break
        else:
            # If no candidate meets the quota, eliminate the candidate with the fewest votes
            min_votes = np.min(vote_counts[~eliminated])
            candidate_to_eliminate = np.where(vote_counts == min_votes)[0][0]
            eliminated[candidate_to_eliminate] = True

    return elected

def coombs(votes):
    num_voters, num_candidates = votes.shape

    # Track eliminated candidates
    eliminated = np.zeros(num_candidates, dtype=bool)

    def count_first_place_votes():
        """Count first-place votes for each candidate."""
        first_place_counts = np.zeros(num_candidates, dtype=int)
        for voter_prefs in votes:
            for pref in voter_prefs:
                if not eliminated[pref - 1]:  # Only count non-eliminated candidates
                    first_place_counts[pref - 1] += 1
                    break
        return first_place_counts

    def count_last_place_votes():
        """Count last-place votes for each candidate."""
        last_place_counts = np.zeros(num_candidates, dtype=int)
        for voter_prefs in votes:
            for pref in voter_prefs[::-1]:  # Iterate from last place to first place
                if not eliminated[pref - 1]:  # Only count non-eliminated candidates
                    last_place_counts[pref - 1] += 1
                    break
        return last_place_counts

    while True:
        # Count first-place votes
        first_place_counts = count_first_place_votes()

        # Check if any candidate has a majority of first-place votes
        majority = num_voters // 2 + 1
        for candidate in range(num_candidates):
            if not eliminated[candidate] and first_place_counts[candidate] >= majority:
                return candidate + 1  # Candidate index is zero-based, so we return candidate + 1

        # No majority, find the candidate with the most last-place votes
        last_place_counts = count_last_place_votes()
        max_last_place_votes = np.max(last_place_counts[~eliminated])

        # Eliminate the candidate with the most last-place votes
        candidate_to_eliminate = np.where(last_place_counts == max_last_place_votes)[0][0]
        eliminated[candidate_to_eliminate] = True

def redistribute_surplus(votes, elected_candidate, surplus):
    # Redistribute surplus votes from the elected candidate to the next preferences
    for voter_prefs in votes:
        if voter_prefs[0] == elected_candidate + 1:
            # Change first preference to second preference
            voter_prefs = np.roll(voter_prefs, -1)

def approval(distances, r_max):
    votes = np.zeros(4)
    #new_dist = np.zeros((201, 4))
    r_max_expanded = np.outer(r_max, np.ones(4))
    new_dist = distances - r_max_expanded
    # for i in range(4):
    #     new_dist = distances[:, i] - r_max
    for i in range(4):
         votes[i] =  np.count_nonzero(new_dist[:, i] <= 0)

    return votes

def approval_runoff(distances, r_max, o_list):
    votes = approval(distances, r_max)
    first = np.argmax(votes)
    votes[first] = 0
    second = np.argmax(votes)
    runoff = [first, second]
    first_votes = np.count_nonzero(o_list[first, :] > o_list[second, :])
    second_votes = np.count_nonzero(o_list[first, :] > o_list[second, :])

    if first_votes > second_votes:
        return first
    else:
        return second
#------------------that was very long and thoroughly debugged at this point, so I don't really want to be scrolling through it-----------


def run_simulation(distances, o_list, r_max):
    win_plurality = np.argmax(plurality(o_list))
    win_plurality_runoff = plurality_runoff(o_list)
    win_borda = np.argmax(borda(o_list))
    win_approval = np.argmax(approval(distances, r_max))
    win_approval_runoff = approval_runoff(distances, r_max, o_list)
    win_hare = hare(o_list)
    win_coombs = coombs(o_list)


    return win_plurality, win_plurality_runoff, win_borda, win_approval, win_approval_runoff, win_hare[0], win_coombs

D = 8
#the number of systems I'm testing (will always be 7)
num_sys=7

#the number of candidate sets I'm testing (will be 200 in the final version, smaller for debugging)
num_candidate_sets = 200
#number of electorates per candidate (5 in the final, smaller for debugging)
num_electorates = 5
#total number of elections to be held under each system
#(for the total number of observations, multiply this number by num_sys)
num_elections=num_candidate_sets*num_electorates
results = np.empty([num_sys, num_elections])
counter = 0
for j in range(num_candidate_sets):
    candidate_file = candidate_file_name(D, j)
    candidates = np.loadtxt(candidate_file, delimiter=',')
    for i in range(num_electorates):
        electorate_file = electorate_file_name(D, i, j)
        electorate = np.loadtxt(electorate_file, delimiter=',')
        distances, o_list, r_max = get_vars(candidates, electorate)
        input = run_simulation(distances, o_list, r_max)
        results[:, counter] = input
        counter += 1

#saving the data in a csv file
np.savetxt('election_results.csv', results, delimiter=",", fmt='%f')
print("mission accomplished")
