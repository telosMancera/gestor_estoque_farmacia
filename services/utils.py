import os
from flask import url_for


def root_dir():
	'''
	Retorna o diretório raiz para este projeto.
	'''
	return os.path.dirname(os.path.realpath(__file__ + '/..'))

