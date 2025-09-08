# README for the Um Para Um Recipe Platform

Este projeto é uma plataforma de receitas culinárias que utiliza um relacionamento um para um entre Chef e PerfilChef. Abaixo estão as instruções para instalação e uso.

## Estrutura do Projeto

```
um_para_um/
├── app.py
├── models.py
├── config.py
├── requirements.txt
├── database.db
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── criar_receita.html
│   └── detalhes_chef.html
└── README.md
```

## Instalação

1. Clone o repositório:
   ```
   git clone <URL_DO_REPOSITORIO>
   cd um_para_um
   ```

2. Crie um ambiente virtual:
   ```
   python -m venv venv
   source venv/bin/activate  # No Windows use `venv\Scripts\activate`
   ```

3. Instale as dependências:
   ```
   pip install -r requirements.txt
   ```

## Uso

1. Execute a aplicação:
   ```
   python app.py
   ```

2. Acesse a aplicação no seu navegador em `http://127.0.0.1:5000`.

## Funcionalidades

- Listagem de receitas com detalhes do chef e ingredientes.
- Formulário para criação de novas receitas.
- Detalhes do chef, incluindo especialidade e anos de experiência.

## Contribuição

Sinta-se à vontade para contribuir com melhorias ou correções. Crie um fork do repositório e envie um pull request.

## Licença

Este projeto está licenciado sob a MIT License. Veja o arquivo LICENSE para mais detalhes.