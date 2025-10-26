from flask import Flask, request, jsonify
import os
import requests

app = Flask(__name__)

# === Credenciais do Trello ===
TRELLO_KEY = os.environ.get("TRELLO_KEY")
TRELLO_TOKEN = os.environ.get("TRELLO_TOKEN")

# === Função auxiliar ===
def listar_quadros():
    """Lista os quadros do Trello do usuário autenticado."""
    url = f"https://api.trello.com/1/members/me/boards?key={TRELLO_KEY}&token={TRELLO_TOKEN}"
    response = requests.get(url)
    return response.json(), response.status_code


# === Endpoint MCP (ChatGPT Agent / Manus AI) ===
@app.route('/mcp', methods=['POST'])
def mcp_endpoint():
    """
    Endpoint padrão compatível com ChatGPT Agent (MCP).
    Recebe requisições JSON contendo um campo 'method' e, opcionalmente, 'params'.
    """
    data = request.get_json()
    if not data or "method" not in data:
        return jsonify({"error": "Formato inválido. Esperado campo 'method'."}), 400

    method = data.get("method")
    params = data.get("params", {})

    # === Listar quadros ===
    if method == "list_boards":
        result, status = listar_quadros()
        return jsonify({"result": result}), status

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


# === Endpoint alternativo de teste via navegador ===
@app.route('/trello/resource', methods=['GET'])
def trello_resource():
    """
    Permite testar pelo navegador via GET:
    https://servidor-mcp-trello.onrender.com/trello/resource?action=list_boards
    """
    action = request.args.get("action")
    if action == "list_boards":
        result, status = listar_quadros()
        return jsonify(result), status
    return jsonify({"error": "Ação não suportada. Use action=list_boards"}), 400


# === Health Check ===
@app.route('/health', methods=['GET'])
def health():
    """Verifica se o servidor está ativo."""
    return "OK", 200


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
