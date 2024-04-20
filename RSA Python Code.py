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

def crack_private_key_brute_force(public_key):
    # Attempts to Crack the Private Key Using a Brute Force Approach 
    n, e = public_key

    start_time = time.perf_counter()  # Record Start Time

    p, q = None, None
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            p = i
            q = n // i
            break

    phi = (p - 1) * (q - 1)
    d = mod_inverse(e, phi)

    end_time = time.perf_counter()  # Record End Time
    runtime = end_time - start_time  # Calculate Runtime

    return (n, d), runtime

def main():
    # Main Function to Run the RSA Encryption Program 
    while True:
        print("Welcome to RSA Cryptography Program!")
        print("Choose an Approach to Find the Private Exponent in RSA: ")
        print("1. Factorization Approach")
        print("2. Brute Force Approach")
        print("3. Exit")

        approach_choice = input("Enter your Choice: ")
        
        if approach_choice == "1":
            # Factorization Approach
            print("\nFactorization Approach Chosen\n")
            bits = int(input("Enter the Number of Bits for Key Generation (8 or 16): "))
            if bits not in [8, 16]:
                print("Invalid Choice! Please Enter 8 or 16")
                continue
            public_key, private_key = generate_keys(bits)
            print(f"Public Key (n, e): {public_key}")
            print(f"Private Key (n, d): {private_key}\n")

            message = input("Enter the Message to Encrypt: ")
            ascii_codes = [ord(char) for char in message]
            encrypted_message = [encrypt(code, public_key) for code in ascii_codes]
            print(f"Encrypted Message: {encrypted_message}\n")

            decrypted_ascii_codes = [decrypt(code, private_key) for code in encrypted_message]
            decrypted_message = "".join([chr(code) for code in decrypted_ascii_codes])
            print(f"Decrypted Message: {decrypted_message}\n")

            # Calculate Runtime For Factorization
            _, _, runtime = factorize_modulus(public_key[0])
            print(f"Runtime for Factorizing Modulus: {runtime:.6f} Seconds\n")
            
        elif approach_choice == "2":
            # Brute Force Approach
            print("\nBrute Force Approach Chosen\n")
            bits = int(input("Enter the Number of Bits for Key Generation (8 or 16): "))
            if bits not in [8, 16]:
                print("Invalid Choice! Please Enter 8 or 16")
                continue
            public_key, _ = generate_keys(bits)
            private_key, runtime = crack_private_key_brute_force(public_key)
            print(f"Public Key (n, e): {public_key}")
            print(f"Cracked Private Key (n, d): {private_key}")
            print(f"Runtime for Cracking Private Key: {runtime:.6f} Seconds\n")

        elif approach_choice == "3":
            # Exit
            print("\nExiting the Program")
            break

        else:
            print("\nInvalid Choice! Please Enter a Valid Option.\n")
            
        choice = input("\nWould You Like to Exit (E) or Restart (R) the Program? ")
        if choice.upper() == "E":
            print("Exiting the Program")
            break
        
if __name__ == "__main__":
    main()
    
