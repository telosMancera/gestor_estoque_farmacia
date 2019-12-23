# -*- coding:utf-8 -*-

import re
import csv
import datetime
import jwt
from io import StringIO
from flask import Flask, jsonify, url_for, make_response, abort, request
from werkzeug.security import generate_password_hash, check_password_hash
from dbinterface import DBInterface
from utils import API_ROUTE, API_USERS_ROUTE, API_USERS_PORT, SECRET_KEY, token_required


api = Flask(__name__)
api.config['SECRET_KEY'] = SECRET_KEY

users = DBInterface('users', [
	'username',
	'password',
	'status',
	'admin'
])


# Funções auxiliares

def make_public_user(user):
	'''
	Altera a forma de exibição de um elemento do cadastro.
	Ao invés de mostrar o ID do elemento, mostra a URI do mesmo,
	  tornando assim mais fácil a requisição do mesmo via API.
	'''
	new_user = {}
	for field in user:
		if field == 'id':
			new_user['uri'] = url_for('get_user', user_id=user['id'], _external=True)

		else:
			new_user[field] = user[field]

	return new_user


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

@api.route(API_USERS_ROUTE + '/<user_id>/activate', methods=['PUT'])
@token_required
def activate_user(current_user, user_id):
	'''
	Ativa o usúario com o ID passado.
	'''
	global users

	if not current_user['admin']:
		return jsonify({'message': 'You don\'t have permission for that!'})

	user = users.get_element('id', user_id)
	if user == []:
		abort(404)

	if user == -1:
		abort(500)

	if users.update_element({'status': 'active'}, 'id', user_id) == -1:
		abort(500)

	user = users.get_element('id', user_id)
	if user == -1:
		abort(500)

	return jsonify({'user': make_public_user(user[0])})


@api.route(API_USERS_ROUTE + '/<user_id>/deactivate', methods=['PUT'])
@token_required
def deactivate_user(current_user, user_id):
	'''
	Desativa o usúario com o ID passado.
	'''
	global users

	if not current_user['admin']:
		return jsonify({'message': 'You don\'t have permission for that!'})

	user = users.get_element('id', user_id)
	if user == []:
		abort(404)

	if user == -1:
		abort(500)

	if user[0]['admin']:
		abort(400)

	if users.update_element({'status': 'inactive'}, 'id', user_id) == -1:
		abort(500)

	user = users.get_element('id', user_id)
	if user == -1:
		abort(500)

	return jsonify({'user': make_public_user(user[0])})


@api.route(API_USERS_ROUTE + '/<user_id>', methods=['DELETE'])
@token_required
def delete_user(current_user, user_id):
	'''
	Deleta o usuário com o ID passado.
	'''
	global users

	if not current_user['admin']:
		return jsonify({'message': 'You don\'t have permission for that!'})

	user = users.get_element('id', user_id)
	if user == []:
		abort(404)

	if user == -1:
		abort(500)

	if user[0]['admin']:
		abort(400)

	if users.delete_element('id', user_id) == -1:
		abort(500)

	return jsonify({'message': 'User deleted sucessfully!'})


@api.route(API_USERS_ROUTE, methods=['GET'])
@token_required
def get_all_users(current_user):
	'''
	Obtém a lista de todos os usuários.
	'''
	global users

	if not current_user['admin']:
		return jsonify({'message': 'You don\'t have permission for that!'})

	public_users = [make_public_user(user) for user in users.get_all_elements()]

	return jsonify({'users': public_users})


@api.route(API_USERS_ROUTE + '/<user_id>', methods=['GET'])
@token_required
def get_user(current_user, user_id):
	'''
	Retorna o usuário com o ID passado.
	'''
	global users

	if not current_user['admin']:
		return jsonify({'message': 'You don\'t have permission for that!'})

	user = users.get_element('id', user_id)
	if user == []:
		abort(404)

	if user == -1:
		abort(500)

	return jsonify({'user': make_public_user(user[0])})


@api.route(API_ROUTE + '/login', methods=['POST'])
def login():
	'''
	Realiza o login na API para receber o token
	'''
	global users

	auth = request.authorization
	if not auth:
		abort(400)

	if auth.username == '' or auth.password == '':
		abort(400)

	user = users.get_element('username', auth.username)
	if user == -1:
		abort(500)

	if user == []:
		abort(404)

	user = user[0]
	if not check_password_hash(user['password'], auth.password):
		abort(400)

	payload = {
			'id'		: user['id'],
			'status'	: user['status'],
			'admin'		: user['admin'],
			'exp'		: datetime.datetime.utcnow() + datetime.timedelta(minutes=10)
	}
	key = api.config['SECRET_KEY']
	token = jwt.encode(payload, key)

	return jsonify({'token': token.decode('UTF-8')})


@api.route(API_USERS_ROUTE + '/<user_id>/promote', methods=['PUT'])
@token_required
def promote_user(current_user, user_id):
	'''
	Promove o usuário com o ID passado para amdin.
	'''
	global users

	if not current_user['admin']:
		return jsonify({'message': 'You don\'t have permission for that!'})

	user = users.get_element('id', user_id)
	if user == []:
		abort(404)

	if user == -1:
		abort(500)

	if users.update_element({'admin': True}, 'id', user_id) == -1:
		abort(500)

	user = users.get_element('id', user_id)
	if user == -1:
		abort(500)

	return jsonify({'user': make_public_user(user[0])})


@api.route(API_ROUTE + '/register', methods=['POST'])
def register():
	'''
	Cadastra um novo usuário
	'''
	global users

	request_json = request.json
	if not request_json:
		abort(400)

	username = request_json.get('username', '')
	if not username or type(username) != str:
		abort(400)

	password = request_json.get('password', '')
	if not password or type(password) != str:
		abort(400)

	user = users.get_element('username', username)
	if user != []:
		abort(501)

	user = users.create_element({
		'username'	: username,
		'password'	: generate_password_hash(password, method='sha256'),
		'status'	: 'active',
		'admin'		: True if users.get_all_elements() == [] else False
	})

	if user == -1:
		abort(500)

	return make_response('User registered sucessfully!', 200)

@api.route(API_ROUTE + '/selfupdate', methods=['PUT'])
@token_required
def self_update(current_user):
	'''
	Altera os dados do usuário.
	'''
	global users

	request_json = request.json
	if not request_json:
		abort(400)

	username = request_json.get('username', '')
	if username and type(username) != str:
		abort(400)

	password = request_json.get('password', '')
	if password and type(password) != str:
		abort(400)

	user = users.get_element('id', current_user['id'])
	if user == -1:
		abort(500)

	if user == []:
		abort(500)

	user = user[0]
	new_values = {
		'username'	: username if username else user['username'],
		'password'	: generate_password_hash(password, method='sha256') if password else user['username']
	}
	user = users.update_element(new_values, 'id', current_user['id'])
	if user == -1:
		abort(500)

	return make_response('User updated sucessfully!', 200)


if __name__ == '__main__':
	api.run(port=API_USERS_PORT, debug=True)

