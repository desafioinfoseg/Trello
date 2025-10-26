from flask import Flask, request, jsonify
import os
import requests

app = Flask(__name__)

# Credenciais do Trello via variáveis de ambiente
TRELLO_KEY = os.environ.get("TRELLO_KEY")
TRELLO_TOKEN = os.environ.get("TRELLO_TOKEN")

@app.route('/mcp', methods=['POST'])
def mcp_endpoint():
    """
    Endpoint compatível com o padrão MCP (JSON-RPC).
    Permite que o ChatGPT Agent interaja com o Trello.
    """
    data = request.get_json()

    # Identifica o método solicitado pelo ChatGPT
    method = data.get("method")
    params = data.get("params", {})

    # === LISTAR QUADROS ===
    if method == "list_boards":
        url = f"https://api.trello.com/1/members/me/boards?key={TRELLO_KEY}&token={TRELLO_TOKEN}"
        resp = requests.get(url)
        return jsonify({"result": resp.json()})

    # === CRIAR CARTÃO ===
    if method == "create_card":
        name = params.get("name", "Novo Cartão")
        list_id = params.get("list_id")
        desc = params.get("desc", "")

        if not list_id:
            return jsonify({"error": "list_id é obrigatório"}), 400

        url = f"https://api.trello.com/1/cards"
        payload = {
            "idList": list_id,
            "name": name,
            "desc": desc,
            "key": TRELLO_KEY,
            "token": TRELLO_TOKEN
        }
        resp = requests.post(url, data=payload)
        return jsonify({"result": resp.json()})

    # === MÉTODO DESCONHECIDO ===
    return jsonify({"error": f"Método '{method}' não suportado"}), 400

@app.route('/health', methods=['GET'])
def health_check():
    return "OK", 200

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
