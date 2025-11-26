from flask import Flask, jsonify, request
from db import Banco

app = Flask(__name__)
db = Banco()

@app.route('/jogadores', methods=['GET'])
def pegar_jogadores():
    dados = db.listar_jogadores()
    lista_formatada = []
    for j in dados:
        lista_formatada.append({
            "id": j[0],
            "nome": j[1],
            "idade": j[2],
            "posicao": j[3],
            "nacionalidade": j[4],
            "time": j[5]
        })
    return jsonify(lista_formatada)

@app.route('/jogadores', methods=['POST'])
def criar_jogador():
    novo = request.json
    try:
        sucesso = db.inserir_jogador(
            novo['nome'], 
            novo['idade'], 
            novo['posicao'], 
            novo['nacionalidade'], 
            novo['time']
        )
        if sucesso:
            return jsonify({"mensagem": "Criado com sucesso"}), 201
        return jsonify({"erro": "Falha ao criar (Nome duplicado?)"}), 400
    except KeyError:
        return jsonify({"erro": "Dados incompletos"}), 400

@app.route('/jogadores/<int:id>', methods=['PUT'])
def atualizar_jogador_api(id):
    dados = request.json
    try:
        sucesso = db.atualizar_jogador(
            id,
            dados['nome'],
            dados['idade'],
            dados['posicao'],
            dados['nacionalidade'],
            dados['time']
        )
        if sucesso:
            return jsonify({"mensagem": "Atualizado com sucesso"}), 200
        return jsonify({"erro": "Jogador não encontrado"}), 404
    except KeyError:
        return jsonify({"erro": "Dados incompletos"}), 400

@app.route('/jogadores/<int:id>', methods=['DELETE'])
def deletar_jogador(id):
    if db.excluir_jogador(id):
        return jsonify({"mensagem": "Deletado"}), 200
    return jsonify({"erro": "Não encontrado"}), 404

if __name__ == '__main__':
    app.run(port=5000)