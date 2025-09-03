# Meu App - Documentação do Projeto

Este projeto é uma aplicação web desenvolvida com Flask, que permite o gerenciamento de usuários e tarefas. A aplicação utiliza um banco de dados SQLite para armazenar as informações.

## Estrutura do Projeto

O projeto possui a seguinte estrutura de arquivos:

```
meu_app/
├── app.py                  # Ponto de entrada da aplicação Flask
├── templates/              # Diretório contendo os templates HTML
│   ├── index.html          # Página inicial que exibe os usuários cadastrados
│   ├── adicionar.html      # Template para adicionar um novo usuário
│   ├── cadastrar_tarefa.html # Template para cadastrar tarefas vinculadas a um usuário
│   ├── editar.html         # Template para editar informações de um usuário
│   └── sobre.html          # Template para a página "Sobre"
└── README.md               # Documentação do projeto
```

## Funcionalidades

- **Gerenciamento de Usuários**: Permite adicionar, editar e deletar usuários.
- **Cadastro de Tarefas**: Usuários podem cadastrar tarefas vinculadas a eles.
- **Visualização**: Exibe uma lista de usuários e suas respectivas tarefas.

## Como Executar

1. Clone o repositório:
   ```
   git clone <URL_DO_REPOSITORIO>
   ```

2. Navegue até o diretório do projeto:
   ```
   cd meu_app
   ```

3. Instale as dependências necessárias:
   ```
   pip install -r requirements.txt
   ```

4. Execute a aplicação:
   ```
   python app.py
   ```

5. Acesse a aplicação no navegador em `http://localhost:5000`.

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou pull requests.

## Licença

Este projeto está licenciado sob a MIT License. Veja o arquivo LICENSE para mais detalhes.