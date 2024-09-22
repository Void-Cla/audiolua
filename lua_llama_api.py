from flask import Flask, request, jsonify, render_template
from lua_llama import gerar_resposta_llama  # Importa a função que gera resposta da IA
import os  # Importa o módulo os para usar variáveis de ambiente

app = Flask(__name__)

# Rota principal para servir o arquivo HTML
@app.route('/')
def home():
    return render_template('index.html')

# Rota para processar a consulta e retornar a resposta
@app.route('/consultar', methods=['POST'])
def consultar():
    dados = request.json
    query = dados.get('query')

    if not query:
        return jsonify({'erro': 'Nenhuma query fornecida.'}), 400

    # Gera a resposta usando o modelo LLaMA
    resposta = gerar_resposta_llama(query)

    return jsonify({'resposta': resposta})

if __name__ == '__main__':
    # Obtém a porta do ambiente, ou usa 5000 se não estiver definida
    port = int(os.environ.get('PORT', 5000))
    # Inicia o servidor com host 0.0.0.0 para permitir conexões externas
    app.run(debug=True, host='0.0.0.0', port=port)
