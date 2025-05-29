"""

liste = [5,5.5,"temel",True,["Python",45,False]]

print(liste[4][2])

----------------------------

Cities = ["İstanbul","Ankara","Adana","Konya"]

for city  in Cities:
    print(city)

new_city = input("Enter City : ")
Cities +=[new_city]

for city  in Cities:
    print(city)

------------------------------

kitap_listesi = list()

menu= """ """
1- Kitap Ekle
2- Kitap Çıkar
3- Kitap Göster
Q- Çıkış
"""
"""

def kitap_ekle(liste,kitap):
    liste += [kitap]
    print("Kitap Eklendi")

def kitap_cikar(liste,kitap):
    pass

def kitap_goster(liste):
    for kitap in liste:
        print("Kitap Adı >>>>>> ",kitap)

def cikis():
    print("Programdan çıkılıyor......")
    quit()

while True:
    print(menu)
    secim = input("Seçiminiz : ")
    if secim == "1":
        kitap_adi = input("Kitap Adı : ")
        kitap_ekle(kitap_listesi,kitap_adi)
    elif secim == "2":
        kitap_adi = input("Kitap Adı : ")
        kitap_cikar(kitap_listesi,kitap_adi)
    elif secim == "3":
        kitap_goster(kitap_listesi)
        input("Ana menu için Enter'a basınız!")
    elif secim == "Q" or secim == "q":
        cikis()
    else:
        print("Hatalı giriş yaptınız.")
        input("Ana menu için Enter'a basınız!")

-------------------------

sozluk = {
    "Doğum" : 1975,
    "Meslek": "Yazılımcı",
    "Konum" : "Ankara"
}

print(sozluk["Doğum"])

-----------------------------

savasci = {
    "Güç":85,
    "Can":1500,
    "Zırh":30,
}

buyucu = {
    "Güç":120,
    "Can":1300,
    "Zırh":5,
}

def vur(vuran:dict,vurulan:dict):
    ekslien= vuran["Güç"]-vurulan["Zırh"]
    vurulan["Can"]-=ekslien
    print("Savaşçı : ",savasci)
    print("Büyücü : ", buyucu)

while True:
    input("Vurmak için enter'a basınız!")
    vur(savasci,buyucu)
    print("Savaşçı Büyücüye Saldırdı.")
    print("Büyücünün Can Değeri : ",buyucu["Can"])
    input("Vurmak için enter'a basınız!")
    vur(buyucu,savasci)
    print("Büyücü Savaşçıya Saldırdı.")
    print("Savaşçının Can Değeri : ", savasci["Can"])

# ----- printlere EMOJİ EKLE -----

--------------------------

import timeit

kume = {}
demet =()
liste=[]

liste = [10,20,30,40,50]
liste_zaman = timeit.timeit("liste[1]", globals=globals(),number=100000000)

demet = (10,20,30,40,50)
demet_zaman = timeit.timeit("demet[1]", globals=globals(),number=100000000)


print("Liste Zaman : ", liste_zaman )
print("Demet Zaman : ", demet_zaman )

------------------------------

liste =["Furkan","Python"]
a = "YapayZeka"
liste += [a]
liste.append(15)
print(liste)
liste.remove(15)
print(liste)

print(a.upper())

---------------------------

sozluk ={"Siyah":"Kara","Beyaz":"Ak","Kırmızı":"Al","Tane":"Adet","Anıt":"Abide"}

print(sozluk.get("Siyah"))

------------------

rehber = {
    "Furkan":{
        "Cep": 123456,
        "İş": 11111,
        "eeee":1212
    }
}
"""

"""

dosya = open("deneme.txt", "r", encoding="utf-8")
eklenecek_veri = "Hayat sevince Güzel"
veri = dosya.readlines()
print(veri)
dosya.close()

"""
