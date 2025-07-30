import os
from flask import Flask, jsonify
import sqlite3

app = Flask(__name__)

CAMINHO_DB = r"\Users\pc\Desktop\projeto correio\api-cpf\database.db"  # Ou um caminho relativo no servidor Render
NOME_TABELA = "registros"

@app.route("/cpf/<cpf>", methods=["GET"])
def consulta_cpf(cpf):
    try:
        conn = sqlite3.connect(CAMINHO_DB)
        cursor = conn.cursor()
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

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
