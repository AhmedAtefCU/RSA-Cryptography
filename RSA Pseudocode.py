# Shared Functions

function greatest_common_divisor(a, b):
    while b != 0:
        a, b = b, a % b
    return a

function extended_euclidean_gcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        gcd, x, y = extended_euclidean_gcd(b % a, a)
        return gcd, y - (b // a) * x, x

function mod_inverse(a, m):
    gcd, x, _ = extended_euclidean_gcd(a, m)
    if gcd != 1:
        raise ValueError("Inverse does not exist.")
    else:
        return x % m
    
function probable_prime_numbers(n, k=10):
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

function generate_prime(bits):
    while True:
        p = random.randint(2**(bits - 1), 2**bits - 1)
        if probable_prime_numbers(p):
            return p

function encrypt(message, public_key):
    n, e = public_key
    return pow(message, e, n)

function decrypt(ciphertext, private_key):
    n, d = private_key
    return pow(ciphertext, d, n)

# Factorization Approach Functions

function generate_keys(bits):
    if bits not in [8, 16]:
        raise ValueError("Key generation bits must be either 8 or 16.")
    
    p = generate_prime(bits // 2)
    q = generate_prime(bits // 2)
    n = p * q
    phi = (p - 1) * (q - 1)

    while True:
        e = random.randint(2, phi - 1)
        if greatest_common_divisor(e, phi) == 1:
            break

    d = mod_inverse(e, phi)
    return (n, e), (n, d)

function factorize_modulus(n):
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            p = i
            q = n // i
            break

    return p, q

# Brute Force Approach Function

function crack_private_key_brute_force(public_key):
    n, e = public_key

    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            p = i
            q = n // i
            break

    phi = (p - 1) * (q - 1)
    d = mod_inverse(e, phi)

    return (n, d)

function main():
    while True:
        print("Welcome to RSA Cryptography Program!")
        print("Choose an Approach to Find the Private Exponent in RSA: ")
        print("1. Factorization Approach")
        print("2. Brute Force Approach")
        print("3. Exit")

        approach_choice = input("Enter your Choice: ")
        
        if approach_choice == "1":
            bits = int(input("Enter the Number of Bits for Key Generation (8 or 16): "))
            if bits not in [8, 16]:
                print("Invalid Choice! Please Enter 8 or 16")
                continue
            public_key, private_key = generate_keys(bits)
            print(f"Public Key (n, e): {public_key}")
            print(f"Private Key (n, d): {private_key}")

            message = input("Enter the Message to Encrypt: ")
            ascii_codes = [ord(char) for char in message]
            encrypted_message = [encrypt(code, public_key) for code in ascii_codes]
            print(f"Encrypted Message: {encrypted_message}")

            decrypted_ascii_codes = [decrypt(code, private_key) for code in encrypted_message]
            decrypted_message = "".join([chr(code) for code in decrypted_ascii_codes])
            print(f"Decrypted Message: {decrypted_message}")
            
        elif approach_choice == "2":
            bits = int(input("Enter the Number of Bits for Key Generation (8 or 16): "))
            if bits not in [8, 16]:
                print("Invalid Choice! Please Enter 8 or 16")
                continue
            public_key, _ = generate_keys(bits)
            private_key = crack_private_key_brute_force(public_key)
            print(f"Public Key (n, e): {public_key}")
            print(f"Cracked Private Key (n, d): {private_key}")

        elif approach_choice == "3":
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

