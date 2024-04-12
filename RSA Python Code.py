import random
import math
import time

# Shared Functions: Common Mathematical Functions Used in Both the Factorization and Brute Force Approaches

def greatest_common_divisor(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def extended_euclidean_gcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        gcd, x, y = extended_euclidean_gcd(b % a, a)
        return gcd, y - (b // a) * x, x
    
def mod_inverse(a, m):
    gcd, x, _ = extended_euclidean_gcd(a, m)
    if gcd != 1:
        raise ValueError("Inverse does not exist.")
    else:
        return x % m
    

