from flask import Flask, request, jsonify, render_template
from lua_llama import gerar_resposta_llama  # Importa a função que gera resposta da IA

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
    app.run(debug=True)
