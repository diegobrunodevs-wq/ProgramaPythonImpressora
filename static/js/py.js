async function testarSamsung() {

    const status = document.getElementById("status");

    status.textContent = "🟡 Consultando impressora...";

    try {

        const resposta = await fetch("/teste/samsung");

        const dados = await resposta.text();


        function pegarCampo(nome) {

            const regex = new RegExp(
                nome + "\\s*:\\s*([^,\\n}]+)"
            );

            const encontrado = dados.match(regex);

            if (!encontrado) {
                return "N/D";
            }

            return encontrado[1]
                .trim()
                .replace(/^"|"$/g, "");
        }


        const serial =
            pegarCampo("GXI_SYS_SERIAL_NUM");


        const impressoes =
            pegarCampo("GXI_BILLING_PRINT_TOTAL_IMP_CNT");


        const copias =
            pegarCampo("GXI_BILLING_COPY_TOTAL_IMP_CNT");


        const fax =
            pegarCampo("GXI_BILLING_FAX_TOTAL_IMP_CNT");


        const relatorios =
            pegarCampo("GXI_BILLING_REPORT_TOTAL_IMP_CNT");


        const total =
            pegarCampo("GXI_BILLING_TOTAL_IMP_CNT");


        const envioSMB =
            pegarCampo("GXI_BILLING_SEND_TO_SMB_CNT");


        const envioTotal =
            pegarCampo("GXI_BILLING_SEND_TO_TOTAL_CNT");


        document.getElementById("serial").textContent =
            serial;


        document.getElementById("impressoes").textContent =
            formatarNumero(impressoes);


        document.getElementById("copias").textContent =
            formatarNumero(copias);


        document.getElementById("fax").textContent =
            formatarNumero(fax);


        document.getElementById("relatorios").textContent =
            formatarNumero(relatorios);


        document.getElementById("total").textContent =
            formatarNumero(total);


        document.getElementById("envioSMB").textContent =
            formatarNumero(envioSMB);


        document.getElementById("envioTotal").textContent =
            formatarNumero(envioTotal);


        status.textContent =
            "🟢 ONLINE";

    }


    catch (erro) {

        console.error(erro);

        status.textContent =
            "🔴 OFFLINE";

    }

}


function formatarNumero(valor) {

    const numero = Number(valor);

    if (isNaN(numero)) {
        return valor;
    }

    return numero.toLocaleString("pt-BR");

}


function gerarPDF() {

    window.open("/pdf/samsung", "_blank");

}