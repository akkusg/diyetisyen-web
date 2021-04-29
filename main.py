import datetime

from flask import Flask, render_template, request, redirect, session
import pymongo

app = Flask(__name__)
app.secret_key = 'bizim cok zor gizli sozcugumuz'

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["INP102"]
mesajlar_tablosu = mydb["mesajlar"]
kullanicilar_tablosu = mydb["kullanicilar"]
oturum_acilis_tablosu = mydb["oturum_acilis"]


@app.route('/')
def baslangic():
    if 'kullanici' not in session:
        return redirect("/giris", code=302)
    else:
        kullanici = session["kullanici"]
        return render_template("anasayfa.html", hesaplama_mesaji="", kullanici=kullanici)


@app.route('/giris', methods=['GET','POST'])
def giris():
    if request.method == 'POST':
        kullanici = request.form['kullanici']
        sifre = request.form['sifre']
        kayit = kullanicilar_tablosu.find_one({"kullanici": kullanici})
        if kayit:
            if sifre == kayit["sifre"]:
                session["kullanici"] = kullanici
                oturum_acilis_tablosu.insert_one({"kullanici": kullanici, "zaman": datetime.datetime.now()})
                return redirect("/", code=302)
            else:
                oturum_acilis_tablosu.insert_one({"kullanici": kullanici, "hata":"Hatalı Şifre Girişi", "zaman": datetime.datetime.now()})
                return "Şifre yanlış"
        else:
            return "Kullanıcı bulunamadı"
    else:
        return render_template("giris.html")


@app.route('/cikis')
def cikis():
    session.clear()
    return redirect("/", code=302)


@app.route('/uyeol', methods=['GET','POST'])
def uyeol():
    if request.method == 'POST':
        kayit = dict(request.form)
        kullanicilar_tablosu.insert_one(kayit)
        return redirect("/giris", code=302)
    else:
        return render_template("uyeol.html")




@app.route('/hakkimizda')
def hakkimizda():
    if 'kullanici' not in session:
        return redirect("/giris", code=302)
    else:
        return render_template("hakkimizda.html")


@app.route('/profil/<profilno>')
def profil_goster(profilno):
    if 'kullanici' not in session:
        return redirect("/giris", code=302)
    else:
        if profilno == "1":
            adsoyad = "Jane Doe"
        else:
            adsoyad = "John Doe"
        return render_template("profil.html", adsoyad=adsoyad)



@app.route('/iletisim')
def iletisim():
    if 'kullanici' not in session:
        return redirect("/giris", code=302)
    else:
        return render_template("iletisim.html")


@app.route('/mesajkaydet', methods=['POST'])
def mesaj_kaydet():
    adsoyad = request.form.get('adsoyad')
    email = request.form.get('email')
    mesaj = request.form.get('mesaj')

    kayit = {"adsoyad": adsoyad, "email": email, "mesaj":mesaj}
    kaydedilmis = mesajlar_tablosu.insert_one(kayit)
    return redirect("/mesajlar", code=302)
    #return "Sayın " + adsoyad + ". Mesajınız için teşekkürler. Tüm mesajlar için tıklayın."

@app.route('/mesajlar')
def mesajlar():
    mesaj_listesi = list(mesajlar_tablosu.find())
    return render_template("mesajlar.html", mesaj_listesi=mesaj_listesi)



@app.route('/hesapla', methods=['POST'])
def hesapla():
    '''
    Yetişkin bir erkeğin vücut yağ oranı yüzde 12-18'i,
    kadınların ise yüzde 20-28 oranında olması beklenir.
    '''
    boy = int(request.form.get('boy'))
    kilo = int(request.form.get('kilo'))
    vboy = boy/100

    vki = kilo / (vboy * vboy)
    cinsiyet = request.form.get('cinsiyet')
    renk = "success"
    hesaplama_mesaji = ""
    link_var = False
    if cinsiyet == "k":
        if 20 < vki < 28:
            hesaplama_mesaji = "Vücut Kitle İndeksine göre NORMAL durumdasınız."
        else:
            hesaplama_mesaji = "Vücut Kitle İndeksine " + str(vki) + " göre sorun var."
            renk = "danger"
            link_var = True
    else:
        if 12 < vki < 18:
            hesaplama_mesaji = "Vücut Kitle İndeksine " + str(vki) + " göre NORMAL durumdasınız."
        else:
            hesaplama_mesaji = "Vücut Kitle İndeksine " + str(vki) + " göre problem var."
            renk = "danger"
            link_var = True
    return render_template("anasayfa.html", hesaplama_mesaji=hesaplama_mesaji, boy=boy, kilo=kilo, renk=renk, link_var=link_var)


if __name__ == "__main__":
    app.run(debug=True)
