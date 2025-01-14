import math 
import random 
import sympy


def generatekey():
    while True:
        p = random.randint(1000, 10000000)
        q = random.randint(1000, 10000000)
        if sympy.isprime(p) and sympy.isprime(q) and p != q:
            break 

    n = p * q 
    phi_n = (p-1)*(q-1)
    while True:
        e = random.choice(range(0, phi_n))    
        if math.gcd(e,phi_n)==1:
            break

    d = pow(e, -1, phi_n)
    return e,d,n



