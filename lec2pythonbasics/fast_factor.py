#!/usr/bin/env python
import sys
import math
if len(sys.argv) != 2:
    sys.exit(sys.argv[0] + ": Expecting one command line argument -- the integer to factor into primes")
n = long(sys.argv[1])
if n < 1:
    sys.exit(sys.argv[0] + "Expecting a positive integer")

if n == 1:
    print 1
    sys.exit(0)


def factor_into_primes(x):
    "Returns a list of prime numbers that are factors of `x`"
    current_x = x
    primes = []
    while (current_x % 2) == 0:
        primes.append(2)
        current_x = (current_x / 2)
    while (current_x % 3) == 0:
        primes.append(3)
        current_x = (current_x / 3)

    potential_factor = 5
    upper_limit = long(math.sqrt(current_x))
    while potential_factor <= upper_limit:
        while ((current_x % potential_factor) == 0) and (potential_factor <= upper_limit):
            primes.append(potential_factor)
            current_x = (current_x / potential_factor)
            upper_limit = long(math.sqrt(current_x))

        potential_factor += 2

    if current_x != 1:
        primes.append(current_x)
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
