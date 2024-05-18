import keyGeneration

with open('Akeys.txt','w') as file:
    eA, dA ,nA = keyGeneration.generatekey()
    # print(f'{e} {d} {n}')
    file.write(f'{eA},{dA},{nA}')

with open('Bkeys.txt','w') as file:
    eB, dB ,nB = keyGeneration.generatekey()
    # print(f'{e} {d} {n}')
    file.write(f'{eB},{dB},{nB}')

with open('Ckeys.txt','w') as file:
    eC, dC ,nC = keyGeneration.generatekey()
    # print(f'{e} {d} {n}')
    file.write(f'{eC},{dC},{nC}')

with open('Skeys.txt','w') as file:
    eS, dS ,nS = keyGeneration.generatekey()
    # print(f'{e} {d} {n}')
    file.write(f'{eS},{dS},{nS}')

with open('publicKeys.txt', 'a') as file:
    file.write(f'A,{eA},{nA}\n')
    file.write(f'B,{eB},{nB}\n')
    file.write(f'C,{eC},{nC}\n')
    file.write(f'S,{eS},{nS}\n')

