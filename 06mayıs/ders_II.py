"""

def ucgen(a,b,c):
    if a**2+b**2==c**2:
        return True
    else:
        return False

print(ucgen(3,4,5))


ucgen2 = lambda a,b,c : a**2+b**2==c**2

print(ucgen2(3,4,5))

----------------

def factorial(sayi): # 6! = 1*2*3*4*5*6
    sonuc = 1
    for a in range(6):
        b = a+1
        sonuc *=b
    return sonuc

print(factorial(6))

def recursive_factorial(sayi):
    if sayi ==1:
        return 1
    else:
        return sayi * recursive_factorial(sayi-1)

print(recursive_factorial(6))

----------------

from hesap_mak import ucgen2 as dikucgen

print( dikucgen(7,24,25) )

----------------

import time

a = time.time()
print(f"Python zaman : {a}")
time.sleep(3)
print("Kursu")
time.sleep(3)
print("Yapay Zeka")
b = time.time()
print(f"Fark : {b-a}  b zaman : {b}")


----------------
"""

import random
import os

while True:

    #os.system("cls")
    rastgele = random.randint(1,9)
    sayi = int(input("Bir sayi giriniz. : "))
    print("Tuttuğum sayi : ",rastgele)
    if sayi == rastgele:
        print("Tebrikler kral")
        quit()
    else:
        input("Yeniden oynama için Entera basın....")

