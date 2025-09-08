# README for Um Para Muitos Recipe Platform

Este projeto é uma plataforma de receitas culinárias que utiliza o framework Flask e SQLAlchemy para gerenciar dados de chefs, receitas e ingredientes. O projeto é estruturado para demonstrar um relacionamento um-para-muitos entre chefs e receitas.

## Estrutura do Projeto

- **app.py**: Ponto de entrada da aplicação Flask. Configura a aplicação, define as rotas e inicializa o banco de dados.
- **models.py**: Contém os modelos SQLAlchemy para as entidades Chef, PerfilChef, Receita e Ingrediente, incluindo suas relações.
- **config.py**: Configurações da aplicação, como a URI do banco de dados e as configurações do SQLAlchemy.
- **requirements.txt**: Lista as dependências do projeto, como Flask e SQLAlchemy.
- **database.db**: Arquivo do banco de dados SQLite onde os dados da aplicação são armazenados.
- **templates/**: Contém os arquivos HTML utilizados pela aplicação:
  - **base.html**: Estrutura HTML base utilizada por todas as páginas.
  - **index.html**: Exibe a lista de todas as receitas, mostrando o título, o nome do chef e os ingredientes.
  - **criar_receita.html**: Formulário para a criação de uma nova receita.
  - **detalhes_chef.html**: Exibe os detalhes de um chef, incluindo seu nome, especialidade, anos de experiência e uma lista de suas receitas.

## Instalação

1. Clone o repositório:
   ```
   git clone <URL_DO_REPOSITORIO>
   cd receitas-plataforma/um_para_muitos
   ```

2. Instale as dependências:
   ```
   pip install -r requirements.txt
   ```

3. Execute a aplicação:
   ```
   python app.py
   ```

4. Acesse a aplicação em seu navegador em `http://127.0.0.1:5000`.

## Uso

- Na página inicial, você pode ver todas as receitas cadastradas.
- Você pode criar uma nova receita acessando a página de criação.
- Clique no nome de um chef para ver suas informações e receitas associadas.

## Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou pull requests.