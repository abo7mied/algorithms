# This is a quick implementation of Gale-Shapley Algorithm
# by Ahmed Alzahrani as part of homework 1 in CMSC451 in Fall 2024.

# Pseudocode (men-proposing)
# let all men be unengaged
# while there is an unengaged man c who has not yet made an offer to every student:
#     let s be the highest preferable woman to c whom c has not made an offer yet
#     mark that c has made an offer to s
#     if s is unengaged:
#         (c, s) are engaged
#     else:
#         if s prefers c to her current partner:
#             (c, s) are engaged

# Given:
# m: number of men
# n: number of women
# men_preferences: m by n matrix where men_preferences[i][j] is the j-th preferred woman for the i-th man
# women_preferences: n by m matrix where women_preferences[i][j] is the j-th preferred man for the i-th woman
# Return:
# matching: an array of length m representing a stable matching;
#           matching[i] is the woman engaged to the i-th man
def gale_shapley(m, n, men_preferences, women_preferences):
    # I write the men-proposing algorithm first.
    matching = [None] * m

    def get_index(item):
        index = -1
        try:
            index = matching.index(item)
        except ValueError:
            pass
        return index

    c = get_index(None)
    while c > -1:
        # pick the highest preferable woman
        k = 0
        while men_preferences[c][k] is None:
            k += 1
        s = men_preferences[c][k]
        men_preferences[c][k] = None

        c2 = get_index(s)
        if c2 == -1:
            matching[c] = s
        else:
            k2 = 0
            while k2 < m and women_preferences[s][k2] != c and women_preferences[s][k2] != c2:
                k2 += 1
            if women_preferences[s][k2] == c:
                matching[c] = s
                matching[c2] = None
        c = get_index(None)

    return matching


def test1():
    print("test1 begins...")
    # men-proposing
    print(gale_shapley(3,3,[[0,1,2], [1,0,2], [0,1,2]], [[2,1,0], [1,2,0], [1,0,2]]))
    # women-proposing
    print(gale_shapley(3,3, [[2,1,0], [1,2,0], [1,0,2]], [[0,1,2], [1,0,2], [0,1,2]]))
    print("test1 complete.")


def test():
    test1()


test()


