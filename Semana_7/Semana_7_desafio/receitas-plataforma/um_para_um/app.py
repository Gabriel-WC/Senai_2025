from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Chef(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    perfil = db.relationship('PerfilChef', backref='chef', uselist=False)
    receitas = db.relationship('Receita', backref='chef')

class PerfilChef(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    especialidade = db.Column(db.String(100), nullable=False)
    anos_experiencia = db.Column(db.Integer, nullable=False)
    chef_id = db.Column(db.Integer, db.ForeignKey('chef.id'))

class Receita(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    instrucoes = db.Column(db.Text, nullable=False)
    chef_id = db.Column(db.Integer, db.ForeignKey('chef.id'))
    ingredientes = db.relationship('ReceitaIngrediente', backref='receita')

class Ingrediente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), unique=True, nullable=False)
    receitas = db.relationship('ReceitaIngrediente', backref='ingrediente')

class ReceitaIngrediente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    receita_id = db.Column(db.Integer, db.ForeignKey('receita.id'))
    ingrediente_id = db.Column(db.Integer, db.ForeignKey('ingrediente.id'))
    quantidade = db.Column(db.String(100))

@app.route('/')
def index():
    receitas = Receita.query.all()
    return render_template('index.html', receitas=receitas)

@app.route('/receita/nova', methods=['GET', 'POST'])
def criar_receita():
    if request.method == 'POST':
        titulo = request.form['titulo']
        instrucoes = request.form['instrucoes']
        chef_id = request.form['chef_id']
        ingredientes_nomes = request.form['ingredientes'].split(',')

        nova_receita = Receita(titulo=titulo, instrucoes=instrucoes, chef_id=chef_id)
        db.session.add(nova_receita)
        db.session.commit()

        for nome in ingredientes_nomes:
            ingrediente = Ingrediente.query.filter_by(nome=nome.strip()).first()
            if not ingrediente:
                ingrediente = Ingrediente(nome=nome.strip())
                db.session.add(ingrediente)
                db.session.commit()
            receita_ingrediente = ReceitaIngrediente(receita_id=nova_receita.id, ingrediente_id=ingrediente.id)
            db.session.add(receita_ingrediente)

        db.session.commit()
        return redirect(url_for('index'))

    return render_template('criar_receita.html')

@app.route('/chef/<int:chef_id>')
def detalhes_chef(chef_id):
    chef = Chef.query.get_or_404(chef_id)
    return render_template('detalhes_chef.html', chef=chef)

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)