from flask import Flask, jsonify
import sqlite3

app = Flask(__name__)

# Caminho do banco SQLite (confirme o caminho correto no seu projeto)
CAMINHO_DB = r"C:\Users\pc\Downloads\dump\db\database.db"
NOME_TABELA = "registros"

@app.route("/cpf/<cpf>", methods=["GET"])
def consulta_cpf(cpf):
    try:
        conn = sqlite3.connect(CAMINHO_DB)
        cursor = conn.cursor()

        # Consulta parametrizada para evitar SQL Injection
        query = f"SELECT cpf, nome, sexo, nascimento FROM {NOME_TABELA} WHERE cpf = ?"
        cursor.execute(query, (cpf,))
        resultado = cursor.fetchone()
        conn.close()

        if resultado:
            return jsonify({
                "cpf": resultado[0],
                "nome": resultado[1],
                "sexo": resultado[2],
                "data_nascimento": resultado[3]
            })
        else:
            return jsonify({"erro": "CPF não encontrado"}), 404

    except Exception as e:
        return jsonify({"erro": f"Erro no banco: {str(e)}"}), 500

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # pega a porta do ambiente ou usa 5000
    print(f"🚀 API rodando em http://0.0.0.0:{port}")
    app.run(host="0.0.0.0", port=port, debug=True)


