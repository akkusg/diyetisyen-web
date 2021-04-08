from flask import Flask, render_template, request

app = Flask(__name__)
app.config["DEBUG"] = True


@app.route('/')
def baslangic():
    return render_template("anasayfa.html")


@app.route('/hakkimizda')
def hakkimizda():
    return render_template("hakkimizda.html")


@app.route('/iletisim')
def iletisim():
    return render_template("iletisim.html")


@app.route('/mesajkaydet', methods=['POST'])
def mesaj_kaydet():
    adsoyad = request.form.get('adsoyad')
    email = request.form.get('email')
    mesaj = request.form.get('mesaj')
    satir = adsoyad + "||" + email + "||" + mesaj + "\n"
    f = open("mesajlar.txt", "a")
    f.write(satir)
    f.close()
    return mesajlar()
    #return "Sayın " + adsoyad + ". Mesajınız için teşekkürler. Tüm mesajlar için tıklayın."

@app.route('/mesajlar')
def mesajlar():
    satirlar = ""
    mesaj_listesi = []
    f = open("mesajlar.txt", "r")
    for satir in f:
        bilgiler = satir.split("||")
        adsoyad = bilgiler[0]
        isimler = adsoyad.split()
        cnt = 0
        yildizli_isim = ""
        for karakter in isimler[0]:
            if cnt == 0:
                yildizli_isim += karakter
                cnt += 1
            else:
                yildizli_isim += "*"
        email=bilgiler[1]
        mesaj=bilgiler[2]
        print(bilgiler)
        satirlar = satirlar + "<b>" + yildizli_isim + "</b> dedi ki: " + mesaj + "<br>"
        mesaj_listesi.append({"adsoyad":adsoyad,"email":email,"mesaj":mesaj})
    f.close()
    return render_template("mesajlar.html", mesaj_listesi=mesaj_listesi)



@app.route('/hesapla', methods=['POST'])
def hesapla():
    '''
    Yetişkin bir erkeğin vücut yağ oranı yüzde 12-18'i,
    kadınların ise yüzde 20-28 oranında olması beklenir.
    '''
    boy = int(request.form.get('boy'))
    kilo = int(request.form.get('kilo'))
    boy = boy/100

    vki = kilo / (boy * boy)
    cinsiyet = request.form.get('cinsiyet')
    if cinsiyet == "k":
        if 20 < vki < 28:
            return "Vücut Kitle İndeksine göre NORMAL durumdasınız."
        else:
            return "Vücut Kitle İndeksine göre sorun var."
    else:
        if 12 < vki < 18:
            return "Vücut Kitle İndeksine " + str(vki) + " göre NORMAL durumdasınız."
        else:
            return "Vücut Kitle İndeksine " + str(vki) + " göre sorun var."


if __name__ == "__main__":
    app.run()
