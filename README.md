<h1>DEV BACK-END</h1>

API desenvolvida para gerenciamento de receitas de cozinha.

## FEATURES 

- [x] Cadastrar um Chef
- [x] Pegar o token 
- [x] Retornar um Chef
- [x] Atualizar dados de um Chef  
- [x] Remover um Chef
- [x] Cadastrar uma Receita 
- [x] Atualizar uma Receita
- [x] Retornar uma Receita pelo ID
- [x] Retornar todas as Receitas
- [x] Remover uma Receita
- [x] Retornar receitas por conter nome no título ou ingredientes
- [x] Retornar receitas de um Chef específico   

## 🛠 TECNOLOGIAS

- [Django](https://www.djangoproject.com/)

## COMO RODAR A APLICAÇÃO

> OBSERVAÇÃO: PRECISA TER O PIPENV INSTALDO NA MÁQUINA

- Fazer o clone do projeto
    - git clone https://github.com/loressl/recipe_backend.git
- Abrir a pasta do projeto
- Abrir o terminal e digitar os seguintes comandos:
    - pipenv shell : criar ou activar o ambiente virtual
    - pipenv install : instalar os packages
    - python manage.py migrate : criar as tabelas no banco de dados (dentro da outra pasta recipe_backend, pois é onde está o manage.py)
    - python manage.py runserver : subir o servidor
    - exit : sair do ambiente virtual

## COMO RODAR OS TESTES

> OBSERVAÇÃO: PRECISA ESTÁ DENTRO DO AMBIENTE VIRTUAL

- Criar um arquivo .env e inserir:
    - API_BASE: seu localhost que aparece no momento que sobe o servidor
- Digitar: python manage.py test

## DOCUMENTAÇÃO

Todas as informações das rotas, como o que deve passar e o que irá retornar, estão [aqui](https://documenter.getpostman.com/view/5841921/TzCL7ntK#f477be36-d530-457f-9ad9-73a4a89992e8).

No repositório, há um arquivo json chamado [recipe_backend.postman_collection](https://github.com/loressl/recipe_backend/blob/master/recipe_backend.postman_collection.json), que pode ser importado para o Postman ou outra plataforma de desenvolvimento de API, e mostra todas as rotas prontas. 
