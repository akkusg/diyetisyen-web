from flask import Flask, render_template, request

app = Flask(__name__)
app.config["DEBUG"] = True


@app.route('/')
def baslangic():
    return render_template("anasayfa.html", hesaplama_mesaji="")


@app.route('/hakkimizda')
def hakkimizda():
    return render_template("hakkimizda.html")

@app.route('/profil/<profilno>')
def profil_goster(profilno):
    if profilno == "1":
        adsoyad = "Jane Doe"
    else:
        adsoyad = "John Doe"
    return render_template("profil.html", adsoyad=adsoyad)



@app.route('/iletisim')
def iletisim():
    return render_template("iletisim.html")


@app.route('/mesajkaydet', methods=['POST'])
def mesaj_kaydet():
    adsoyad = request.form.get('adsoyad')
    email = request.form.get('email')
    mesaj = request.form.get('mesaj').replace("\r","").replace("\n", " - ")
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
            hesaplama_mesaji = "Vücut Kitle İndeksine " + str(vki) + " göre sorun var."
            renk = "danger"
            link_var = True


    return render_template("anasayfa.html", hesaplama_mesaji=hesaplama_mesaji, boy=boy, kilo=kilo, renk=renk, link_var=link_var)

if __name__ == "__main__":
    app.run()
