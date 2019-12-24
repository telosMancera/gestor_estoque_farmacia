# gestor\_estoque\_farmacia

O Gestor de estoque para farmácias consiste de uma aplicação para gerenciar medicamentos de uma farmácia, com controle de usuário, cadastro de medicamentos e cadastro de clientes.

## Organização do repositório

O repositório está organizado seguindo o modelo apresentado em <https://github.com/umermansoor/microservices>.

**database**

Diretório onde se econtram os arquivos do banco de dados da API.

**doc**

Documentação da API.

A documentação da API foi feita através da ferramenta **Postman**. Além dos PDFs neste diretório, é possivel ver a documentação nos *links* as seguir:

* Clientes: <https://documenter.getpostman.com/view/9886470/SWLYCWpp?version=latest>
* Remédios: <https://documenter.getpostman.com/view/9886470/SWLYCWpq?version=latest>
* Usuários: <https://documenter.getpostman.com/view/9886470/SWLYCWpr?version=latest>

**services**

Aqui se encontram os serviços da API em si.

**tests**

Diretório destinado a armazenar os *scripts* para testes da API.

## Ambiente de desenvolvimento

### Python

Toda a programação da aplicação foi feita na linguagem **Python**, mais especificamente na versão 3.8.0.

**Instalação**

Para instalar o **Python** no Windows, faça o *download* do instalador no *link* e execute-o.

<https://www.python.org/downloads/>

**Documentação**

<https://docs.python.org/3/>

### Git Bash for Windows

A aplicação foi desenvolvida em ambiente **Windows**, porém utilzando a ferramenta **Git Bash for Windows**. Tal ferramenta além de ser utilizada para versionamento através do **Git**, também proporciona a oportunidade de se utilizar comandos do **Bash**.

Todos os comandos mostrados neste **README** são baseados na utilização desta ferramenta.

**Instalação**

Para instalar o **Git Bash for Windows**, faça o *download* do instalador no *link* abaixo e execute o mesmo.

<https://gitforwindows.org/>

### Virtualenv

Para o desenvolvimento da aplicação, optou-se utlizar a ferramenta **virtualenv**, no intuito de se isolar o ambiente do *host* e ter maior controle sobre as bibliotecas utilzadas.

A seguir, serão mostradas algumas instruções para a utilização do **virutalenv**.

**Instalação**

Caso o **virutalenv** não esteja instalado, execute o comando abaixo.

**Documentação**

<https://virtualenv.pypa.io/en/latest/>

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

### Postman

Ferramenta utilizada para desenvolvimento de APIs. Possui vários recursos de teste, documentação e outras funcionalidades. Foi utilizada para os testes da API e sua documentação.

Uma vez no ambiente, toda biblioteca será instalada neste ambiente, e o ambiente *host* não será modificado.

**Instalação**

O instalador do **Postman** encontra-se no link abaixo.

<https://www.getpostman.com/downloads/>

**Documentação**

<https://learning.getpostman.com/docs/postman/launching-postman/introduction/>

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

## Execução

Para executar a API é necessária a execução dos três módulos principais da mesma, presentes no diretório **services**: **clients.py**, **medicines.py** e **users.py**.

Para isso, execute os comandos abaixo:

```bash
python clients.py &
python medicines.py &
python users.py &
```

Para cada comando executado, um identificador de processo é exibido logo em seguida. Com este número é possível matar o processo se necessário.

```bash
kill <PID>
```

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

## Melhorias

Esta seção destina-se a levantar pontos nos quais a aplicação pode ser melhorada.

* Encontrar uma forma de se utilizar apenas uma porta para o acesso à API. Como várias instâncias do **Flask** rodam concomitamente, portas diferentes foram utilizadas. Há alguns *links* onde se fala de utilizar servidores *web* ou programas parecidos que servem de "roteador" e que gerenciaria tal roteamento entre os módulos. Os arquivos dos cadastros estão sendo executados separadamente para se atender o requisito do projeto de ser em microserviços.
* Implementar os testes unitários.
* Utilizar um banco de dados mais "sofisticado". Mais precisamente utilizar um banco de dados que seja mais amplamente utilizado para estar mais de acordo com a tendência/demanda do mercado.
* Utilizar métodos de autenticação mais seguros ao invés do Basic Auth.
* Melhorar a forma de execução da API. Achar uma forma que automatize a execução de todos os módulos e que trate melhor a forma de se parar os processos.
* Melhorar os helpers/comentários dos métodos, utilizandos-se sintaxes similiares ao *docstring* e, assim, permitindo o uso de geradores automáticos de documentação.
* Adaptar o código para padrões do PEP 8. Pode se utilizar ferramentas como Pylint para facilitar a verificação da conformidade com o padrão.

