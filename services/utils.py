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
	@wraps(func)
	def decorated(*args, **kwargs):
		request_json = request.json
		if not request_json or 'token' not in request_json or request_json['token'] == '':
			return jsonify({'message': 'Token is missing!'}), 403

		token = request_json['token']
		try:
			data = jwt.decode(token, SECRET_KEY)

		except Exception:
			return jsonify({'message': 'Token is invalid!'}), 403

		return func(*args, **kwargs)

	return decorated

