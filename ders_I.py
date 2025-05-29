"""
a = "Kullanıcı adi"
b= "Şifre"
c ="Doğum Tarihi"

print(a,b,c,sep="----", end="\n")

print("""
from tabnanny import check

""")

------------------------------

giris=input("Adınız: ")

isim = giris
soy_isim = "qwer"

print("isim:  ",isim)
print("Soy isim: ",soy_isim)

----------------------------

sayi_1 =float(input("Birinci sayiyi giriniz: "))
sayi_2 =float(input("İkinci sayiyi giriniz: "))

print("iki sayinin toplami : ", sayi_1+sayi_2)
print("iki sayinin çarpımı : ", sayi_1*sayi_2)

---------------------------

a = input("bir sayi gir: ")

if a == "3":
    print("a 3 tür")
elif a == "5":
    print("a 5 tir")
else:
    print("koşul yok")
    
------------------------

sayi1 = float(input("Birinci sayi: "))
isaret = input("yapılacak işlem: ")
sayi2 = float(input("İkinci sayi: "))

if isaret =="+":
    print("Sonuç : ",sayi1+sayi2)
elif isaret =="-":
    print("Sonuç : ",sayi1-sayi2)
elif isaret =="*":
    print("Sonuç : ",sayi1*sayi2)
elif isaret =="/":
    print("Sonuç : ",sayi1/sayi2)
else:
    print("Hatalı işlem")

-----------------------------

print("Taktir Teşkür Hesaplayıcı")

mynot = float(input("Notunuzu giriniz: "))

if mynot<50:
    print("Kaldın....")
elif mynot>=50 and mynot <70:
    print("düz geçtin kanks")
elif mynot>=70 and mynot <85:
    print("ooo fenasın teşkür filan")
elif mynot>=85 and mynot <=100:
    print("şerrefsizzzz geceleri mi çalıştın lan takdir ne!!")
else:
    print("yavaş lan kaç puan alıyon")

-----------------------------

username = input("Username : ")
password= input("Password : ")

check_username = "furkan"
check_password = "12345"

if check_username != username:
    print("Wrong Username")
elif check_password != password:
    print("Wrong Password")
else:
    print("You are in Sir ",username)

--------------------

parola = input("Parola giriniz: ")

if "a" and "A" in parola:
    print("A ve a girmeyin")
if "b" in parola:
    print("b girmeyin")
if "c" in parola:
    print("c girmeyin")
if "?" not in parola:
    print("? kullan kardeş")

------------------

anahtar = True
parola = input("Parola giriniz: ")

list = "/*?!'+%"

for simge in list:
    if simge not in parola:
        anahtar = False
    elif anahtar:
        print("Şifreniz başarıyla oluştu")
        break

if anahtar == False:
    print("Şifrenizde simge kullanın")

-----------------------------

sayilar = "01234"

for sayi in sayilar:
    print(sayi)

# range(a,b,c) a = başlangıç | b = bitiş  | c = artış miktarı
for sayi in range(10,20,5):
    print(sayi)

a = 10
while a<=100:
    print("Yapay Zeka ",a)
    a*=2

----------------

def toplama(ilk:int, ikinci:int) -> int:
    topla = ilk+ ikinci
    return topla

print(toplama(3,3))

--------------

def hipo(a,b,c):
    if (a**2 + b**2) == c**2:
       return "Üçgen Dik üçgen"
    else:
        return "Dik değel"

print(hipo(3,4,5))

--------------
"""
