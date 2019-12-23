# -*- coding:utf-8 -*-

import re
import csv
from io import StringIO
from flask import Flask, jsonify, url_for, make_response, abort, request
from werkzeug.utils import secure_filename
from dbinterface import DBInterface
from utils import API_MEDICINES_ROUTE, API_MEDICINES_PORT, token_required


api = Flask(__name__)

medicines = DBInterface('medicines', [
	'name',
	'type',
	'dosage',
	'price',
	'manufacturer', 
	'sales'
])

# Funções auxiliares

def make_public_medicine(medicine):
	'''
	Altera a forma de exibição de um elemento do cadastro.
	Ao invés de mostrar o ID do elemento, mostra a URI do mesmo,
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

@api.route(API_MEDICINES_ROUTE, methods=['POST'])
@token_required
def create_medicine(current_user):
	'''
	Cria um novo remédio no cadastro com as informações passadas.
	Os dados do remédio sáo passados como JSON, com os seguintes campos:

	* medicine_id    : ID do remédio. Valor deve ser um inteiro.

	* 'name'         : nome do remédio. Valor do campo deve ser uma string. Campo obrigatório.
	* 'type'		 : tipo do remédio. Valor deve ser uma string.
	* 'dosage'		 : dosagem do remédio. Valor deve ser uma string. Campo obrigatório.
	* 'price'		 : preço do remédio. Valor deve ser um float.
	* 'manufacturer' : fabricante do remédio. Valor deve ser uma string. Campo obrigatório.

	Exemplo de requisição:

	curl -i -H 'Content-Type: application/json' -X POST -d '{"name":"Remedio A", "type":"Xarope", "dosage":"10mL", "price":50.0, "manufacturer":"Fabricante X"}' http://localhost:5001/gestor/medicines
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
		'sales'			: {}
	})

	if medicine == -1:
		abort(500)

	return jsonify({'medicine': make_public_medicine(medicine)})


@api.route(API_MEDICINES_ROUTE + '/<int:medicine_id>', methods=['DELETE'])
@token_required
def delete_medicine(current_user, medicine_id):
	'''
	Deleta o remédio cadastrado com o ID passado.

	* medicine_id    : ID do remédio. Valor deve ser um inteiro.

	Exemplo de requisição:

	curl -i -X DELETE http://localhost:5001/gestor/medicines/3
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


@api.route(API_MEDICINES_ROUTE, methods=['GET'])
@token_required
def get_all_medicines(current_user):
	'''
	Retorna todos os remédios cadastrados.

	Exemplo de requisição:

	curl -i -X GET http://localhost:5001/gestor/medicines
	'''
	global medicines

	public_medicines = [make_public_medicine(medicine) for medicine in medicines.get_all_elements()]

	return jsonify({'medicines': public_medicines})


@api.route(API_MEDICINES_ROUTE + '/<int:medicine_id>', methods=['GET'])
@token_required
def get_medicine(current_user, medicine_id):
	'''
	Retorna o remédio cadastrado com o ID passado

	* medicine_id    : ID do remédio. Valor deve ser um inteiro.

	Exemplo de requisição:

	curl -i -X GET http://localhost:5001/gestor/medicines/2
	'''
	global medicines

	medicine = medicines.get_element('id', medicine_id)

	if medicine == []:
		abort(404)

	if medicine == -1:
		abort(500)

	return jsonify({'medicine': make_public_medicine(medicine[0])})


@api.route(API_MEDICINES_ROUTE + '/mostconsumed', methods=['GET'])
#@token_required
def get_most_consumed_medicines():
	'''
	Retorna os remédios mais consumidos em uma período passado. Os argumentos da pesquisa são passados via JSON.

	* "most"  : número de elementos na resposta. Valor deve ser um inteiro. Caso este campo não seja passado, o método retornará todos os remédios.
	* "begin" : início do intervalo da pesquisa. Valor deve ser uma string. Caso não seja passado, o método considerará a venda mais antiga como início.
	* "end"   : fim do intervalo da pesquisa. Valor deve ser uma string. Caso não seja passado, o método assumirá a venda mais recente como fim.
	* "csv"   : flag indicando se o retorno deve ser em arquivo csv. Para retornar em arquivo, "csv" deve ter como valor o inteiro 1. Caso não seja igual a 1, ou não haja este campo, o retorno do método será no formato JSON.

	As datas de início e fim do intervalo devem ser strings no formato "aaaammdd", sendo:

	* aaaa : dígitos do ano.
	* mm   : dígitos do mês.
	* dd   : dígitos do dia.

	Exemplo de requisição:

	curl -i -H 'Content-Type: application/json' -X GET -d '{"most":2, "begin":"20191115", "end":"20191121"}' http://localhost:5001/gestor/medicines/mostconsumed
	'''
	request_json = request.json if request.json else {}

	if 'most' in request_json and type(request_json['most']) != int:
		abort(400)

	if 'begin' in request_json and re.search('^\d{8}$', request_json['begin']) == None:
		abort(400)

	if 'end' in request_json and re.search('^\d{8}$', request_json['end']) == None:
		abort(400)

	if 'csv' in request_json and type(request_json['csv']) != int:
		abort(400)

	most = request_json.get('most', 100)
	begin = int(request_json.get('begin', '0'))
	end = int(request_json.get('end', '99999999'))

	minor_date = 99999999
	major_date = 0
	for medicine in medicines.get_all_elements():
		sales = medicine['sales']
		minor = min((int(date) for date in sales), default=minor_date)
		minor_date = min(minor_date, minor)
		major = max((int(date) for date in sales), default=major_date)
		major_date = max(major_date, major)

	# Uma vez descobertas as datas mais recente e mais remota entre todos os remédios, calcula-se o intervalo final de consulta
	begin = max(begin, minor_date)
	end = min(end, major_date)

	mostconsumed = []
	for medicine in medicines.get_all_elements():
		sales = medicine['sales']
		if sales == {}:
			continue

		sales_in_interval = [quantity for date, quantity in sales.items() if begin <= int(date) <= end]
		quantity = sum(sales_in_interval, start=0)
		if quantity == 0:
			continue

		d = {}
		d['id'] = medicine['id']
		d['name'] = medicine['name']
		d['quantity'] = quantity
		mostconsumed.append(make_public_medicine(d))

	mostconsumed = sorted(mostconsumed, key=lambda medicine : medicine['quantity'], reverse=True)[:most]

	if 'csv' not in request_json or request_json['csv'] == 0:
		return jsonify({'medicines': mostconsumed})

	if mostconsumed == []:
		abort(500)

	with StringIO() as sio:
		writer = csv.writer(sio)

		# 1a linha deve conter os campos dos dicionários
		writer.writerow(mostconsumed[0].keys())
		# As linhas subsequentes são os dados de cada remédio
		for medicine in mostconsumed:
			writer.writerow(medicine.values())

		response = make_response(sio.getvalue())
		response.headers['Content-Disposition'] = 'attachment; filename=mostconsumed.csv'
		response.headers['Content-Type'] = 'text/csv'

	return response


@api.route(API_MEDICINES_ROUTE + '/<int:medicine_id>', methods=['PUT'])
@token_required
def update_medicine(current_user, medicine_id):
	'''
	Atualiza o remédio cadastrado com o ID passado. O ID do remédio é passado via URI do remédio na API, enquanto que os outros dados do mesmo é passado via JSON.

	O campo 'sales' não é atualizado via este método. Para tal, o método update_medicine_sales é utilizado.

	* medicine_id    : ID do remédio. Valor deve ser um inteiro.

	* 'name'         : nome do remédio. Valor do campo deve ser uma string.
	* 'type'		 : tipo do remédio. Valor deve ser uma string.
	* 'dosage'		 : dosagem do remédio. Valor deve ser uma string.
	* 'price'		 : preço do remédio. Valor deve ser um float.
	* 'manufacturer' : fabricante do remédio. Valor deve ser uma string.

	Exemplo:

	curl -i -H 'Content-Type: application/json' -X PUT -d '{"name":"Novo nome", "type":"Novo tipo", "dosage":"30mL", "price":45.0, "manufacturer":"Novo fabricante"}' http://localhost:5001/gestor/medicines/1
	'''
	global medicines

	medicine = medicines.get_element('id', medicine_id)

	if medicine == []:
		abort(404)

	if medicine == -1:
		abort(500)

	request_json = request.json
	if not request_json:
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

	request_json.pop('sales', None)
	medicine = medicines.update_element(request_json, 'id', medicine_id)
	if medicine == -1:
		abort(500)

	return jsonify({'medicine': make_public_medicine(medicine[0])})


@api.route(API_MEDICINES_ROUTE + '/<int:medicine_id>/sales', methods=['PUT'])
@token_required
def update_medicine_sales(current_user, medicine_id):
	'''
	Atualiza o registro de vendas do remédio com o ID passado. O ID do remédio é passado via URI, enquanto que o registro de vendas é passado no formato JSON.

	* medicine_id    : ID do remédio. Valor deve ser um inteiro.

	O registro de vendas é passado no formato JSON, onde cada chave é data da venda, e o valor para a chave é a quantidade de unidades do remédio vendida nesta data. Caso a quantidade para uma data seja 0, o registro desta data é apagado.

	A data deve ser uma string no formato 'aaaammdd', sendo:

	* aaaa : dígitos do ano.
	* mm   : dígitos do mês.
	* dd   : dígitos do dia.

	Exemplo de requisição:

	curl -i -H 'Content-Type: application/json' -X PUT -d '{"20191220":3, "20191223":1}' http://localhost:5001/gestor/medicines/2
	'''
	global medicines

	medicine = medicines.get_element('id', medicine_id)

	if medicine == []:
		abort(404)

	if medicine == -1:
		abort(500)

	request_json = request.json
	if not request_json:
		abort(400)

	if type(request_json) != dict:
		abort(400)

	if any(re.search('^\d{8}$', key) == None for key in request_json):
		abort(400)

	if any(type(value) != int for value in request_json.values()):
		abort(400)

	new_sales = {**medicine[0]['sales'], **request_json}
	new_sales = {k: v for k, v in new_sales.items() if v != 0}

	medicine = medicines.update_element({'sales': new_sales}, 'id', medicine_id)
	if medicine == -1:
		abort(500)

	return jsonify({'medicine': make_public_medicine(medicine[0])})


@api.route(API_MEDICINES_ROUTE + '/sales', methods=['POST'])
@token_required
def update_medicines_sales_with_csv(current_user):
	'''
	Atualiza o registro de venda dos remédios com um arquivo CSV.

	A primeira linha do arquivo deve conter a palavra 'id' e as outras colunas devem conter as datas a serem alteradas. Nas linhas subsequentes devem-se colocar o ID do remédio na primeira coluna, e os novos valores de vendas para cada data nas outras colunas.

	Caso em alguma data deseja-se manter o valor de venda atual, deixe o campo vazio. Caso a quantidade para uma data seja 0, o registro desta data é apagado.

	As datas devem ser uma string no formato 'aaaammdd', sendo:

	* aaaa : dígitos do ano.
	* mm   : dígitos do mês.
	* dd   : dígitos do dia.
	'''
	global medicines

	csvfile = request.files['file']
	with StringIO(csvfile.read().decode()) as sio:
		content = list(csv.reader(sio))

	keys = content[0]
	if 'id' not in keys:
		abort(400)

	if any(re.search('^\d{8}$', key) == None for key in keys[1:]):
		abort(400)

	updatelist = [{k: v for k, v in zip(keys, values)} for values in content[1:]]
	new_medicines = []
	for update in updatelist:
		medicine_id = int(update.pop('id', ''))
		medicine = medicines.get_element('id', medicine_id)

		if medicine == []:
			abort(404)

		if medicine == -1:
			abort(500)

		for date, quantity in update.items():
			if quantity == '':
				update[date] = medicine[0]['sales'].get(date, 0)

			else:
				try:
					update[date] = int(quantity)

				except Exception:
					abort(400)

		new_sales = {**medicine[0]['sales'], **update}
		new_sales = {k: v for k, v in new_sales.items() if v != 0}

		medicine = medicines.update_element({'sales': new_sales}, 'id', medicine_id)
		if medicine == -1:
			abort(500)

		new_medicines.append(make_public_medicine(medicine[0]))

	return jsonify({'medicines' : new_medicines})


@api.route(API_MEDICINES_ROUTE + '/update', methods=['POST'])
@token_required
def update_medicines_with_csv(current_user):
	'''
	Atualiza o banco de dados dos remédios com um arquivo CSV.

	A primeira linha deve conter a palavra 'id' e as outras colunas devem conter os nomes dos campos a serem alterados. Nas linhas subsequentes devem-se colocar o ID do remédio na primeira coluna, e os novos valores para cada campo nas outras colunas.

	* 'name'         : nome do remédio. Valor do campo deve ser uma string.
	* 'type'		 : tipo do remédio. Valor deve ser uma string.
	* 'dosage'		 : dosagem do remédio. Valor deve ser uma string.
	* 'price'		 : preço do remédio. Valor deve ser um float.
	* 'manufacturer' : fabricante do remédio. Valor deve ser uma string.
	'''
	global medicines

	csvfile = request.files['file']
	with StringIO(csvfile.read().decode()) as sio:
		content = list(csv.reader(sio))

	keys = content[0]
	if 'id' not in keys:
		abort(400)

	updatelist = [{k: v for k, v in zip(keys, values)} for values in content[1:]]
	new_medicines = []
	for update in updatelist:
		medicine_id = int(update.pop('id', ''))
		medicine = medicines.get_element('id', medicine_id)
		if medicine == []:
			abort(404)

		if medicine == -1:
			abort(500)

		if 'name' in update and type(update['name']) != str:
			abort(400)

		if 'type' in update and type(update['type']) != str:
			abort(400)

		if 'dosage' in update and type(update['dosage']) != str:
			abort(400)

		if 'price' in update and update['price'] != '':
			try:
				update['price'] = float(update['price'])

			except Exception:
				abort(400)

		if 'manufacturer' in update and type(update['manufacturer']) != str:
			abort(400)

		update = {k: v for k, v in update.items() if v != ''}

		medicine = medicines.update_element(update, 'id', medicine_id)
		if medicine == -1:
			abort(500)

		new_medicines.append(make_public_medicine(medicine[0]))

	return jsonify({'medicines' : new_medicines})


if __name__ == '__main__':
	api.run(port=API_MEDICINES_PORT, debug=True)

