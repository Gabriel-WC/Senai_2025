# -*- coding: utf-8 -*-

# Passo 1: Importações e Configuração
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, redirect, url_for

# Inicializa a aplicação Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'sua_segurança_mora_aqui'

# Configuração do banco de dados SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///meu_app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# --- Modelos ---
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return f'<Usuario: {self.nome}>'


class Tarefa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)

    usuario = db.relationship('Usuario', backref=db.backref('tarefas', lazy=True))

    def __repr__(self):
        return f'<Tarefa: {self.nome}>'


class Postagem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(120), nullable=False)
    conteudo = db.Column(db.Text, nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)

    usuario = db.relationship('Usuario', backref=db.backref('postagens', lazy=True))

    def __repr__(self):
        return f'<Postagem: {self.titulo}>'


# --- Rotas da Aplicação ---
@app.route('/')
def index():
    """Página inicial que exibe os usuários cadastrados"""
    usuarios = Usuario.query.all()
    postagens = Postagem.query.all()  # Para exibir postagens na página inicial
    return render_template('index.html', usuarios=usuarios, postagens=postagens)


# ...existing code...
@app.route('/adicionar', methods=['GET', 'POST'])
def adicionar():
    """Adiciona um novo usuário"""
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')

        if nome and email:
            novo_usuario = Usuario(nome=nome, email=email)
            db.session.add(novo_usuario)
            db.session.commit()

        return redirect(url_for('index'))

    return render_template('adicionar.html')


@app.route('/cadastrar-tarefa', methods=['GET', 'POST'])
def cadastrar_tarefa():
    """Cadastro de tarefas vinculadas a um usuário"""
    if request.method == 'POST':
        nome_tarefa = request.form.get('nome_tarefa')
        usuario_id = request.form.get('usuario_id')

        if nome_tarefa and usuario_id:
            nova_tarefa = Tarefa(nome=nome_tarefa, usuario_id=int(usuario_id))
            db.session.add(nova_tarefa)
            db.session.commit()

        return redirect(url_for('index'))

    usuarios = Usuario.query.all()  # Para selecionar o usuário dono da tarefa
    return render_template('cadastrar_tarefa.html', usuarios=usuarios)


@app.route('/deletar/<int:id>')
def deletar_usuario(id):
    """Remove um usuário"""
    usuario = Usuario.query.get(id)
    if usuario:
        db.session.delete(usuario)
        db.session.commit()
    return redirect(url_for('index'))


@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_usuario(id):
    """Edita informações de um usuário"""
    usuario = Usuario.query.get_or_404(id)
    if request.method == 'POST':
        usuario.nome = request.form.get('nome')
        usuario.email = request.form.get('email')
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('editar.html', usuario=usuario)


@app.route('/sobre')
def sobre():
    """Página Sobre"""
    return render_template('sobre.html')


@app.route('/adicionar-postagem', methods=['GET', 'POST'])
def adicionar_postagem():
    """Adiciona uma nova postagem"""
    if request.method == 'POST':
        titulo = request.form.get('titulo')
        conteudo = request.form.get('conteudo')
        usuario_id = request.form.get('usuario_id')

        if titulo and conteudo and usuario_id:
            nova_postagem = Postagem(titulo=titulo, conteudo=conteudo, usuario_id=int(usuario_id))
            db.session.add(nova_postagem)
            db.session.commit()

        return redirect(url_for('index'))

    usuarios = Usuario.query.all()  # Para selecionar o usuário dono da postagem
    return render_template('adicionar_postagem.html', usuarios=usuarios)


# Passo 3: Criando o Banco de Dados Físico e rodando o servidor
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)