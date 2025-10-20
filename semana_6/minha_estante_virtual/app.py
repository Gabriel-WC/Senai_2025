from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from forms import AutorForm, LivroForm
from models import db, Autor, Livro

app = Flask(__name__)
app.config['SECRET_KEY'] = 'minha-chave-secreta'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///minha_estante.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Configura o QuerySelectField do LivroForm
def get_autores():
    return Autor.query

@app.route('/autores', methods=['GET', 'POST'])
def autores():
    form = AutorForm()
    if form.validate_on_submit():
        novo_autor = Autor(nome=form.nome.data)
        db.session.add(novo_autor)
        db.session.commit()
        return redirect(url_for('autores'))
    lista_autores = Autor.query.all()
    return render_template('autores.html', form=form, autores=lista_autores)

@app.route('/', methods=['GET', 'POST'])
@app.route('/livros', methods=['GET', 'POST'])
def livros():
    form = LivroForm()
    form.autor.query = get_autores()
    if form.validate_on_submit():
        novo_livro = Livro(
            titulo=form.titulo.data,
            ano_publicacao=form.ano_publicacao.data,
            autor=form.autor.data
        )
        db.session.add(novo_livro)
        db.session.commit()
        return redirect(url_for('livros'))
    lista_livros = Livro.query.all()
    return render_template('livros.html', form=form, livros=lista_livros)

# Cria o banco de dados na primeira execução
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)