import os
import psycopg
from dotenv import load_dotenv

load_dotenv()


def conectar_banco():
    return psycopg.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )


def salvar_afericao(dados):
    conexao = conectar_banco()

    try:
        with conexao.cursor() as cursor:

            cursor.execute("""
                INSERT INTO afericoes (
                    impressora_id,
                    contador_impressao,
                    contador_copia,
                    contador_fax,
                    contador_relatorio,
                    contador_total,
                    envio_smb,
                    envio_total,
                    serial
                )
                VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s
                )
            """, (
                dados["impressora_id"],
                dados["contador_impressao"],
                dados["contador_copia"],
                dados["contador_fax"],
                dados["contador_relatorio"],
                dados["contador_total"],
                dados["envio_smb"],
                dados["envio_total"],
                dados["serial"]
            ))

        conexao.commit()

        print("✅ Aferição salva com sucesso!")

    except Exception as erro:
        conexao.rollback()
        print("❌ Erro ao salvar aferição:")
        print(erro)

    finally:
        conexao.close()

if __name__ == "__main__":
    salvar_afericao()