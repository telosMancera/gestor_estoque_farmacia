# -*- coding:utf-8 -*-

import re
import csv
import datetime
import jwt
from io import StringIO
from flask import Flask, jsonify, url_for, make_response, abort, request
from dbinterface import DBInterface
from utils import API_USERS_ROUTE, API_USERS_PORT, SECRET_KEY


api = Flask(__name__)
api.config['SECRET_KEY'] = SECRET_KEY

users = DBInterface('users', [
	'login',
	'password',
	'status'
])


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

@api.route(API_USERS_ROUTE + '/login', methods=['POST'])
def login():
	'''
	Realiza o login na API para receber o token
	'''
	auth = request.authorization
	if not auth:
		abort(400)

	if auth.username == '' or auth.password == '':
		abort(400)

	user = users.get_element('login', auth.username)
	if user == -1:
		abort(500)

	if user == []:
		abort(404)

	# FIXME : encriptar senha
	if auth.password != user[0]['password']:
		abort(400)

	payload = {
			'user'	: auth.username,
			'exp'	: datetime.datetime.utcnow() + datetime.timedelta(seconds=20)
	}
	key = api.config['SECRET_KEY']
	token = jwt.encode(payload, key)

	return jsonify({'token': token.decode('UTF-8')})


@api.route(API_USERS_ROUTE + '/register', methods=['POST'])
def register():
	'''
	Cadastra um novo usuário
	'''
	request_json = request.json
	if not request_json:
		abort(400)

	if 'login' not in request_json or type(request_json['login']) != str:
		abort(400)

	if 'password' not in request_json or type(request_json['password']) != str:
		abort(400)

	user = users.get_element('login', request_json['login'])
	if user != []
		abort(501)

	user = users.create_element({
		'login'		: request_json['login'],
		# FIXME : encriptar senha
		'password'	: request_json['password'],
		'status'	: 'inactive'
	})

	if user == -1:
		abort(500)

	return make_response('User registered sucessfully!', 200)


if __name__ == '__main__':
	api.run(port=API_USERS_PORT, debug=True)

