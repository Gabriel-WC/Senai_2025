class Chef(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String, nullable=False)
    perfil = db.relationship('PerfilChef', back_populates='chef', uselist=False)
    receitas = db.relationship('Receita', back_populates='chef')

class PerfilChef(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    especialidade = db.Column(db.String, nullable=False)
    anos_experiencia = db.Column(db.Integer, nullable=False)
    chef_id = db.Column(db.Integer, db.ForeignKey('chef.id'), unique=True)
    chef = db.relationship('Chef', back_populates='perfil')

class Receita(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String, nullable=False)
    instrucoes = db.Column(db.Text, nullable=False)
    chef_id = db.Column(db.Integer, db.ForeignKey('chef.id'))
    chef = db.relationship('Chef', back_populates='receitas')
    ingredientes = db.relationship('Ingrediente', secondary='receita_ingredientes', back_populates='receitas')

class Ingrediente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String, unique=True, nullable=False)
    receitas = db.relationship('Receita', secondary='receita_ingredientes', back_populates='ingredientes')

class ReceitaIngrediente(db.Model):
    __tablename__ = 'receita_ingredientes'
    receita_id = db.Column(db.Integer, db.ForeignKey('receita.id'), primary_key=True)
    ingrediente_id = db.Column(db.Integer, db.ForeignKey('ingrediente.id'), primary_key=True)
    quantidade = db.Column(db.String, nullable=False)