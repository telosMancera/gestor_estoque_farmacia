# gestor_estoque_farmacia

O Gestor de estoque para farmácias consiste de uma aplicação para gerenciar medicamentos de uma farmácia, com controle de usuário, cadastro de medicamentos e cadastro de clientes.

## Organização do repositório

O repositório está organizado seguindo o modelo apresentado em <https://github.com/umermansoor/microservices>.

**database**

Diretório onde se econtram os arquivos do banco de dados da api.

**services**

Aqui se encontram os serviços da API em si.

**tests**

Diretório destinado a armazenar os *scripts* para testes da API.

## Ambiente de desenvolvimento

### Git Bash for Windows

A aplicação foi desenvolvida em ambiente **Windows**, porém utilzando a ferramenta **Git Bash for Windows**. Tal ferramenta além de ser utilizada para versionamento através do **Git**, também proporciona a oportunidade de se utilizar comandos do **Bash**.

Todos os comandos mostrados neste **README** são baseados na utilização desta ferramenta.

### Virtualenv

Para o desenvolvimento da aplicação, optou-se utlizar a ferramenta **virtualenv**, no intuito de se isolar o ambiente do *host* e ter maior controle sobre as bibliotecas utilzadas.

A seguir, serão mostradas algumas instruções para a utilização do **virutalenv**. Para maiores informações, leia a documentação completa em <https://virtualenv.pypa.io/en/latest/>.

**Instalação**

Caso o **virutalenv** não esteja instalado, execute o comando abaixo.

```bash
pip install virtualenv
```

**Utilização**

Para utilizar o **virtualenv**, execute o comando a seguir. Sendo que **ENV** é o diretório serão armazenados os arquivos para a virutalização. Pode se utilizar qualquer outro nome

```bash
python -m virtualenv ENV
```

Uma vez criado o diretório, ativa-se a virtualização através do comando:

```bash
source ENV/Scripts/activate
```

O caminho para o *script* de ativação pode variar de ambiente para ambiente. Uma vez ativado, observa-se que no *prompt* aparecerá o texto **(ENV)**, indicando que se está no ambiente virtualizado

Para sair deste ambiente, basta rodar o comando:

```bash
deactivate
```

Uma vez no ambiente, toda biblioteca será instalada neste ambiente, e o ambiente *host* não será modificado.

## Dependências

**OBS:** Lembre-se de estar no ambiente virtualizado para se evitar problemas com o ambiente *host*.

Para o desenvolvimento e execução da aplicação, algumas bibliotecas são utilizadas. A seguir é mostrado como se instalar cada biblioteca.

Se preferir, é possível utilizar o comando abaixo para se intalar todas as bibliotecas em suas respectivas versões automaticamente. 

```bash
pip install -r requirements.txt
```

O arquivo **requirements.txt** armazena todas as bibliotecas instaladas através da ferramenta **pip** do **Python**. Sempre que houver uma alteração nas bibliotecas utilizadas, execute o comando a seguir para atualizar este arquivo.

```bash
pip freeze > requirements.txt
```

### Flask

*Framework* utilzado para desenvolvimento *web*. Utilizado para a construção das APIs

**Instalação**

```bash
pip install flask
```

**Documentação**

<http://flask.palletsprojects.com/en/1.1.x/>

### TinyDB

Banco de dados baseado em documentos utilizado para armazenamento dos cadastros.

**Instalação**

```bash
pip install tinydb
```

**Documentação**

<https://tinydb.readthedocs.io/en/latest/intro.html>

## PyJWT

Biblioteca utilizada para geração de tokens JWT.

```bash
pip install pwjwt
```

**Documentação**

<https://pyjwt.readthedocs.io/en/latest/>

## Links

Abaixo estão alguns links utilizados como referência no desenvolvimento desta aplicação

* <https://github.com/umermansoor/microservices>
* <https://virtualenv.pypa.io/en/latest/>
* <http://flask.palletsprojects.com/en/1.1.x/>
* <https://tinydb.readthedocs.io/en/latest/intro.html>
* <https://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask>
* <https://stackoverflow.com/questions/26997679/writing-a-csv-from-flask-framework>
* <http://blog.appliedinformaticsinc.com/how-to-parse-and-convert-json-to-csv-using-python/>
* <https://medium.com/@petehouston/upload-files-with-curl-93064dcccc76>
* <https://curl.haxx.se/docs/httpscripting.html>
* <https://www.youtube.com/watch?v=tfKatqbZicA>

