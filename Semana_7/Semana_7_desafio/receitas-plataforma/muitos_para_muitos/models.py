from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Chef(db.Model):
    __tablename__ = 'chefs'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String, nullable=False)
    perfil = db.relationship('PerfilChef', back_populates='chef', uselist=False)
    receitas = db.relationship('Receita', back_populates='chef')

class PerfilChef(db.Model):
    __tablename__ = 'perfil_chefs'
    id = db.Column(db.Integer, primary_key=True)
    especialidade = db.Column(db.String, nullable=False)
    anos_experiencia = db.Column(db.Integer, nullable=False)
    chef_id = db.Column(db.Integer, db.ForeignKey('chefs.id'), nullable=False)
    chef = db.relationship('Chef', back_populates='perfil')

class Receita(db.Model):
    __tablename__ = 'receitas'
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String, nullable=False)
    instrucoes = db.Column(db.Text, nullable=False)
    chef_id = db.Column(db.Integer, db.ForeignKey('chefs.id'), nullable=False)
    chef = db.relationship('Chef', back_populates='receitas')
    ingredientes = db.relationship('Ingrediente', secondary='receita_ingredientes', back_populates='receitas')

class Ingrediente(db.Model):
    __tablename__ = 'ingredientes'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String, unique=True, nullable=False)
    receitas = db.relationship('Receita', secondary='receita_ingredientes', back_populates='ingredientes')

class ReceitaIngrediente(db.Model):
    __tablename__ = 'receita_ingredientes'
    receita_id = db.Column(db.Integer, db.ForeignKey('receitas.id'), primary_key=True)
    ingrediente_id = db.Column(db.Integer, db.ForeignKey('ingredientes.id'), primary_key=True)
    quantidade = db.Column(db.String, nullable=False)  # Ex: "2 xícaras", "100g"
    receita = db.relationship('Receita', back_populates='ingredientes')
    ingrediente = db.relationship('Ingrediente', back_populates='receitas')