import math 
import random 
import sympy



while True:
    p = random.randint(1, 1000)
    q = random.randint(1, 1000)
    if sympy.isprime(p) and sympy.isprime(q) and p != q:
        break 

n = p * q 
phi_n = (p-1)*(q-1)
while True:
    e = random.choice(range(0, phi_n))    
    if math.gcd(e,phi_n)==1:
        break

d = pow(e, -1, phi_n)



print(p)
print(q)
print(phi_n)
print(n)
print(e)
print(d)
