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
        
def gcd(a, b):
    # Calculate the Greatest Common Divisor of two numbers 
    while b != 0:
        a, b = b, a % b
    return a

def extended_gcd(a, b):
    # Extended Euclidean Algorithm to find the modular inverse 
    if a == 0:
        return (b, 0, 1)
    else:
        gcd_val, x, y = extended_gcd(b % a, a)
        return (gcd_val, y - (b // a) * x, x)

def generate_keys(bits):
    # Generate RSA public and private keys 
    p = generate_large_prime(bits // 2)
    q = generate_large_prime(bits // 2)
    n = p * q
    phi = (p - 1) * (q - 1)
    
    while True:
        e = random.randrange(2, phi)
        if gcd(e, phi) == 1:
            break
    
    gcd_val, x, y = extended_gcd(e, phi)
    d = x % phi
    return ((e, n), (d, n))

def encrypt(message, public_key):
    # Encrypt a message using RSA 
    e, n = public_key
    encrypted_msg = [pow(ord(char), e, n) for char in message]
    return encrypted_msg