# CryptoTrendAnalyzer

Este projeto tem como objetivo fornecer uma análise de tendências de criptomoedas, utilizando uma API desenvolvida com Django Rest Framework (DRF) e Postgres para o gerenciamento de dados.
A aplicação oferece endpoints RESTful para interação com dados de criptomoedas, incluindo visualizações de tendências, preços atuais e históricos.

## Requisitos Técnicos

Para obter uma compreensão detalhada dos requisitos técnicos deste projeto, consulte o documento "Quero Ser MB - Teste Backend 2.pdf" disponível na pasta `requisitos`. Este documento contém todas as especificações e critérios necessários para o desenvolvimento e avaliação do projeto.

[Visualizar Requisitos Técnicos](requisitos/Quero%20Ser%20MB%20-%20Teste%20Backend%202.pdf)


## Versões e Dependências

Este projeto foi desenvolvido com Python 3.10 e faz uso do Pipenv para gerenciamento de dependências. As principais tecnologias incluem Django Rest Framework para a criação de APIs RESTful, Postgres como banco de dados, Pytest e Pytest-coverage para testes e relatórios de cobertura de testes, respectivamente.

Dependências principais:
- Django 5.0.3
- Django Rest Framework 3.15.1
- Psycopg2-binary 2.9.9 (adaptador Postgres para Python)
- Drf-yasg 1.21.7 (geração de documentação Swagger)
- Pytest 8.1.1
- Pytest-cov 5.0.0
- Make

### Docker e Docker Compose

Este projeto é orquestrado com Docker, simplificando tanto o desenvolvimento quanto a implantação. Para utilizar o Docker, é necessário instalá-lo junto ao Docker Compose. Aqui estão os links para as documentações oficiais que contêm instruções detalhadas de instalação:

- Docker: [Instalação do Docker](https://docs.docker.com/engine/install/)
- Docker Compose: [Instalação do Docker Compose](https://docs.docker.com/compose/install/)

### Configuração Inicial para Linux

Para usuários Linux, é altamente recomendável utilizar o `make` para simplificar a execução de tarefas comuns através de aliases definidos no `Makefile`. Se o `make` não estiver instalado no seu sistema, você pode instalá-lo usando o seguinte comando:

```bash
sudo apt update
sudo apt install make
```
## Usando comandos do Makefile

Os comandos do `Makefile` facilitam a execução de tarefas comuns durante o desenvolvimento e a manutenção do projeto. Para utilizá-los, certifique-se de que você tem o `make` instalado em seu sistema e execute os comandos no terminal a partir da raiz do projeto.

Para facilitar o desenvolvimento e a implantação, este projeto foi dockerizado. Abaixo estão os comandos principais do `Makefile` para interagir com a aplicação via Docker:

- `make setup`: Cria o arquivo `.env` a partir do `.env-exemplo` na pasta `contrib`.
- `make build`: Constrói as imagens Docker do projeto.
- `make up`: inicia os contêineres Docker do projeto
- `make up-log`: Similar ao `make up`, mas mantém os logs da aplicação visíveis no terminal.
- `make down`: Para e remove os contêineres Docker.
- `make test`: Executa os testes do projeto utilizando Pytest.
- `make test-coverage`: Executa os testes e gera um relatório de cobertura de código.
- `make test-cov-report`: Gera um relatório detalhado da cobertura de testes em formato HTML.


## Iniciando a aplicação com Docker
- rode o comando `make setup` para criação do .env na pasta app
- rode o comando `make up-log` e aguarde o terminal mostrar que o serviço já está rodando na porta 8000


## Acessando o API via Swagger

Uma vez que a aplicação esteja rodando (via `make up` ou `make up-log`), você pode acessar a documentação interativa da API Swagger pelo seguinte URL: `http://localhost:8000/`.
Isso permite que você visualize e interaja com os endpoints da API de forma fácil e intuitiva.


## Rotinas de Monitoramento
- Rode o comando: `make crontab-add` para adicionar as rotinas configuradas a serem executadas de hora em hora
- Rode o comando: `make crontab-show` para vizualizar as rotinas no cron
- Rode o comando: `make check-missing-days` para rodar a rotina e fazer a verificação se há algum dia ausente no intervalo de 365 dias.
- Rode o comando: `make verify-makrket-data` para rodar a rotina e verificar se houve algum erro na carga dos dados da api do MB no dia.

- A rotina está configurada para rodar de hora em hora, caso encontre algum erro de carga, será efetuado uma nova tentativa a cada hora.
- A Rotina de verificação de dados ausentes no range de 365 dias, vai mostrar no log do terminal e salvar na tabela no banco os dias faltantes.
