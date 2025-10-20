from flask import Flask, request, redirect, url_for, render_template, flash
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'uma-chave-secreta-bem-segura'

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# MODELS
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario_nome = db.Column(db.String(80), unique=True, nullable=False)
    publicacoes = db.relationship('Publicacao', back_populates='autor', cascade='all, delete-orphan')

class Publicacao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(120), nullable=False)
    conteudo = db.Column(db.Text)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    autor = db.relationship('Usuario', back_populates='publicacoes')

# ROTAS
@app.route('/')
def index():
    usuarios = Usuario.query.all()
    return render_template('index.html', usuarios=usuarios)

@app.route('/adicionar_usuario', methods=['POST'])
def adicionar_usuario():
    nome = request.form.get('usuario_nome')
    if nome and not Usuario.query.filter_by(usuario_nome=nome).first():
        db.session.add(Usuario(usuario_nome=nome))
        db.session.commit()
        flash(f'Usuário "{nome}" adicionado com sucesso!', 'success')
    else:
        flash(f'Usuário "{nome}" já existe ou é inválido.', 'danger')
    return redirect(url_for('index'))

@app.route('/adicionar_perfil', methods=['POST'])
def adicionar_perfil():
    usuario_id = request.form.get('usuario_id')
    titulo = request.form.get('titulo')
    conteudo = request.form.get('conteudo')
    if usuario_id and titulo:
        usuario = Usuario.query.get(usuario_id)
        if usuario:
            db.session.add(Publicacao(titulo=titulo, conteudo=conteudo, autor=usuario))
            db.session.commit()
            flash(f'Publicação "{titulo}" adicionada para {usuario.usuario_nome}!', 'success')
    return redirect(url_for('index'))

@app.route('/excluir_usuario/<int:usuario_id>', methods=['POST'])
def excluir_usuario(usuario_id):
    usuario = Usuario.query.get_or_404(usuario_id)
    db.session.delete(usuario)
    db.session.commit()
    flash(f'Usuário "{usuario.usuario_nome}" e suas publicações foram deletados.', 'info')
    return redirect(url_for('index'))

# MAIN
if __name__ == "__main__":
    with app.app_context():  # garante que o contexto do Flask está ativo
        db.create_all()      # cria todas as tabelas do banco
    app.run(debug=True, host='0.0.0.0', port=5001)

