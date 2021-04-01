from flask import Flask, render_template, request

app = Flask(__name__)
app.config["DEBUG"] = True


@app.route('/')
def baslangic():
    return render_template("anasayfa.html")


@app.route('/hakkimizda')
def hakkimizda():
    return render_template("hakkimizda.html")


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
