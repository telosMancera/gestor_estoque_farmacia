import os
import json
from flask import make_response


def root_dir():
	'''
	Retorna o diretório raiz para este projeto
	'''
	return os.path.dirname(os.path.realpath(__file__ + '/..'))

