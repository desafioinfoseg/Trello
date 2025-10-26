# 🚀 Servidor MCP Trello – DesafioInfoSeg

Servidor MCP em **Python (Flask)** para integração com **ChatGPT Agent** (ou Manus AI), permitindo automações diretas com o **Trello**: listar quadros, criar cartões, etc.

---

## 📁 Estrutura do Projeto


---

## 🧰 Requisitos

- Conta **Trello** ativa.  
- **API Key** e **Token** do Trello (https://trello.com/app-key).  
- Conta no **Render.com** (ou similar) para deploy.  
- Python 3.9+ (apenas se quiser rodar localmente).

---

## ⚙️ Variáveis de Ambiente

Defina no Render (ou local):


> **Importante:** a conta vinculada ao `TRELLO_TOKEN` precisa ter acesso aos quadros/listas onde você irá operar.

---

## 📦 Dependências (requirements.txt)


`gunicorn` é recomendado em produção.

---

## 🚀 Deploy no Render

1. Acesse **Render.com** → **New +** → **Web Service**.  
2. Selecione o repositório `desafioinfoseg/Trello`.  
3. Configure:
   - **Environment:** `Python 3`
   - **Build Command:**
     ```
     pip install -r requirements.txt
     ```
   - **Start Command (recomendado):**
     ```
     gunicorn app:app
     ```
   - **Environment Variables:** adicione `TRELLO_KEY`, `TRELLO_TOKEN`, `PORT`.
4. Clique em **Deploy**.  
5. A URL pública ficará algo como:

---

## 🧠 Endpoints

### Health Check
