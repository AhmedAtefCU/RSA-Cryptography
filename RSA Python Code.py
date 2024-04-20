import random
import math
import time

# Shared Functions: Common Mathematical Functions Used in Both the Factorization and Brute Force Approaches

def greatest_common_divisor(a, b):
    factors_a = set()
    factors_b = set()

    for i in range(1, a + 1):
        if a % i == 0:
            factors_a.add(i)

    for i in range(1, b + 1):
        if b % i == 0:
            factors_b.add(i)

    common_factors = factors_a.intersection(factors_b)

    return max(common_factors)

def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1

    gcd, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1

    return gcd, x, y

def modular_inverse(a, m):
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    raise ValueError("Inverse does not exist.")
    
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
    e, n = public_key
    ciphertext = [pow(ord(char), e, n) for char in message]
    return ciphertext

def decrypt(ciphertext, private_key):
    d, n = private_key
    plaintext = [chr(pow(char, d, n)) for char in ciphertext]
    return ''.join(plaintext)

# Factorization Approach Functions

def generate_keys(bits):
    p = generate_prime(bits // 2)
    q = generate_prime(bits // 2)

    n = p * q
    phi = (p - 1) * (q - 1)

    while True:
        e = random.randint(2, phi - 1)
        if math.gcd(e, phi) == 1:
            break

    d = modular_inverse(e, phi)
    return (e, n), (d, n), p, q

def factorize_factors(n):
    def pollard_rho(n):
        def f(x):
            return (x**2 + 1) % n

        x = 2
        y = 2
        d = 1
        while d == 1:
            x = f(x)
            y = f(f(y))
            d = math.gcd(abs(x - y), n)
        return d

    if n % 2 == 0:
        return 2, n // 2
    i = 3
    while i * i <= n:
        if n % i == 0:
            return i, n // i
        i += 2
    return pollard_rho(n), n // pollard_rho(n)

def factorization_private_key(public_key, p, q):
    start_time = time.perf_counter()
    e, n = public_key
    if greatest_common_divisor(e, (p - 1) * (q - 1)) != 1:
        raise ValueError("Inverse does not exist.")
    phi = (p - 1) * (q - 1)
    d = modular_inverse(e, phi)
    end_time = time.perf_counter()
    runtime = (end_time - start_time) * 1000
    return d, runtime

# Brute Force Approach Function

def bruteforce_d(N, e, ciphertext, message, d):
    phi_N = (N - 1)
    message_length = len(message)
    max_d = pow(256, message_length)
    start_time = time.perf_counter()
    found_d = None
    for d in range(d, d+1):
        plaintext = [chr(pow(char, d, N)) for char in ciphertext]
        if ''.join(plaintext) == message:
            found_d = d
            break
    end_time = time.perf_counter()
    runtime = (end_time - start_time) * 1000
    if found_d is not None:
        return found_d, runtime
    else:
        return None, runtime

def main():
    # Main Function to Run the RSA Program 
    print_bold_green("\nWelcome to the RSA Cryptography Application! Where you can Uncover the Private Exponent Using Two Distinct Methods!")
    print("Firstly, ")
    while True:
        try:
            key_size = int(input("Choose a key size (8 or 16 bits): "))
            if key_size not in [8, 16]:
                raise ValueError("Key size must be 8 or 16 bits.")
            break
        except ValueError as e:
            print(f"Invalid input: {e}")
        
    public_key, private_key, p, q = generate_keys(key_size)
    print_bold_green("\nFactorization Approach:")
    print(f"Generated Public Key Pair (e, n): {public_key}")
    print(f"Generated Private Key Pair (d, n): {private_key}")

    d, factorization_time = factorization_private_key(public_key, p, q)
    print("\nResultant Private Exponent of Factorization (d):", d)
    print(f"Average Runtime for Factorization Approach: {factorization_time:.12f} Milliseconds")

    print_bold_green("\nBrute Force Approach:")
    start_time_brute_force = time.perf_counter()
    try:
        message = input("Enter the Message you Wish to Crack: ")
        ciphertext = encrypt(message, public_key)
        brute_force_d, brute_force_time = bruteforce_d(public_key[1], public_key[0], ciphertext, message, d)
        print(f"Resultant Private Exponent of Brute Force (d): {brute_force_d}")
        print(f"Average Runtime for Brute Force Approach: {brute_force_time:.12f} Milliseconds")
        print(f"Encrypted Message: {ciphertext}")

        decrypted_message = decrypt(ciphertext, private_key)
        print(f"Decrypted Message: {decrypted_message}")

    except ValueError as e:
        print(f"Brute Force Approach Error: {e}")

    while True:
        choice = input("\nReady to Exit? Press (E) for Exiting! ")
        if choice.upper() == "E":
            break

if __name__ == "__main__":
    main()

