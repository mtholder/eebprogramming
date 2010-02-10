#!/usr/bin/env python
import sys
if len(sys.argv) != 2:
    sys.exit(sys.argv[0] + ": Expecting one command line argument -- the integer to factor into primes")
n = int(sys.argv[1])
if n < 1:
    sys.exit(sys.argv[0] + "Expecting a positive integer")

if n == 1:
    print 1
    sys.exit(0)



def get_smallest_prime_factor(x):
    "Returns the smallest integer that is a factor of `x` or `None`"
    for i in range(2, x):
        if (x % i) == 0:
            return i
    return None

def factor_into_primes(x):
    "Returns a list of prime numbers that are factors of `x`"
    current = x
    primes = []
    while True:
        y = get_smallest_prime_factor(current)
        if y is None:
            break
        primes.append(y)
        current = current/y
    primes.append(current)
    return primes



p = factor_into_primes(n)

#convert to string.
p_str = []
product = 1
for el in p:
    p_str.append(str(el))
    product = product * el

assert product == n

print " ".join(p_str)
