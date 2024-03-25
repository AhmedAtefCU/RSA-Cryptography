function is_prime(n):
    if n <= 1:
        return False
    else if n <= 3:
        return True
    else if n is divisible by 2 or 3:
        return False
    i = 5
    while i * i <= n:
        if n is divisible by i or n is divisible by (i + 2):
            return False
        i += 6
    return True

function generate_large_prime(bits):
    while True:
        p = random integer between 2^(bits-1) and 2^bits
        if is_prime(p):
            return p

function gcd(a, b):
    while b is not 0:
        a, b = b, a % b
    return a

function extended_gcd(a, b):
    if a is 0:
        return (b, 0, 1)
    else:
        gcd_val, x, y = extended_gcd(b % a, a)
        return (gcd_val, y - (b // a) * x, x)