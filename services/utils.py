# -*- coding:utf-8 -*-

import os


API_ROUTE = '/gestor'
API_USERS_ROUTE = API_ROUTE + '/users'
API_MEDICINES_ROUTE = API_ROUTE + '/medicines'
API_CLIENTS_ROUTE = API_ROUTE + '/clients'

API_USERS_PORT = 5000
API_MEDICINES_PORT = 5001
API_CLIENTS_PORT = 5002


def root_dir():
	'''
	Retorna o diretório raiz para este projeto.
	'''
	return os.path.dirname(os.path.realpath(__file__ + '/..'))

