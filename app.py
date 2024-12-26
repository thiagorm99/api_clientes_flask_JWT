from flask import Flask, jsonify, request
from Clientes import Clientes
from datetime import timedelta
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required, get_jwt_identity
)


c = Clientes()
app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = '8df7gfd87gdfg76dfgdf6g787g6e878ew7we86we76ew'
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
jwt = JWTManager(app)


# Rota para buscar todos os clientes
@app.route('/clientes/all', methods=['GET'])
@jwt_required() 
def get_all_clients():
    return jsonify(c.get_all())


# Rota para adicionar um novo cliente
@app.route('/clientes/add', methods=['POST'])
@jwt_required() 
def add_client():
    dados = request.get_json()
    nometxt = dados.get('nome')
    telefonetxt = dados.get('telefone')
    return c.add_client(nome=nometxt, telefone=telefonetxt)


# Rota para editar um cliente existente
@app.route('/clientes/edit/<int:id>', methods=['PUT'])
def edit_client(id):
    dados = request.get_json()
    nometxt = dados.get('nome')
    telefonetxt = dados.get('telefone')
    return c.edit_client(cod=id, nome=nometxt, telefone=telefonetxt)


# Rota para deletar um cliente
@app.route('/clientes/delete/<int:id>', methods=['DELETE'])
def delete_client(id):
    return c.delete_client(cod=id)


# Rota para login
@app.route('/login', methods=['POST'])
def login():
    dados = request.json
    username = dados.get('username')
    password = dados.get('password')

    if username != 'admin' or password != '1234':
        return jsonify({"msg": "Usuário ou senha inválidos"}), 401

    # Gera o token de acesso
    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token)

if __name__ == '__main__':
    app.run(debug=True)