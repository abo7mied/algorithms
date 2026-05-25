# These are the dynamic programming algorithms
# 1. weighted interval schedule (10/22/2024)
# 2. knapsack (10/23/2024)
# 3. sequence alignment (10/24/2024)
# 4. shortest paths in graphs with possibly negative weights (10/24/2024)
# implemented by Ahmed Alzahrani in leisure in CMSC451 in Fall 2024.
import queue
import random
from datetime import datetime


# TODO: Modify so as to return not only the optimal aggregate value but also the optimal schedule
# Given:
# s: array of length n; s[j] is the start time of job j
# f: array of length n; f[j] is the finishing time of job j
# v: array of length n; v[j] (>= 0) is the value/weight of job j
# Return:
# largest aggregate weight of compatible intervals.
# 1. weighted_interval_schedule: version without memoization without p(j) pre-computation
# 2. weighted_interval_schedule2: version with memoization without p(j) pre-computation
# 3. weighted_interval_schedule3: version with memoization and p(j) pre-computation (buggy)
def weighted_interval_schedule(s, f, v):
    n = len(s) # = len(f) = len(v)
    indices = sorted([i for i in range(n)], key=f.__getitem__)
    M = [None] * n

    def p(j):
        i = j - 1
        while i >= 0 and f[indices[i]] > s[indices[j]]:
            i -= 1
        return i

    def compute_opt_j(j):
        if j == -1:
            return 0
        elif M[j] is not None:
            return M[j]
        else:
            M[j] = max(compute_opt_j(j-1), v[j] + compute_opt_j(p(j)))
            return M[j]

    return compute_opt_j(n-1)


# with memoization without p(j) pre-computation.
def weighted_interval_schedule2(s, f, v):
    n = len(s) # = len(f) = len(v)
    indices = sorted([i for i in range(n)], key=f.__getitem__)
    M = [None] * (n+1)
    M[0] = 0

    def p(j):
        i = j - 1
        while i >= 0 and f[indices[i]] > s[indices[j]]:
            i -= 1
        return i

    for i in range(1,n+1):
        M[i] = max(M[i-1], v[indices[i-1]] + M[p(i-1)+1])
    return M[n]


# TODO: Debug
def weighted_interval_schedule3(s, f, v):
    n = len(s) # = len(f) = len(v)
    indices = sorted([i for i in range(n)], key=f.__getitem__)
    M = [None] * (n+1)
    M[0] = 0
    P = [-1] * n
    ptr1 = 1
    ptr2 = 0
    indices_by_s = sorted([i for i in range(n)], key= lambda i: s[indices[i]])
    while ptr1 < n and ptr2 < n:
        if s[indices[indices_by_s[ptr1]]] <= f[indices[ptr2]]:
            P[indices_by_s[ptr1]] = ptr2 - 1
            ptr1 += 1
        else:
            ptr2 += 1
    print(s)
    print(f)
    print(indices)
    print(indices_by_s)
    print(P)

    for i in range(1,n+1):
        M[i] = max(M[i-1], v[indices[i-1]] + M[P[i-1]+1])

    return M[n]


# Given:
# weights: array of length n; weights[j] is a positive integer and the weight of item j
# constraint: a positive integer specifies the maximum aggregate weight allowed
# Return:
# maximum aggregate weight <= constraint
def knapsack(weights, constraint):
    n = len(weights)
    M = [[0 for w in range(constraint + 1)] for i in range(n+1)]
    for i in range(n):
        for w in range(constraint+1):
            if weights[i] > w:
                M[i+1][w] = M[i][w]
            else:
                M[i+1][w] = max(M[i][w], (weights[i] + M[i][w - weights[i]]))
    return M[n][constraint]


# REACHES MAXIMUM RECURSION DEPTH
# def knapsack(weights, constraint):
#     n = len(weights)
#     M = [[None] * (constraint + 1)] * n
#
#     def opt(j, bound):
#         if j == -1:
#             return 0
#         elif M[j][bound] is not None:
#             return M[j][bound]
#         else:
#             optimal = opt(j-1, bound)
#             if weights[j] <= bound:
#                 optimal = max(optimal, weights[j] + opt(j-1, bound - weights[j]))
#             return optimal
#
#     return opt(n-1, constraint)


# TODO: Modify so as to take actual characters (not restricted to labels 0, 1, .., k-1).
# TODO: Modify so that different characters may have different gap penalties.
# Given:
# mismatch_penalties: a symmetric k-by-k matrix where k is the size of the alphabet to which sequence
#                     characters belong (characters are labeled 0, 1, .., k-1 for simplicity);
#                     mismatch_penalties[i][j] = mismatch_penalties[j][i] is the penalty for
#                     (mis)matching the character with label i to a character with label j;
#                     mismatch_penalties[i][i] = 0.
# seq1: an array of length m; seq1[i-1] is the label of the ith character in the first sequence.
# seq2: an array of length n; seq2[j-1] is the label of the jth character in the second sequence.
# gap_penalty: a fixed penalty for leaving a single term unmatched (i.e., matching it to a gap).
# Return:
# minimum aggregate penalty for a valid alignment
def seq_align(seq1, seq2, mismatch_penalties, gap_penalty):
    m = len(seq1)
    n = len(seq2)
    M = [ [0 for j in range(n+1)] for i in range(m+1) ]
    for i in range(m+1):
        M[i][0] = i * gap_penalty
    for j in range(n+1):
        M[0][j] = j * gap_penalty

    for i in range(1, m+1):
        for j in range(1, n+1):
            matched = M[i-1][j-1]
            if seq1[i-1] != seq2[j-1]:
                matched += mismatch_penalties[seq1[i-1]][seq2[j-1]]
            M[i][j] = min(matched,
                          gap_penalty + min(M[i-1][j], M[i][j-1]))
    return M[m][n]


# Given:
# G: an adjacency list of a digraph of order n; G[u] is an array of neighbors (spec., successors) vi of u
#    [(v1, cost of u->v1), (v2, cost of u->v2), ...];
#    a cost is any real number, and no negative cycle exists.
# s: a vertex in G.
# t: another vertex in G.
# Return:
# length (i.e., aggregate cost) of the shortest (simple) path from s to t
def shortest_path(G, s, t):
    n = len(G)

    def opt(i, v, hitherto):
        if v == t:
            return hitherto
        elif i == 0:
            return float("inf")
        else:
            optimal = float("inf")
            for k in range(len(G[v])):
                w = G[v][k]
                optimal = min(optimal, opt(i - 1, w[0], hitherto + w[1]))
            return optimal

    return opt(n-1, s, 0) # the path is simple, for otherwise we must have a negative cycle

# DOESN'T WORK;
# assumes that the shortest path from s to t has at most as many vertices as in
# the path found by the BFS tree rooted at s (what a bad logic!)
# def shortest_path(G, s, t):
#     n = len(G)
#     visited = [-1] * n
#     q = queue.Queue()
#     q.put((s, 0))
#     visited[s] = 0
#     while not q.empty():
#         (v, l) = q.get()
#         for (neighbor, _) in G[v]:
#             if visited[neighbor] == -1:
#                 q.put((neighbor, l + 1))
#                 visited[neighbor] = l + 1
#
#     def opt(i, v, hitherto):
#         if v == t:
#             return hitherto
#         elif i == 0:
#             return float("inf")
#         else:
#             optimal = float("inf")
#             for k in range(len(G[v])):
#                 w = G[v][k]
#                 optimal = min(optimal, opt(i - 1, w[0], hitherto + w[1]))
#             return optimal
#
#     return opt(visited[s], s, 0)


def bellmanford(G, s, t):
    n = len(G)
    M = [[None for j in range(n)] for i in range(n)]
    for j in range(n):
        M[0][j] = float("inf")
    M[0][t] = 0
    for i in range(1, n):
        for v in range(n):
            optimal = M[i-1][v]
            for j in range(len(G[v])):
                (u, c_vu) = G[v][j]
                optimal = min(optimal, M[i-1][u] + c_vu)
            M[i][v] = optimal
    return M[n-1][s]


def weighted_intervals_sample():
    s = [0, 2, 4, 8]
    f = [8, 6, 5, 10]
    v = [9, 10, 8, 1]
    return s, f, v


# tests weighted_interval_schedule on a trivial set
def test1():
    assert weighted_interval_schedule([0], [3], [5]) == 5


# tests weighted_interval_schedule on a set with overlaps
def test2():
    s, f, v = weighted_intervals_sample()
    assert weighted_interval_schedule(s, f, v) == 11


# tests efficiency of weighted_interval_schedule with vs without memoization.
# n =  10
# Without:  0 seconds.
# With:  0 seconds.
# n =  100
# Without:  0 seconds.
# With:  0 seconds.
# n =  1000
# Without:  ERROR.
# With:  0 seconds.
# n =  10000
# Without:  ERROR.
# With:  1 seconds.
# n =  100000
# Without:  ERROR.
# With:  188 seconds.
# n =  1000000
# Without:  ERROR.
# With:  ERROR.
def test3():
    k = 10
    while k <= 100000:
        s = [random.randint(0, 2 * k) for i in range(k)]
        f = [random.randint(0, 2 * k) for i in range(k)]
        v = [random.randint(1, 10) for i in range(k)]
        d_without = 0
        d_with = 0
        time1 = datetime.now()
        try:
            weighted_interval_schedule(s, f, v)
            d_without = str((datetime.now() - time1).seconds) + " seconds. "
        except:
            d_without = "ERROR."
        time2 = datetime.now()
        try:
            weighted_interval_schedule2(s, f, v)
            d_with = str((datetime.now() - time2).seconds) + " seconds. "
        except:
            d_with = "ERROR."
        time3 = datetime.now()
        print("n = ", k, "\nWithout: ", d_without,
                         "\nWith: ", d_with)
        k *= 10


# tests knapsack in a few cases, including when greed doesn't conduce to optimality
def test4():
    assert knapsack([4,5,7], 10) == 9
    assert knapsack([3, 5, 7], 4) == 3
    assert knapsack([5], 100) == 5
    assert knapsack([], 10) == 0


# 10  ->  10  in  0  seconds
# 100  ->  100  in  0  seconds
# 1000  ->  1000  in  0  seconds
# 10000  ->  10000  in  15  seconds
# 100000 attempted and got MemoryError
def test5():
    for k in [10, 100, 1000, 10000]:
        weights = [i for i in range(k+1)]
        s = datetime.now()
        res = knapsack(weights, k)
        e = datetime.now()
        print(k, " -> ", res, " in ", (e - s).seconds, " seconds")


# tests the functionality of sequence alignment algorithm in the following cases:
# 1. empty sequences
# 2. an empty sequence with a nonempty sequence
# 3. distinct single-character sequences such that mismatching is worse than unmatching
# 4. distinct single-character sequences such that unmatching is worse than mismatching
# 5. random, distinct three-character sequences
def test6():
    assert seq_align([], [], [[]], 1) == 0

    assert seq_align([0], [], [[0]], 10) == 10
    assert seq_align([], [0], [[0]], 100) == 100

    assert seq_align([0], [1], [[0, 10], [10, 0]], 4) == 8

    assert seq_align([0], [1], [[0, 10], [10, 0]], 20) == 10

    x = [0, 0, 1]
    y = [2, 0, 1]
    mismatch_penalties = [[0, 2, 4],
                          [2, 0, 4],
                          [2, 2, 0]]
    assert seq_align(x, y, mismatch_penalties, 1) == 2 * 1
    assert seq_align(x, y, mismatch_penalties, 3) == mismatch_penalties[0][2]


# tests the functionality of shortest_paths with negative edge costs
def test7():
    G = [[(1, -1), (2, 50), (3, 60), (6, 100)],
         [(2, -1)],
         [(6, 10)],
         [(4, 1), (6, 30)],
         [(5, -21), (6, -20)],
         [(6, -39)],
         []]
    s = 0
    t = 6
    assert shortest_path(G, s, t) == 1
    assert bellmanford(G, s, t) == 1


# n =  10
# Bellman-Ford:  0 seconds.
# n =  100
# Bellman-Ford:  0 seconds.
# n =  1000
# Bellman-Ford:  0 seconds.
# n =  10000
# Bellman-Ford:  57 seconds.
def test8():
    k = 10
    while k <= 10000:
        G = [[((i+2) % k, random.randint(-10, 10)),
              ((i+1) % k, random.randint(-10, 10))] for i in range(k)]
        s = 0
        t = k-1
        time1 = datetime.now()
        bellmanford(G, s, t)
        time2 = datetime.now()
        print("n = ", k, "\nBellman-Ford: ", (time2-time1).seconds, "seconds.")

        k *= 10


# n =  10
# shortest_path:  0 seconds.
# (n = 100 attempted but timed out (I gave it at least 5 minutes))
# this makes sense because shortest_path doesn't store optimal values it computes;
# if 0 -> 1 <- 2, then opt(1,1) is computed more than once; that is inefficient
def test9():
    k = 10
    while k <= 10000:
        G = [[((i+2) % k, random.randint(-10, 10)),
              ((i+1) % k, random.randint(-10, 10))] for i in range(k)]
        s = 0
        t = k-1
        time1 = datetime.now()
        shortest_path(G, s, t)
        time2 = datetime.now()
        print("n = ", k, "\nshortest_path: ", (time2-time1).seconds, "seconds.")

        k *= 10


# runs all tests
def test():
    test1()
    test2()
    test3()
    test4()
    # test5() # times out
    test6()
    test7()
    test8()
    # test9() # times out


test()
