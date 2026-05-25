# This is Dijkstra's algorithm using min heap for graphs represented as adjacency lists
# implemented by Ahmed Alzahrani in leisure as part of CMSC451 in Fall 2024.

# Given:
# G: a connected, undirected, weighted, simple graph with n vertices and non-negative weights
#    implemented as an adjacency list [[(a neighbor u of 0, cost of edge joining 0 and u), ...], ...]
# s: a vertex in G to be the source or initial vertex of shortest paths found by Dijkstra's algorithm.
# Return:
# D: an n-array of distances from s; D[v] = length of the shortest path from s to v.
# Pr: an n-array of predecessors that essentially stores shortest paths; Pr[v] is the
#     predecessor of v in the shortest path from s to v.
def dijkstra(G, s):
    n = len(G)
    D = [float('inf')] * n
    D[s] = 0
    Pr = [None] * n
    unexhausted_heap = MinHeap(n)
    min_unexhausted = (s, D[s])
    while min_unexhausted is not None: # for i in range(n):
        min_unexhausted = min_unexhausted[0]
        d0 = D[min_unexhausted]
        for (neighbor, cost) in G[min_unexhausted]:
            if unexhausted_heap.pos[neighbor] is not None:
                d = d0 + cost
                if d < D[neighbor]:
                    D[neighbor] = d
                    Pr[neighbor] = min_unexhausted
                    unexhausted_heap.insert((neighbor, d))
        min_unexhausted = unexhausted_heap.pop()
    return D, Pr


# Given:
# Pr: an output of a dijkstra(G, s) call with v in G such that Pr[u] is the predecessor
#     of v in the shortest path from s
# Return:
# path: a list that is a shortest path from s to v (path[0] = s, path[1], path[2], ..., path[k] = v);
#       if v is the source s, the trivial path [s] is returned.
def path_to_v(v, Pr):
    path = [v]
    pr = Pr[v]
    while pr is not None:
        path.append(pr)
        pr = Pr[pr]
    return list(reversed(path))


# Ad-hoc implementation of a min heap for Dijkstra's algorithm with the following properties:
# 0. The heap is constructed with the number n of vertices in G and an n-array pos such that
#    pos[k] for a vertex k in G is its position in heap, -1 if it hasn't been inserted, or None
#    if it has been popped (i.e., is exhausted).
# 1. Each node is a 2-tuple (vertex k in G, distance from s to k).
# 2. Insert can be used to decrease the value (distance) of an existing vertex but not increase it.
# 3. The method size() returns the number of elements in heap.
class MinHeap:
    def __init__(self, n):
        self.heap = []
        self.n = 0
        self.pos = [-1] * n

    def insert(self, kv: (int, int)):
        if kv[0] >= len(self.pos):
            raise Exception("Vertex not in the graph.")
        j = self.pos[kv[0]]
        if j == -1:
            self.heap.append(kv)
            self.n += 1
            self.pos[kv[0]] = self.n - 1
            j = self.pos[kv[0]]
        else:
            if self.heap[j][1] < kv[1]:
                raise Exception("Node update with greater distance attempted.")
            self.heap[j] = kv
        i = (j-1) // 2
        while j > 0 and self.heap[j][1] < self.heap[i][1]:
            self.pos[self.heap[i][0]] = j
            self.pos[self.heap[j][0]] = i
            x = self.heap[i]
            self.heap[i] = self.heap[j]
            self.heap[j] = x
            j = i
            i = (j-1) // 2

    def pop(self) -> (int, int):
        top = None
        if self.n > 0:
            top = self.heap[0]
            self.pos[top[0]] = None
            self.heap[0] = self.heap[self.n-1]
            self.pos[self.heap[0][0]] = 0
            self.n -= 1
            self.heap = self.heap[:self.n]
            i = 0
            j = 1
            while j < self.n:
                x = self.heap[j]
                if j+1 < self.n and self.heap[j+1][1] < x[1]:
                    j += 1
                    x = self.heap[j]
                if x[1] < self.heap[i][1]:
                    self.heap[j] = self.heap[i]
                    self.pos[self.heap[j][0]] = j
                    self.heap[i] = x
                    self.pos[x[0]] = i
                    i = j
                    j = 2*i + 1
                else:
                    break
        return top

    def size(self):
        return self.n

    def __str__(self):
        return self.heap.__str__()


# tests accurate functionality of MinHeap.
def test1():
    n = 4
    heap = MinHeap(n)
    heap.insert((0,5))
    heap.insert((2,9))
    heap.insert((1,3))
    heap.insert((3, 7))
    heap.insert((2,1))
    assert heap.size() == 4
    assert heap.pop()[0] == 2
    assert heap.size() == 3


# tests exception handling of MinHeap.
def test2():
    heap = MinHeap(1)
    try:
        heap.insert((1, 1))
        assert False
    except:
        heap.insert((0,2))
        try:
            heap.insert((0,3))
            assert False
        except:
            heap.insert((0,1))
            assert heap.pop()[1] == 1
            assert heap.size() == 0


# For this example, dijkstra(G, 0) returns the following:
# D: [0, 2, 1, 7, 10]
# Pr: [None, 0, 0, 1, 1]
def graph_example1():
    G = [[(1,2), (2, 1)],
         [(3, 5), (4,8)],
         [(1, 5), (3,8)],
         [(4, 5)],
         []]
    return G


# tests functionality of dijkstra().
def test3():
    G = graph_example1()
    D, Pr = dijkstra(G, 0)
    assert D[4] == 10


# tests functionality of path_to_v().
def test4():
    G = graph_example1()
    D, Pr = dijkstra(G, 0)
    path_to_4 = path_to_v(4, Pr)
    assert path_to_4 == [0, 1, 4]


# runs all tests.
def test():
    test1()
    test2()
    test3()
    test4()


test()