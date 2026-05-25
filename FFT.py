# This is Fast Fourier Transform algorithm for multiplying polynomials or finding convolutions
# implemented by Ahmed Alzahrani in leisure as part of CMSC451 in Fall 2024.

# PROBLEM STATEMENT
# Given 2 integer vectors of size n:
# A: (a1, a2, ..., an)
# B: (b1, b2, ..., bn)
# Return the convolution of A and B:
# C: (a1 * b1,
#     a1 * b2 + a2 * b1,
#     a1 * b3 + a2 * b2 + a3 * b1,
#     ...,
#     an * bn)

import math

from datetime import datetime
from matplotlib import pyplot as plt
import random


# Takes two vectors and returns them with the smaller padded with zeros to match the size of the larger
def zero_pad(A, B):
    n = len(A)
    m = len(B)

    if n < m:
        A += [0] * (m - n)
    else:
        B += [0] * (n - m)

    return A, B


# Find the convolution with runtime in O(n^2) using the definition.
def naive_convolution(A, B):
    A, B = zero_pad(A, B)
    n = len(A)
    n2 = 2*(n-1) + 1
    C = [0] * n2
    for i in range(n2):
        c = 0
        for j in range(max(0, i-n+1), min(i+1, n)):
            c += A[j] * B[i - j]
        C[i] = c
    return C


# TODO: Allow for non-integer real coefficients.
# Find the convolution with runtime in O(n lg n) using divide-and-conquer FFT algorithm.
# Coefficients are assumed to be integers in this implementation and real numbers in general.
# W: (2n+1)th roots of unity; W[j] = w_{2n+1}^j
# D: ( C(W[0]), C(W[1]), ..., C(W[2n]) )
def fft(A, B):
    A, B = zero_pad(A, B)
    n = len(A)
    num_roots = 2*(n-1) + 1

    W = [complex(math.cos(2 * math.pi * k / num_roots), math.sin(2 * math.pi * k / num_roots))
         for k in range(num_roots)]

    D = [eval_rec(n, A, W[k], 0, 1) * eval_rec(n, B, W[k], 0, 1) for k in range(num_roots)]

    C = [round(eval_rec(num_roots, D, W[(num_roots - k) % num_roots], 0, 1).real / num_roots) for k in range(num_roots)]

    return C


# efficient (why is eval_rec more efficient than eval_rec2?
#            do you have another way to solve the problem in eval_rec2?)
# O(lg n) for a value
def eval_rec(n, P, x, start, step):
    if start >= n:
        return 0
    elif start + step >= n:
        return P[start]
    else:
        return eval_rec(n, P, x*x, start, step*2) + x * eval_rec(n, P, x*x, start+step, step*2)


# inefficient (why? which lines?)
# O(n lgn) for a value
def eval_rec2(P, x):
    n = len(P)
    if n < 1:
        return 0
    elif n == 1:
        return P[0]
    else:
        P_even = [P[k] for k in range(0,n,2)]
        P_odd = [P[k] for k in range(1,n,2)]

        return eval_rec(P_even, x*x) + x * eval_rec(P_odd, x*x)


def time_graph(n):
    x = []
    y = []
    k = 1
    while k <= n:
        A = [2] * k
        B = [2] * k

        s = datetime.now()
        _ = fft(A, B)
        e = datetime.now()
        t = (e-s).seconds
        print(k, " : ", t, " seconds")
        x.append(k)
        y.append((e-s).seconds)
        k *= 10
    plt.scatter(x, y)
    plt.xlabel("n")
    plt.ylabel("seconds")
    plt.ylim(0, y[-1])
    plt.show()


def test1():
    A = [2,-1,3,9]
    B = [9,2,8,32]
    C = fft(A, B)
    assert C == naive_convolution(A, B)


def test():
    test1()


test()
time_graph(10000)

# output using eval_rec2:
# 1  :  0  seconds
# 10  :  0  seconds
# 100  :  0  seconds
# 1000  :  8  seconds
# 10000  :  959  seconds

# output using eval_rec:
# 1  :  0  seconds
# 10  :  0  seconds
# 100  :  0  seconds
# 1000  :  2  seconds
# 10000  :  336  seconds

