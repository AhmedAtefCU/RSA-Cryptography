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
    
def probable_prime_numbers(n, k=10):
    # Checks if a Number is a Probable Prime Using the Miller-Rabin Primality Test 
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False

    r, s = 0, n - 1
    while s % 2 == 0:
        r += 1
        s //= 2

    for _ in range(k):
        a = random.randint(2, n - 2)
        x = pow(a, s, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

def generate_prime(bits):
    # Generates a Prime Number of Specified Bit Length 
    while True:
        p = random.randint(2**(bits - 1), 2**bits - 1)
        if probable_prime_numbers(p):
            return p

def encrypt(message, public_key):
    # Encrypts a Message Using the RSA Encryption Algorithm 
    n, e = public_key
    return pow(message, e, n)

def decrypt(ciphertext, private_key):
    # Decrypts a Ciphertext Using the RSA Decryption Algorithm 
    n, d = private_key
    return pow(ciphertext, d, n)

