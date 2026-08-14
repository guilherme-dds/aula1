from flask import Flask, request, jsonify, render_template
import json
import os

app = Flask(__name__)

# Nome do arquivo onde os dados serão salvos
ARQUIVO_JSON = 'dados.json'

def ler_dados():
    """Lê os dados existentes no arquivo JSON."""
    if not os.path.exists(ARQUIVO_JSON):
        return [] # Retorna uma lista vazia se o arquivo não existir
    
    with open(ARQUIVO_JSON, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def salvar_dados(dados):
    """Salva a lista de dados no arquivo JSON."""
    with open(ARQUIVO_JSON, 'w', encoding='utf-8') as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)

# --- NOVA ROTA ADICIONADA AQUI ---
@app.route('/', methods=['GET'])
def index():
    # Lê os dados atuais para enviar para a tela
    dados = ler_dados()
    return render_template('index.html', dados=dados)
# ---------------------------------

@app.route('/listar', methods=['GET'])
def getDados():
    return json.load(open('dados.json', 'r'))

@app.route('/api/registrar', methods=['POST'])
def registrar():
    # Captura o JSON enviado na requisição
    dados_recebidos = request.get_json()

    # Validação simples para garantir que os campos existem
    if not dados_recebidos or not all(campo in dados_recebidos for campo in ('nome', 'telefone', 'valor')):
        return jsonify({'erro': 'Os campos "nome", "telefone" e "valor" são obrigatórios.'}), 400

    # Cria o novo registro
    novo_registro = {
        'nome': dados_recebidos['nome'],
        'telefone': dados_recebidos['telefone'],
        'valor': dados_recebidos['valor']
    }

    # Lê os dados atuais, adiciona o novo e salva
    lista_dados = ler_dados()
    lista_dados.append(novo_registro)
    salvar_dados(lista_dados)

    return jsonify({
        'mensagem': 'Registro salvo com sucesso!', 
        'registro': novo_registro
    }), 201

if __name__ == '__main__':
    # Roda a aplicação na porta padrão (5000)
    app.run(debug=True)