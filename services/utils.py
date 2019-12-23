# -*- coding:utf-8 -*-

import os
import jwt
from functools import wraps
from flask import request, jsonify


API_ROUTE = '/gestor'
API_USERS_ROUTE = API_ROUTE + '/users'
API_MEDICINES_ROUTE = API_ROUTE + '/medicines'
API_CLIENTS_ROUTE = API_ROUTE + '/clients'

API_USERS_PORT = 5000
API_MEDICINES_PORT = 5001
API_CLIENTS_PORT = 5002

SECRET_KEY = 'secretkey'


def root_dir():
	'''
	Retorna o diretório raiz para este projeto.
	'''
	return os.path.dirname(os.path.realpath(__file__ + '/..'))


def token_required(func):
	'''
	Força a validação via token JWT no método passado.

	* func : método a receber a validação via token.

	O método deve possuir como primeiro argumento, o usuário corrente (current_user).

	O token deve ser passado para a URI através da chave 'x-access-token' no cabeçalho da requisição.
	'''
	@wraps(func)
	def decorated(*args, **kwargs):
		token = None

		if 'x-access-token' in request.headers:
			token = request.headers.get('x-access-token', None)

		if not token:
			return jsonify({'message': 'Token is missing!'}), 403

		try:
			data = jwt.decode(token, SECRET_KEY)

		except Exception:
			return jsonify({'message': 'Token is invalid!'}), 403

		current_user = {
				'id'		: data['id'],
				'status'	: data['status'],
				'admin'		: data['admin']
		}

		if not current_user['admin'] and current_user['status'] == 'inactive':
			return jsonify({'message': 'You are inactive!'}), 403

		return func(current_user, *args, **kwargs)

	return decorated

