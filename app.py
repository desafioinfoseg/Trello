from flask import Flask, request, jsonify
import os
import requests

app = Flask(__name__)

# Credenciais do Trello obtidas das variáveis de ambiente
TRELLO_KEY = os.environ.get("TRELLO_KEY")
TRELLO_TOKEN = os.environ.get("TRELLO_TOKEN")

@app.route('/mcp', methods=['POST'])
def mcp_endpoint():
    """
    Endpoint compatível com o ChatGPT Agent (MCP).
    Aceita requisições JSON-RPC contendo um campo 'method'.
    """
    data = request.get_json()
    if not data or "method" not in data:
        return jsonify({"error": "Formato inválido. Esperado campo 'method'."}), 400

    method = data.get("method")
    params = data.get("params", {})

    # === Listar quadros ===
    if method == "list_boards":
        url = f"https://api.trello.com/1/members/me/boards?key={TRELLO_KEY}&token={TRELLO_TOKEN}"
        response = requests.get(url)
        return jsonify({"result": response.json()}), response.status_code

    # === Criar cartão ===
    elif method == "create_card":
        list_id = params.get("list_id")
        name = params.get("name", "Novo Cartão")
        desc = params.get("desc", "")
        if not list_id:
            return jsonify({"error": "Parâmetro 'list_id' é obrigatório"}), 400

        url = "https://api.trello.com/1/cards"
        payload = {
            "idList": list_id,
            "name": name,
            "desc": desc,
            "key": TRELLO_KEY,
            "token": TRELLO_TOKEN
        }
        response = requests.post(url, data=payload)
        return jsonify({"result": response.json()}), response.status_code

    else:
        return jsonify({"error": f"Método '{method}' não suportado"}), 400


@app.route('/health', methods=['GET'])
def health():
    """Verifica se o servidor está rodando."""
    return "OK", 200


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
