from flask import Flask, send_file
import requests
from impressoras import IMPRESSORAS

app = Flask(__name__)


@app.route("/")
def index():
    return send_file("index.html")


@app.route("/teste/samsung")
def teste_samsung():

    ip = IMPRESSORAS[0]["ip"]

    url = f"http://{ip}/sws/app/information/counters/counters.json"

    try:
        response = requests.get(
            url,
            timeout=10,
            allow_redirects=False
        )

        print("STATUS:", response.status_code)
        print("RESPOSTA:")
        print(response.text)

        return response.text, response.status_code

    except requests.RequestException as erro:
        print("ERRO:", erro)
        return str(erro), 500


if __name__ == "__main__":
    app.run(debug=True)