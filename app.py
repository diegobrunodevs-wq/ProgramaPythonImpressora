from flask import Flask, send_file
import requests
from impressoras import IMPRESSORAS

app = Flask(__name__)


@app.route("/")
def index():
    return send_file("index.html")

@app.route("/api/impressoras")
def listar_impressora():
    return IMPRESSORAS


@app.route("/teste/samsung")
def teste_samsung():

    ip = "192.168.1.237"

    url = f"http://{ip}/sws/app/information/counters/counters.json"

    try:
        response = requests.get(
            url,
            timeout=10,
            allow_redirects=False
        )

        print("===================================")
        print("IMPRESSORA: Samsung M407")
        print("IP:", ip)
        print("STATUS:", response.status_code)
        print("CONTENT-TYPE:", response.headers.get("Content-Type"))
        print("LOCATION:", response.headers.get("Location"))
        print("RESPOSTA:")
        print(response.text)
        print("===================================")

        return response.text, response.status_code

    except requests.RequestException as erro:

        print("ERRO:", erro)

        return str(erro), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)