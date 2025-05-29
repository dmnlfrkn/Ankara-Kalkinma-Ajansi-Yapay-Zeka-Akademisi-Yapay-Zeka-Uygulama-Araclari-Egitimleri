masalar = dict()

for a in range(20):
    masalar[a] = 0

def display_masa():
    for a in range(20):
        print("Masa {} için hesap : {} TL".format(a+1,masalar[a]))

def hesap_ekle():
    masa_no = int(input("Masa Numarası : "))-1
    bakiye =masalar[masa_no]
    eklenenecek_ucret = float(input("Eklenecek Ücret : "))
    guncel_bakiye = bakiye + eklenenecek_ucret
    masalar[masa_no] = guncel_bakiye


def hesap_ode():
    masa_no = int(input("Masa Numarası : ")) -1
    bakiye = masalar[masa_no]
    print("Masa {}'in hesabı : {} TL".format(masa_no+1,bakiye))
    input("Ödeme yapmak için Enter'a basın!")
    masalar[masa_no]= 0
    print("Hesap Ödendi.")

def dosya_kontrol(dosya_adi):
    try:
        dosya =  open(dosya_adi,"r",encoding="utf-8")
        veri = dosya.read()
        veri = veri.split("\n")
        veri.pop()
        dosya.close()
        for a in enumerate(veri):
            masalar[a[0]] = float(a[1])
    except FileNotFoundError:
        dosya = open(dosya_adi, "w", encoding="utf-8")
        dosya.close()
        print("Kayıt Dosyası Oluşturuldu.")

def dosya_guncelle(dosya_adi):
    dosya = open(dosya_adi, "w", encoding="utf-8")
    for a in range(20):
        bakiye = masalar[a]
        bakiye = str(bakiye)
        dosya.write(bakiye+"\n")
    dosya.close()

def ana_islemler():
    dosya_kontrol("bakiye.txt")
    while True:
        print("""
            Yapay Zeka Lokanta Hoşgeldiniz
            
        1- Masaları Görüntüle
        2- Hesap Ekle
        3- Hesap Öde
        Q+ Çıkıs    
        """)

        secim = input("Yapılacak İşlemi Giriniz : ")
        if secim == "1":
            display_masa()
        elif secim == "2":
            hesap_ekle()
        elif secim == "3":
            hesap_ode()
        elif secim == "Q" or secim == "q":
            print("Çıkış Yapılıyor...")
            break
        else:
            print("Hatalı seçim yaptınız")
        dosya_guncelle("bakiye.txt")
        input("Anamenüye Dönmek İçin Entera Basınız")
    dosya_guncelle("bakiye.txt")
    print("Güncelleme yapıldı.")

ana_islemler()
