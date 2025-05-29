import sqlite3

db = sqlite3.connect("veritabani.db")
imlec = db.cursor()

imlec.execute("CREATE TABLE IF NOT EXISTS 'kisiselBilgiler' (isim,soyisim,yas,dyeri)")
imlec.execute("INSERT INTO 'kisiselBilgiler' VALUES ('Temek','Reis','70','Rize') ")


imlec.execute("SELECT isim,dyeri FROM 'kisiselBilgiler'")
veriler = imlec.fetchall()

print(veriler)

for veri in veriler:
    print(veri[0],veri[1])


db.commit()
db.close()
