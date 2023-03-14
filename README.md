# Gerenciador de cpfs
Esta é uma aplicação em python que oferece uma api de gerenciador de cpfs. Ela permite que você insira, delete e busque o cpf.

**Obs: A aplicação só aceita cpfs válidos.**
___
## Tecnologias ultilizadas
* FastAPi
* SQLAlchemy
* Sqlite3
* Pytest
* Uvicorn
* Docker

O FastAPi é um framework python focado no desenvolvimento de api, moderno e simples de usar que permite a utilização de bibliotecas como o SQLAlchemy que facilita a conexão e manipulação de registros nos bancos de dados. Para fazer testes é possível usar a biblioteca pytest diretamente com FastApi.

O Sqlite3 foi escolhido por ser um banco de dados leve, podendo ser substituído facilmente, devido ao SQLAlchemy, caso a aplicação precise de um banco mais robusto.

## Rodando a aplicação

No diretório da aplicação execute os comandos abaixo:

``` $ docker-compose build``` 

``` $ docker-compose up``` 

## Rodando os testes

Com a aplicação rodando execute o comando:

``` $ docker-compose exec api pytest . ```



