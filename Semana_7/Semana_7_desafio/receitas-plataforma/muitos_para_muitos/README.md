# README for Muitos para Muitos Recipe Platform

## Descrição do Projeto
Este projeto é uma plataforma de receitas culinárias desenvolvida em Python utilizando o framework Flask e o ORM SQLAlchemy. O objetivo é permitir que chefs registrem suas receitas, incluindo ingredientes e instruções, e que os usuários possam visualizar essas receitas.

## Estrutura do Projeto
A estrutura do projeto é a seguinte:

```
muitos_para_muitos/
├── app.py                # Ponto de entrada da aplicação Flask
├── models.py             # Modelos SQLAlchemy para as entidades
├── config.py             # Configurações da aplicação
├── requirements.txt      # Dependências do projeto
├── database.db           # Banco de dados SQLite
├── templates/            # Templates HTML
│   ├── base.html         # Estrutura HTML base
│   ├── index.html        # Lista de receitas
│   ├── criar_receita.html # Formulário para criar nova receita
│   └── detalhes_chef.html # Detalhes do chef
└── README.md             # Documentação do projeto
```

## Instalação
Para instalar as dependências do projeto, execute o seguinte comando:

```
pip install -r requirements.txt
```

## Uso
1. Execute a aplicação Flask:
   ```
   python app.py
   ```
2. Acesse a aplicação no seu navegador em `http://127.0.0.1:5000/`.

## Funcionalidades
- Listar todas as receitas com título, nome do chef e ingredientes.
- Criar novas receitas com título, instruções, seleção do chef e ingredientes.
- Visualizar detalhes de cada chef, incluindo suas especialidades e receitas.

## Contribuição
Sinta-se à vontade para contribuir com melhorias ou correções. Para isso, faça um fork do repositório e envie um pull request.

## Licença
Este projeto está licenciado sob a MIT License. Veja o arquivo LICENSE para mais detalhes.