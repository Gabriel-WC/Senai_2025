import os
from flask import Flask, request, redirect, url_for, render_template, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'uma-chave-secreta'
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'database.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# -------------------- MODELS --------------------
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), unique=True, nullable=False)
    perfil = db.relationship('Perfil', uselist=False, back_populates='usuario', cascade='all, delete-orphan')

class Perfil(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome_completo = db.Column(db.String(120), nullable=False)
    bio = db.Column(db.Text)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), unique=True, nullable=False)
    usuario = db.relationship('Usuario', back_populates='perfil')

# -------------------- ROTAS --------------------
@app.route('/')
def index():
    usuarios = Usuario.query.all()
    return render_template('index.html', usuarios=usuarios)

@app.route('/adicionar_usuario', methods=['POST'])
def adicionar_usuario():
    nome = request.form.get('nome')
    if nome and not Usuario.query.filter_by(nome=nome).first():
        db.session.add(Usuario(nome=nome))
        db.session.commit()
        flash(f'Usuário "{nome}" adicionado!', 'success')
    else:
        flash('Nome inválido ou já existe.', 'danger')
    return redirect(url_for('index'))

@app.route('/adicionar_perfil', methods=['POST'])
def adicionar_perfil():
    usuario_id = int(request.form.get('usuario_id'))
    nome_completo = request.form.get('nome_completo')
    bio = request.form.get('bio')
    usuario = Usuario.query.get(usuario_id)
    if usuario and not usuario.perfil:
        db.session.add(Perfil(nome_completo=nome_completo, bio=bio, usuario_id=usuario.id))
        db.session.commit()
        flash(f'Perfil adicionado para {usuario.nome}!', 'success')
    else:
        flash('Usuário não existe ou já tem perfil.', 'danger')
    return redirect(url_for('index'))

@app.route('/excluir_usuario/<int:usuario_id>', methods=['POST'])
def excluir_usuario(usuario_id):
    usuario = Usuario.query.get_or_404(usuario_id)
    db.session.delete(usuario)
    db.session.commit()
    flash(f'Usuário "{usuario.nome}" excluído.', 'info')
    return redirect(url_for('index'))

# -------------------- INICIALIZAÇÃO --------------------
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=500)
