"""
class karakter():
    saglik=0
    saldiri=0
    silah=""
    ekipman=""
    isim=""
    cephanelik=""

savasci = karakter()
savasci.saglik=250
savasci.silah ="Kılıç"
savasci.ekipman ="Kalkan"
savasci.isim ="Battal"
savasci.saldiri = 50

buyucu = karakter()
buyucu.saglik=500
buyucu.silah ="Asa"
buyucu.ekipman ="Pelerin"
buyucu.isim ="Ahmet"
buyucu.cephanelik = 1200
buyucu.saldiri = 25

savasci.saglik -= buyucu.saldiri

print(savasci.saglik)
-----------------------------------


class karakter():
    liste = []

battal = karakter()
battal.liste += ["battal"]

ahmet = karakter()
ahmet.liste += ["ahmet"]

print(battal.liste)
print(ahmet.liste)

----------------------


class karakter():
    def __init__(self,can):
        self.liste = []
        self.can = can

battal = karakter(100)
battal.liste += ["battal"]

ahmet = karakter(200)
ahmet.liste += ["ahmet"]

print(battal.liste)
print(ahmet.liste)

----------------------


import random
import os




class Hedef():
    def __init__(self):
        self.saglik = random.randint(5,10)
        self.guc = random.randint(3,8)
        self.kalkan = random.randint(1,6)
        self.is_alive = True
    def vur(self,oyuncu):
        atak = self.guc - oyuncu.kalkan
        oyuncu.saglik -= atak
        if oyuncu.saglik <= 0:
            oyuncu.is_alive = False

class Oyuncu():
    def __init__(self):
        self.saglik = 40
        self.guc = 7
        self.kalkan = 2
        self.is_alive = True
    def vur(self,hedef):
        atak = self.guc - hedef.kalkan
        hedef.saglik -= atak
        if hedef.saglik <= 0:
            hedef.is_alive = False
            hedefler.remove(hedef)

hedefler = list()

for a in range(5):
    hedefler.append(Hedef())

oyuncu = Oyuncu()

while True:
    os.system("cls")
    print("Oyuncu ----- Sağlık {} ----- Saldırı {} ----- Kalkan {}".format(oyuncu.saglik,oyuncu.guc,oyuncu.kalkan))
    print("-"*90)
    for a in hedefler:
        print("{}. Hedef ----- Sağlık : {} ----- Saldırı : {} ----- Kalkan : {}".format(hedefler.index(a)+1),a.saglik,a.guc,a.kalkan)
    if oyuncu.is_alive:
        print("Kaybettiniz")
    elif not hedefler:
        print("Kazandınız")


    try:
        secim = int(input("Hedef Seçin :"))
        vurulan_hedef = hedefler[secim-1]
        oyuncu.vur(vurulan_hedef)
        if hedefler:
            saldıran = hedefler[random.randint(a- len(hedefler)-1)]
            print("{}. Vuran Hedef ----- Sağlık : {} ----- Saldırı : {} ----- Kalkan : {} ".format(hedefler.index(saldıran)+1,saldıran.saglik,saldıran.guc,saldıran.kalkan))
            saldıran.vur(oyuncu)
        input("Yeniden Saldırmak için Enter a Basın")
    except IndexError:
        input("Hatalı seçim yaptınız. Yeniden Başlamak için Entera Basın")

---------------------------------------

"""

class Musteri():
    def __init__(self,TC,ISIM,SIFRE):
        self.tc = TC
        self.isim = ISIM
        self.sifre = SIFRE
        self.bakiye =0

class Banka():
    def __init__(self):
        self.musteriler = list()

    def musteri_ol(self,TC,ISIM,SIFRE):
        self.musteriler.append(Musteri(TC,ISIM,SIFRE))
        print("Kayıt için Teşkürler")

banka = Banka()
menu= "Ana menüye dönmek için Entera basınız"

while True:
    print("""
        BattalBanka Hoşgeldiniz
        
        1- Müsteriyim
        2- Üye Ol
        Q- Çıkıs
    """)
    secim = input("Seçiminiz : ")

    if secim == "1":
        girilen_TC = input("TC no giriniz : ")
        tc_no = [a.tc for a in banka.musteriler]
        if girilen_TC in tc_no:
            for musteri in banka.musteriler:
                if girilen_TC == musteri.tc:
                    girilen_sifre = input("Şifre giriniz : ")
                    if girilen_sifre == musteri.sifre:
                        while True:
                            print("""
                                Hosgeldiniz Sayın {}
                                
                                1- Bakiye Sorgula
                                2- Para yatır
                                3- Para Transfer Et
                                4- Para çek
                                Q- Çıkış
                            """.format(musteri.isim))
                            secim2 = input("İşlem Numarası : ")
                            if secim2 == "1":
                                print("Bakiyeniz : {}".format(musteri.bakiye))
                                input(menu)
                            elif secim2 == "2":
                                yatırılan_tutar = int(input("Miktar Girin : "))
                                onay = input("Kendi Hesabınıza {} Tl yatırıyorsunuz? (E/H)".format(yatırılan_tutar))
                                onay = onay.lower()
                                if onay =="e":
                                    musteri.bakiye += yatırılan_tutar
                                    print("Para yatırıldı.")
                                    input(menu)
                                elif onay== "h":
                                    print("İşlem iptal edildi")
                                    input(menu)
                                else:
                                    print("Hatalı işlem")
                                    input(menu)
                            elif secim2 == "3":
                                hedef_tc = input("Hedef TC")
                                if hedef_tc in tc_no:
                                    for musteri2 in banka.musteriler:
                                        if hedef_tc == musteri2.tc:
                                            yatırılan_tutar2 = int(input("Miktar : "))
                                            if yatırılan_tutar2 <= musteri.bakiye:
                                                onay = input("{} adlı kişiye , {} tutarunda para gönderiyorsun  ?".format(musteri2.isim,yatırılan_tutar2))
                                                onay = onay.lower()
                                                if onay =="e":
                                                    musteri2.bakiye += yatırılan_tutar2
                                                    musteri.bakiye-= yatırılan_tutar2
                                                    print("Para gönderildi.")
                                                    input(menu)
                                                elif onay =="h":
                                                    print("işlem iptal edildi")
                                                    input(menu)
                                                else:
                                                    print("hatalı işlem")
                                                    input(menu)
                                        else:
                                            print("müşteri bulunamadı")
                                            input(menu)
                            elif secim2 == "4":
                                cekilecek_tutar = int(input("Miktar : "))
                                if cekilecek_tutar <= musteri.bakiye:
                                    musteri.bakiye-= cekilecek_tutar
                                    print("İşlem tamam")
                                    input(menu)
                                else:
                                    print("Bakiye yetersiz")
                                    input(menu)
                            elif secim2 == "q" or secim2 =="Q":
                                print("Hesabınızdan Çıkılıyor...")
                                input(menu)
                                break
                            else:
                                print("Hatalı İşlem")
                                input(menu)

    elif secim == "2":
        t = input("TC giriniz: ")
        i = input("İSİM giriniz: ")
        s = input("ŞİFRE giriniz: ")
        banka.musteri_ol(t,i,s)
        input(menu)
    elif secim == "Q" or secim == "q":
        print("Çıkış yapılıyor.")
        break

    else:
        print("Hatalı İşlem")
        input("Yeni işlem için Entera Basın")
