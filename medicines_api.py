# -*- coding:utf-8 -*-

from flask import Flask, jsonify, url_for, make_response, abort, request
from dbinterface import DBInterface


API_ROUTE = '/gestor'
API_CLIENTS_ROUTE = API_ROUTE + '/medicines'


api = Flask(__name__)

medicines = DBInterface('medicines_db', [
	'name',
	'type',
	'dosage',
	'price',
	'manufacturer', 
	'sold'
])

# Funções auxiliares

def make_public_medicine(medicine):
	'''
	Altera a forma de exibição de um elemento do cadastro.
	Ao invés de mostraro ID do elemento, mostra a URI do mesmo,
	  tornando assim mais fácil a requisição do mesmo via API.
	'''
	new_medicine = {}
	for field in medicine:
		if field == 'id':
			new_medicine['uri'] = url_for('get_medicine', medicine_id=medicine['id'], _external=True)

		else:
			new_medicine[field] = medicine[field]

	return new_medicine


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
def create_medicine():
	'''
	Cria um novo remédio no cadastro com as informações passadas.
	Os dados do remédio sáo passados como JSON, com os seguintes campos:

	* 'name'         : nome do remédio. Valor do campo deve ser uma string. Campo obrigatório.
	* 'type'		 : tipo do remédio. Valor deve ser uma string.
	* 'dosage'		 : dosagem do remédio. Valor deve ser uma string. Campo obrigatório.
	* 'price'		 : preço do remédio. Valor deve ser um float.
	* 'manufacturer' : fabricante do remédio. Valor deve ser uma string. Campo obrigatório.

	Exemplo de requisição:

	curl -i -H 'Content-Type: application/json' -X POST -d '{"name":"Remedio A", "type":"Xarope", "dosage":"10mL", "price":50.0, "manufacturer":"Fabricante X"}' http://localhost:5000/gestor/medicines
	'''
	global medicines

	request_json = request.json
	if not request_json :
		abort(400)

	if 'name' not in request_json or type(request_json['name']) != str:
		abort(400)

	if 'type' in request_json and type(request_json['type']) != str:
		abort(400)

	if 'dosage' not in request_json or type(request_json['dosage']) != str:
		abort(400)

	if 'price' in request_json and type(request_json['price']) != float:
		abort(400)

	if 'manufacturer' not in request_json or type(request_json['manufacturer']) != str:
		abort(400)

	medicine = medicines.create_element({
		'name'			: request_json['name'],
		'type'			: request_json.get('type', ''),
		'dosage'		: request_json['dosage'],
		'price'			: request_json.get('price', 0),
		'manufacturer'	: request_json['manufacturer'],
		'sold'			: 0
	})

	if medicine == -1:
		abort(500)

	return jsonify({'medicine': make_public_medicine(medicine)})


@api.route(API_CLIENTS_ROUTE + '/<int:medicine_id>', methods=['DELETE'])
def delete_medicine(medicine_id):
	'''
	Deleta o remédio cadastrado com o ID passado.

	* medicine_id : inteiro representando o ID do remédio.

	Exemplo de requisição:

	curl -i -X DELETE http://localhost:5000/gestor/medicines/3
	'''
	global medicines

	medicine = medicines.get_element('id', medicine_id)

	if medicine == []:
		abort(404)

	if medicine == -1:
		abort(500)

	if medicines.delete_element('id', medicine_id) == -1:
		abort(500)

	return jsonify({'result': True})


@api.route(API_CLIENTS_ROUTE, methods=['GET'])
def get_all_medicines():
	'''
	Retorna todos os remédios cadastrados.

	Exemplo de requisição:

	curl -i -X GET http://localhost:5000/gestor/medicines
	'''
	global medicines

	public_medicines = [make_public_medicine(medicine) for medicine in medicines.get_all_elements()]

	return jsonify({'medicines': public_medicines})


@api.route(API_CLIENTS_ROUTE + '/<int:medicine_id>', methods=['GET'])
def get_medicine(medicine_id):
	'''
	Retorna o remédio cadastrado com o ID passado

	* medicine_id : inteiro representando o ID do remédio.

	Exemplo de requisição:

	curl -i -X GET http://localhost:5000/gestor/medicines/2
	'''
	global medicines

	medicine = medicines.get_element('id', medicine_id)

	if medicine == []:
		abort(404)

	if medicine == -1:
		abort(500)

	return jsonify({'medicine': make_public_medicine(medicine[0])})


@api.route(API_CLIENTS_ROUTE + '/<int:medicine_id>', methods=['PUT'])
def update_medicine(medicine_id):
	'''
	Atualiza o remédio cadastrado com o ID passado. O ID do remédio é passado via uri do remédio na API, enquanto que os outros dados do mesmo é passado via JSON.

	* 'name'         : nome do remédio. Valor do campo deve ser uma string.
	* 'type'		 : tipo do remédio. Valor deve ser uma string.
	* 'dosage'		 : dosagem do remédio. Valor deve ser uma string.
	* 'price'		 : preço do remédio. Valor deve ser um float.
	* 'manufacturer' : fabricante do remédio. Valor deve ser uma string.
	* 'sold'         : quantidade vendida do remédio. Valor deve ser um inteiro.

	Exemplo:

	curl -i -H 'Content-Type: application/json' -X PUT -d '{"name":"Novo nome", "type":"Novo tipo", "dosage":"30mL", "price":45.0, "manufacturer":"Novo fabricante", "sold":3}' http://localhost:5000/gestor/medicines/1
	'''
	global medicines

	medicine = medicines.get_element('id', medicine_id)

	if medicine == []:
		abort(404)

	if medicine == -1:
		abort(500)

	request_json = request.json
	if not request_json :
		abort(400)

	if 'name' in request_json and type(request_json['name']) != str:
		abort(400)

	if 'type' in request_json and type(request_json['type']) != str:
		abort(400)

	if 'dosage' in request_json and type(request_json['dosage']) != str:
		abort(400)

	if 'price' in request_json and type(request_json['price']) != float:
		abort(400)

	if 'manufacturer' in request_json and type(request_json['manufacturer']) != str:
		abort(400)

	if 'sold' in request_json and type(request_json['sold']) != int:
		abort(400)

	if medicines.update_element(request_json, 'id', medicine_id) == -1:
		abort(500)

	medicine = medicines.get_element('id', medicine_id)
	if medicine == -1:
		abort(500)

	return jsonify({'medicine': make_public_medicine(medicine[0])})


if __name__ == '__main__':
	api.run(debug=True)

