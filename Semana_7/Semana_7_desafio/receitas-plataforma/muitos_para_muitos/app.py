from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'sua_chave_secreta_aqui'

db = SQLAlchemy(app)

# Modelos
class Chef(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    perfil = db.relationship('PerfilChef', backref='chef', uselist=False, cascade='all, delete-orphan')
    receitas = db.relationship('Receita', backref='chef', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Chef {self.nome}>'

class PerfilChef(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    especialidade = db.Column(db.String(100), nullable=False)
    anos_experiencia = db.Column(db.Integer, nullable=False)
    chef_id = db.Column(db.Integer, db.ForeignKey('chef.id'))

class Receita(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    instrucoes = db.Column(db.Text, nullable=False)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    chef_id = db.Column(db.Integer, db.ForeignKey('chef.id'))
    ingredientes = db.relationship('ReceitaIngrediente', backref='receita', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Receita {self.titulo}>'

class Ingrediente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), unique=True, nullable=False)
    receitas = db.relationship('ReceitaIngrediente', backref='ingrediente')

    def __repr__(self):
        return f'<Ingrediente {self.nome}>'

class ReceitaIngrediente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    receita_id = db.Column(db.Integer, db.ForeignKey('receita.id'))
    ingrediente_id = db.Column(db.Integer, db.ForeignKey('ingrediente.id'))
    quantidade = db.Column(db.String(50))

# Rotas
@app.route('/')
def index():
    receitas = Receita.query.order_by(Receita.data_criacao.desc()).all()
    return render_template('index.html', receitas=receitas)

@app.route('/receita/nova', methods=['GET', 'POST'])
def criar_receita():
    chefs = Chef.query.all()
    
    if request.method == 'POST':
        titulo = request.form['titulo']
        instrucoes = request.form['instrucoes']
        chef_id = int(request.form['chef_id'])
        ingredientes_texto = request.form.get('ingredientes', '')
        
        if not titulo or not instrucoes or not chef_id:
            flash('Por favor, preencha todos os campos obrigatórios.', 'error')
            return render_template('criar_receita.html', chefs=chefs)
        
        # Criar a receita
        receita = Receita(titulo=titulo, instrucoes=instrucoes, chef_id=chef_id)
        db.session.add(receita)
        db.session.commit()
        
        # Processar ingredientes
        if ingredientes_texto:
            linhas = ingredientes_texto.strip().split('\n')
            for linha in linhas:
                if ':' in linha:
                    partes = linha.split(':', 1)
                    nome_ingrediente = partes[0].strip()
                    quantidade = partes[1].strip() if len(partes) > 1 else ''
                else:
                    nome_ingrediente = linha.strip()
                    quantidade = ''
                
                if nome_ingrediente:
                    # Verificar se o ingrediente já existe
                    ingrediente = Ingrediente.query.filter_by(nome=nome_ingrediente).first()
                    if not ingrediente:
                        ingrediente = Ingrediente(nome=nome_ingrediente)
                        db.session.add(ingrediente)
                        db.session.commit()
                    
                    # Associar ingrediente à receita
                    receita_ingrediente = ReceitaIngrediente(
                        receita_id=receita.id,
                        ingrediente_id=ingrediente.id,
                        quantidade=quantidade
                    )
                    db.session.add(receita_ingrediente)
        
        db.session.commit()
        flash('Receita criada com sucesso!', 'success')
        return redirect(url_for('index'))
    
    return render_template('criar_receita.html', chefs=chefs)

@app.route('/chef/novo', methods=['GET', 'POST'])
def criar_chef():
    if request.method == 'POST':
        nome = request.form['nome']
        especialidade = request.form['especialidade']
        anos_experiencia = request.form['anos_experiencia']
        
        if not nome or not especialidade or not anos_experiencia:
            flash('Por favor, preencha todos os campos.', 'error')
            return render_template('criar_chef.html')
        
        chef = Chef(nome=nome)
        db.session.add(chef)
        db.session.commit()
        
        perfil = PerfilChef(
            especialidade=especialidade,
            anos_experiencia=anos_experiencia,
            chef_id=chef.id
        )
        db.session.add(perfil)
        db.session.commit()
        
        flash('Chef criado com sucesso!', 'success')
        return redirect(url_for('index'))
    
    return render_template('criar_chef.html')

@app.route('/chef/<int:chef_id>')
def detalhes_chef(chef_id):
    chef = Chef.query.get_or_404(chef_id)
    return render_template('detalhes_chef.html', chef=chef)

@app.route('/receita/<int:receita_id>')
def detalhes_receita(receita_id):
    receita = Receita.query.get_or_404(receita_id)
    return render_template('detalhes_receita.html', receita=receita)

@app.route('/chefs')
def listar_chefs():
    chefs = Chef.query.all()
    return render_template('chefs.html', chefs=chefs)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  
    app.run(debug=True, port=5000)