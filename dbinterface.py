from tinydb import TinyDB, Query


class DBInterface():
	'''
	Classe interface com o banco de dados
	Utilzada para abstrair o banco utilizado e armazenar os cadastros da forma desejada
	'''

	def __init__(self, dbname, fields):
		'''
		Construtor da classe

		* dbname : nome do banco a ser criado/carregado
		* fields : campos do cadastro inseridos em forma de lista
		'''
		self.__dbname = dbname
		self.__fields = fields

		# A classe DBInterface já se encarrega de atribuir IDs ao elementos do cadastro
		# Caso um campo ID seja adicionado em fields, a classe insere um campo de ID
		#   adicional com um "nome" diferente para diferenciação
		self.__idfield = 'id' if 'id' not in fields else '_id'

		self.__db = TinyDB(f'./tinydb_{dbname}.json')


	def create_element(self, element):
		'''
		Adiciona um novo elemento no banco

		* element : elemento a ser inserido. Deve ser um dicionário
		'''
		try:
			new_element = {}
			new_element[self.__idfield] = ''
			for field in self.__fields:
				new_element[field] = element.get(field, '')

			tinydb_id = self.__db.insert(new_element)
			self.__db.update({self.__idfield: tinydb_id}, doc_ids=[tinydb_id])

			return self.__db.get(doc_id=tinydb_id)

		except Exception:
			return -1


	def delete_element(self, field_name, field_value):
		'''
		Remove o selementos que correspondam à consulta passada

		* field_name  : campo a ser utilizado na consulta
		* field_value : valor desejado para o campo da consulta
		'''
		try:
			self.__db.remove(Query()[field_name] == field_value)

			return 0 

		except Exception:
			return -1


	def get_all_elements(self):
		'''
		Retorna todos elementos do banco
		'''
		return self.__db.all()


	def get_element(self, field_name, field_value):
		'''
		Retorna os elementos que correspondam à consulta

		* field_name  : campo a ser utilizado na consulta
		* field_value : valor desejado para o campo da consulta
		'''
		try:
			return self.__db.search(Query()[field_name] == field_value)

		except Exception:
			return -1


	def update_element(self, fields, field_name, field_value):
		'''
		Atualiza todos os elementos que correspondam à consulta passada

		* fields      : dicionário contendo os campos a serem atualizados e seus respectivos novos valores
		* field_name  : campo a ser utilizado na consulta
		* filed_value : valor desejado para o campo da consulta
		'''
		try:
			# O campoo ID do cadastro não pode ser alterado
			if self.__idfield in fields:
				return -1

			self.__db.update(fields, Query()[field_name] == field_value)

			return self.__db.search(Query()[field_name] == field_value)

		except Exception:
			return -1


if __name__ == '__main__':
	with open('tinydb_dbtest.json', 'wb') as f:
		f.seek(0)
		f.write(b'')

	db = DBInterface('dbtest', ['a', 'b'])

	print('create element')
	print(db.create_element({
		'a': 1,
		'b': 2
	}))
	print(db.create_element({
		'a': 10,
		'b': 20
	}))

	print('\nget all elements')
	print(db.get_all_elements())

	print('\nget element')
	print(db.get_element('a', 1))
	print(db.get_element('a', 5))

	print('\nupdate element')
	print(db.update_element({'b': 15}, 'a', 10))
	print(db.get_all_elements())

	print('\ndelete element')
	print(db.delete_element('id', 2))
	print(db.get_all_elements())

	print('\ncreate element')
	print(db.create_element({
		'a': 100,
		'b': 200
	}))
	print(db.get_all_elements())

	print('\ncreate element')
	print(db.create_element({
		'a': 1000,
		'b': 2000
	}))
	print(db.get_all_elements())
