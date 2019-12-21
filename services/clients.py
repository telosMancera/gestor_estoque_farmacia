# -*- coding:utf-8 -*-

from flask import Flask, jsonify, url_for, make_response, abort, request
from dbinterface import DBInterface


API_ROUTE = '/gestor'
API_CLIENTS_ROUTE = API_ROUTE + '/clients'

API_CLIENTS_PORT = 5002


api = Flask(__name__)

clients = DBInterface('clients', [
	'name',
	'phonenumber',
	'medicines'
])

# Funções auxiliares

def make_public_client(client):
	'''
	Altera a forma de exibição de um elemento do cadastro.
	Ao invés de mostraro ID do elemento, mostra a URI do mesmo,
	  tornando assim mais fácil a requisição do mesmo via API.
	'''
	new_client = {}
	for field in client:
		if field == 'id':
			new_client['uri'] = url_for('get_client', client_id=client['id'], _external=True)

		else:
			new_client[field] = client[field]

	return new_client


# Tratamento dos erros

@api.errorhandler(400)
def bad_request(error):
	'''
	Altera o retorno para erros tipo 400 para o formato JSON.
	'''
	return make_response(jsonify({'error': 'Bad request'}), 400)


@api.errorhandler(404)
def not_found(error):
	'''
	Altera o retorno para erros tipo 404 para o formato JSON.
	'''
	return make_response(jsonify({'error': 'Not found'}), 404)


@api.errorhandler(500)
def internal_server_error(error):
	'''
	Altera o retorno para erros tipo 500 para o formato JSON.
	'''
	return make_response(jsonify({'error': 'Internal Server Error'}), 500)


# Métodos da API

@api.route(API_CLIENTS_ROUTE, methods=['POST'])
def create_client():
	'''
	Cria um novo cliente no cadastro com as informações passadas.
	Os dados do cliente sáo passados como JSON, com os seguintes campos:

	* 'name'        : nome do cliente. Valor do campo deve ser uma string. Campo obrigatório.
	* 'phonenumber' : número do telefone do cliente. Valor do campo deve ser uma string.

	Exemplo de requisição:

	curl -i -H 'Content-Type: application/json' -X POST -d '{"name":"Cliente A","phonenumber":"+5516999999999"}' http://localhost:5002/gestor/clients
	'''
	global clients

	request_json = request.json
	if not request_json :
		abort(400)

	if 'name' not in request_json or type(request_json['name']) != str:
		abort(400)

	if 'phonenumber' in request_json and type(request_json['phonenumber']) != str:
		abort(400)

	client = clients.create_element({
		'name'			: request_json['name'],
		'phonenumber'	: request_json.get('phonenumber', ''),
		'medicines'		: []
	})

	if client == -1:
		abort(500)

	return jsonify({'client': make_public_client(client)})


@api.route(API_CLIENTS_ROUTE + '/<int:client_id>', methods=['DELETE'])
def delete_client(client_id):
	'''
	Deleta o cliente cadastrado com o ID passado.

	* client_id : inteiro representando o ID do cliente.

	Exemplo de requisição:

	curl -i -X DELETE http://localhost:5002/gestor/clients/3
	'''
	global clients

	client = clients.get_element('id', client_id)

	if client == []:
		abort(404)

	if client == -1:
		abort(500)

	if clients.delete_element('id', client_id) == -1:
		abort(500)

	return jsonify({'result': True})


@api.route(API_CLIENTS_ROUTE, methods=['GET'])
def get_all_clients():
	'''
	Retorna todos os clientes cadastrados.

	Exemplo de requisição:

	curl -i -X GET http://localhost:5002/gestor/clients
	'''
	global clients

	public_clients = [make_public_client(client) for client in clients.get_all_elements()]

	return jsonify({'clients': public_clients})


@api.route(API_CLIENTS_ROUTE + '/<int:client_id>', methods=['GET'])
def get_client(client_id):
	'''
	Retorna o cliente cadastrado com o ID passado

	* client_id : inteiro representando o ID do cliente.

	Exemplo de requisição:

	curl -i -X GET http://localhost:5002/gestor/clients/2
	'''
	global clients

	client = clients.get_element('id', client_id)

	if client == []:
		abort(404)

	if client == -1:
		abort(500)

	return jsonify({'client': make_public_client(client[0])})


@api.route(API_CLIENTS_ROUTE + '/<int:client_id>', methods=['PUT'])
def update_client(client_id):
	'''
	Atualiza o cliente cadastrado com o ID passado. O ID do cliente é passado via uri do cliente na API, enquanto que os outros dados do mesmo é passado via JSON.

	* client_id : inteiro representando o ID do cliente
	* 'name'        : nome do cliente. Valor do campo deve ser uma string.
	* 'phonenumber' : número do telefone do cliente. Valor do campo deve ser uma string.
	* 'medicines'   : remédios comprados pelo cliente. medicines deve ser uma lista de dicionários, sendo que cada dicionário deve apresentar os campos 'uri' e 'quantity'.
	  * 'uri'       : URI do remédio no cadastro dos remédios.
	  * 'quantity'  : quantidade deste remédio consumido pelo cliente. Valor deve ser um inteiro.

	Exemplo:

	curl -i -H 'Content-Type: application/json' -X PUT -d '{"name":"novo nome","phonenumber":"88888888","medicines":[{"uri":"http://localhost:5002/gestor/medicines/1","quantity":2}]}' http://localhost:5002/gestor/clients/1
	'''
	global clients

	client = clients.get_element('id', client_id)

	if client == []:
		abort(404)

	if client == -1:
		abort(500)

	request_json = request.json
	if not request_json :
		abort(400)

	if 'name' in request_json and type(request_json['name']) != str:
		abort(400)

	if 'phonenumber' in request_json and type(request_json['phonenumber']) != str:
		abort(400)

	if 'medicines' in request_json:
		medicines = request_json['medicines']
		if type(medicines) != list:
			abort(400)

		else:
			for medicine in medicines:
				if type(medicine) != dict:
					abort(400)

				elif 'quantity' not in medicine or 'uri' not in medicine:
					abort(400)

				elif type(medicine['uri']) != str or type(medicine['quantity']) != int:
					abort(400)

	if clients.update_element(request_json, 'id', client_id) == -1:
		abort(500)

	client = clients.get_element('id', client_id)
	if client == -1:
		abort(500)

	return jsonify({'client': make_public_client(client[0])})


if __name__ == '__main__':
	api.run(port=API_CLIENTS_PORT, debug=True)

