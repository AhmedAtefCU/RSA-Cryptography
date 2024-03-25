import random
import math

def is_prime(n):
    # Check if a number is prime 
    if n <= 1:
        return False
    elif n <= 3:
        return True
    elif n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

def generate_large_prime(bits):
    # Generate a large prime number 
    while True:
        p = random.randint(2**(bits-1), 2**bits)
        if is_prime(p):
            return p