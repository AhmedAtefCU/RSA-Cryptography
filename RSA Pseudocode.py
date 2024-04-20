import random
import math
import time

function print_bold_green(text):
    print text in bold and green

function greatest_common_divisor(a, b):
    factors_a = set()
    factors_b = set()
    for i in range(1, a + 1):
        if a % i == 0:
            add i to factors_a
    for i in range(1, b + 1):
        if b % i == 0:
            add i to factors_b
    common_factors = intersection of factors_a and factors_b
    return maximum value in common_factors

function generate_prime(bits):
    while True:
        p = random integer between 2^(bits-1) and 2^bits - 1
        if p is prime:
            return p

function is_prime(n, k=5):
    if n <= 3:
        return n == 2 or n == 3
    if n is even:
        return False
    r, s = 0, n - 1
    while s is even:
        increment r by 1
        divide s by 2
    repeat k times:
        choose a random integer a between 2 and n - 2
        compute x as a^s mod n
        if x is 1 or x is n - 1:
            continue to next iteration
        repeat r - 1 times:
            compute x as x^2 mod n
            if x is n - 1:
                break out of loop
        if x is not n - 1:
            return False
    return True

function modular_inverse(a, m):
    for x in range(1, m):
        if (a * x) mod m is 1:
            return x
    raise ValueError("Inverse does not exist.")

function extended_gcd(a, b):
    if a is 0:
        return b, 0, 1
    gcd, x1, y1 = extended_gcd(b mod a, a)
    x = y1 - (b div a) * x1
    y = x1
    return gcd, x, y

function generate_keys(bits):
    p = generate_prime(bits / 2)
    q = generate_prime(bits / 2)
    n = p * q
    phi = (p - 1) * (q - 1)
    while True:
        e = random integer between 2 and phi - 1
        if gcd(e, phi) is 1:
            break
    d = modular_inverse(e, phi)
    return (e, n), (d, n), p, q

function encrypt(message, public_key):
    e, n = public_key
    ciphertext = [char^e mod n for char in message]
    return ciphertext

function decrypt(ciphertext, private_key):
    d, n = private_key
    plaintext = [char^d mod n for char in ciphertext]
    return join(plaintext)

function factorize_factors(n):
    function pollard_rho(n):
        function f(x):
            return (x^2 + 1) mod n
        x = 2
        y = 2
        d = 1
        while d is 1:
            x = f(x)
            y = f(f(y))
            d = gcd(abs(x - y), n)
        return d
    if n is even:
        return 2, n / 2
    i = 3
    while i^2 <= n:
        if n mod i is 0:
            return i, n / i
        increment i by 2
    return pollard_rho(n), n / pollard_rho(n)

function factorization_private_key(public_key, p, q):
    start_time = current time
    e, n = public_key
    if gcd(e, (p - 1) * (q - 1)) is not 1:
        raise ValueError("Inverse does not exist.")
    phi = (p - 1) * (q - 1)
    d = modular_inverse(e, phi)
    end_time = current time
    runtime = (end_time - start_time) * 1000
    return d, runtime

function bruteforce_d(N, e, ciphertext, message, d):
    phi_N = (N - 1)
    message_length = length of message
    max_d = 256^message_length
    start_time = current time
    found_d = None
    for d in range(d, d+1):
        plaintext = [char^d mod N for char in ciphertext]
        if join(plaintext) is message:
            found_d = d
            break
    end_time = current time
    runtime = (end_time - start_time) * 1000
    if found_d is not None:
        return found_d, runtime
    else:
        return None, runtime

function main():
    print_bold_green("\nWelcome to the RSA Cryptography Application! Where you can Uncover the Private Exponent Using Two Distinct Methods!")
    print("Firstly, ")
    while True:
        try:
            key_size = input("Choose a key size (8 or 16 bits): ")
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
    start_time_brute_force = current time
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
