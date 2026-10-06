from flask import Flask, send_file
import requests
import re

from impressoras import IMPRESSORAS
from banco import salvar_afericao

app = Flask(__name__)


@app.route("/")
def index():
    return send_file("index.html")

@app.route("/api/impressoras")
def listar_impressora():
    return IMPRESSORAS


@app.route("/api/impressoras/<impressora_id>")
def consultar_impressora(impressora_id):

    impressora = next(
        (
            impressora
            for impressora in IMPRESSORAS
            if impressora["id"] == impressora_id
        ),
        None
    )

    if impressora is None:
        return {
            "erro": "Impressora não encontrada"
        }, 404


    # Por enquanto, somente Samsung SL-M4020ND está implementada.
    # Nenhuma outra impressora será consultada por esta rota.

    if impressora["nome"] != "Samsung SL-M4020ND":
        return {
            "erro": "Coletor ainda não implementado para esta impressora"
        }, 400


    ip = impressora["ip"]

    url = (
        f"http://{ip}"
        "/sws/app/information/counters/counters.json"
    )


    try:

        response = requests.get(
            url,
            timeout=10,
            allow_redirects=False
        )


        if response.status_code != 200:
            return response.text, response.status_code


        def pegar_campo(nome):

            encontrado = re.search(
                rf"{nome}\s*:\s*([^,\n}}]+)",
                response.text
            )


            if not encontrado:
                return None


            valor = encontrado.group(1).strip()

            valor = valor.strip('"')


            try:
                return int(valor)

            except ValueError:
                return valor


        dados = {

            "impressora_id": impressora["id"],

            "contador_impressao": pegar_campo(
                "GXI_BILLING_PRINT_TOTAL_IMP_CNT"
            ),

            "contador_copia": pegar_campo(
                "GXI_BILLING_COPY_TOTAL_IMP_CNT"
            ),

            "contador_fax": pegar_campo(
                "GXI_BILLING_FAX_TOTAL_IMP_CNT"
            ),

            "contador_relatorio": pegar_campo(
                "GXI_BILLING_REPORT_TOTAL_IMP_CNT"
            ),

            "contador_total": pegar_campo(
                "GXI_BILLING_TOTAL_IMP_CNT"
            ),

            "envio_smb": pegar_campo(
                "GXI_BILLING_SEND_TO_SMB_CNT"
            ),

            "envio_total": pegar_campo(
                "GXI_BILLING_SEND_TO_TOTAL_CNT"
            ),

            "serial": pegar_campo(
                "GXI_SYS_SERIAL_NUM"
            )
        }


        print("===================================")
        print("AFERIÇÃO SAMSUNG")
        print(dados)
        print("===================================")


        salvar_afericao(dados)


        return dados, 200


    except requests.RequestException as erro:

        print("ERRO:", erro)

        return str(erro), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)