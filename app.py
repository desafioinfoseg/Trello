from flask import Flask, request, jsonify, send_from_directory, make_response
import os
import requests

app = Flask(__name__)

# ============================================================
# === CONFIGURAÇÃO DO SERVIDOR MCP (ChatGPT Agent + Trello) ===
# ============================================================

# === Credenciais do Trello ===
# (Adicione no Render: Environment → TRELLO_KEY / TRELLO_TOKEN)
TRELLO_KEY = os.environ.get("TRELLO_KEY")
TRELLO_TOKEN = os.environ.get("TRELLO_TOKEN")

# ============================================================
# === SERVIR MANIFESTO E OPENAPI (necessário para ChatGPT) ===
# ============================================================

@app.route('/.well-known/ai-plugin.json')
def serve_manifest():
    """Fornece o manifesto para o ChatGPT (Actions)"""
    resp = make_response(send_from_directory('.well-known', 'ai-plugin.json', mimetype='application/json'))
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

@app.route('/openapi.json')
def serve_openapi():
    """Fornece o arquivo OpenAPI com a descrição dos endpoints"""
    resp = make_response(send_from_directory('.', 'openapi.json', mimetype='application/json'))
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


# ============================================================
# === FUNÇÕES AUXILIARES PARA OPERAÇÕES NO TRELLO ============
# ============================================================

def listar_quadros():
    """Lista os quadros do Trello do usuário autenticado."""
    url = f"https://api.trello.com/1/members/me/boards?key={TRELLO_KEY}&token={TRELLO_TOKEN}"
    response = requests.get(url)
    return response.json(), response.status_code


def criar_cartao(list_id, name, desc=""):
    """Cria um cartão em uma lista do Trello."""
    url = "https://api.trello.com/1/cards"
    payload = {
        "idList": list_id,
        "name": name,
        "desc": desc,
        "key": TRELLO_KEY,
        "token": TRELLO_TOKEN
    }
    response = requests.post(url, data=payload)
    return response.json(), response.status_code


# ============================================================
# === ENDPOINT MCP (usado pelo ChatGPT Agent ou Manus AI) ====
# ============================================================

@app.route('/mcp', methods=['POST'])
def mcp_endpoint():
    """
    Endpoint padrão compatível com ChatGPT Agent (MCP).
    Recebe requisições JSON contendo 'method' e 'params'.
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
        result, status = criar_cartao(list_id, name, desc)
        return jsonify({"result": result}), status

    # === Método não suportado ===
    else:
        return jsonify({"error": f"Método '{method}' não suportado"}), 400


# ============================================================
# === ENDPOINT DE TESTE VIA NAVEGADOR ========================
# ============================================================

@app.route('/trello/resource', methods=['GET'])
def trello_resource():
    """
    Permite testar pelo navegador:
    https://servidor-mcp-trello.onrender.com/trello/resource?action=list_boards
    """
    action = request.args.get("action")
    if action == "list_boards":
        result, status = listar_quadros()
        return jsonify(result), status
    return jsonify({"error": "Ação não suportada. Use action=list_boards"}), 400


# ============================================================
# === HEALTH CHECK (para Render e testes) ====================
# ============================================================

@app.route('/health', methods=['GET'])
def health():
    """Verifica se o servidor está ativo."""
    return "OK", 200


# ============================================================
# === EXECUÇÃO LOCAL =========================================
# ============================================================

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
