async function consultarImpressora(impressoraId) {

    const status =
        document.getElementById(`status-${impressoraId}`);

    if (!status) {
        console.error(
            `Status da impressora não encontrado: ${impressoraId}`
        );
        return;
    }

    status.textContent = "🟡 Consultando impressora...";

    try {

        const resposta = await fetch(
            `/api/impressoras/${impressoraId}`,
            {
                method: "GET",
                cache: "no-store"
            }
        );

        if (!resposta.ok) {
            throw new Error(
                `Erro HTTP ${resposta.status}`
            );
        }

        const dados = await resposta.json();


        document.getElementById(
            `serial-${impressoraId}`
        ).textContent =
            dados.serial ?? "N/D";


        document.getElementById(
            `impressoes-${impressoraId}`
        ).textContent =
            formatarNumero(
                dados.contador_impressao
            );


        document.getElementById(
            `copias-${impressoraId}`
        ).textContent =
            formatarNumero(
                dados.contador_copia
            );


        document.getElementById(
            `fax-${impressoraId}`
        ).textContent =
            formatarNumero(
                dados.contador_fax
            );


        document.getElementById(
            `relatorios-${impressoraId}`
        ).textContent =
            formatarNumero(
                dados.contador_relatorio
            );


        document.getElementById(
            `total-${impressoraId}`
        ).textContent =
            formatarNumero(
                dados.contador_total
            );


        document.getElementById(
            `envioSMB-${impressoraId}`
        ).textContent =
            formatarNumero(
                dados.envio_smb
            );


        document.getElementById(
            `envioTotal-${impressoraId}`
        ).textContent =
            formatarNumero(
                dados.envio_total
            );


        status.textContent = "🟢 ONLINE";

    }

    catch (erro) {

        console.error(
            `Erro ao consultar ${impressoraId}:`,
            erro
        );

        status.textContent = "🔴 OFFLINE";
    }
}


function formatarNumero(valor) {

    const numero = Number(valor);

    if (isNaN(numero)) {
        return valor ?? "N/D";
    }

    return numero.toLocaleString("pt-BR");
}


function gerarPDF(impressoraId) {

    window.open(
        `/pdf/${impressoraId}`,
        "_blank"
    );
}