# Deloitte
Para instalar somente é necessário ter o Python instalado na máquina e executar o script [deploy.py](https://raw.githubusercontent.com/mmanfro/deloitte/main/deploy.py)<br />
> <sup>O script foi testado no Windows 11 e Debian WSL com Python 3.10</sup>

- Esse script irá baixar o projeto, criar um ambiente virtual, baixar as dependências neste ambiente virtual, e executar os comandos para o deploy
- Caso o navegador não seja aberto automaticamento, você pode acessar a aplicação manualmente no endereço [127.0.0.1:8000](http://127.0.0.1:8000/)
- Existem algumas centenas de dados em arquivos JSON que podem ser carregados para a API via REST, apenas clicando num botão na página inicial
- Um super-usuário já é criado automaticamente:
  > **Usuário**: admin<br />
  > **Senha**: admin
- Para obter o token é só enviar uma requisição para http://127.0.0.1:8000/api-token-auth/ com o corpo:
  ```
  {
    "username": "admin",
    "password": "admin"
  }
  ```
- O token é utilizado com o **HEADER** ` Authorization: Token <token> ` Exemplo:
  ```
  curl --header "Authorization: Token b17eeb47a0e5d68ad5aba5e2952e4969a615bef1" http://127.0.0.1:8000/api/v1/aluno/
  ```

# Caso queira fazer o deploy manualmente:
<ol>
  <li>Baixar o projeto para sua máquina</li>
  <li>Caso não queria instalar as dependências no Python global,
  <a href="https://docs.python.org/pt-br/3/library/venv.html">criar um ambiente virtual e ativá-lo</a></li>
  <li>Instalar as dependências que constam no arquivo requirements.txt <code>pip install -r requirements.txt</code></li>
  <li>Criar o banco de dados via Django <code>python manage.py migrate</code></li>
  <li>Coletar os arquivos estáticos <code>python manage.py collectstatic</code></li>  
  <li>Criar um super-usuário <code>python manage.py createsuperuser</code></li>
  <li>Rodar a aplicação via servidor do Django <code>python manage.py runserver</code></li>
  <li>Acessar a aplicação no endereço http://127.0.0.1:8000/</li>
</ol>

# Observações
- Foi utilizado o ORM do Django para a criação das tabelas, porém tem também um script SQL de como eu as criaria manualmente no SQLite
- Foram feitos alguns testes, que podem ser executados com `python manage.py test `
- Foi feito um versionamento básico via `namespace `
- Foi feita internacionalização
- Os objetos também podem ser acessados pelo painel admin do Django: [127.0.0.1:8000/admin](http://127.0.0.1:8000/admin/)
