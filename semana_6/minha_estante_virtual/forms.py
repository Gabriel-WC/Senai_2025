from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired
from wtforms_sqlalchemy.fields import QuerySelectField

class AutorForm(FlaskForm):
    nome = StringField('Nome do Autor', validators=[DataRequired()])
    submit = SubmitField('Adicionar Autor')

class LivroForm(FlaskForm):
    titulo = StringField('Título do Livro', validators=[DataRequired()])
    ano_publicacao = IntegerField('Ano de Publicação', validators=[DataRequired()])
    autor = QuerySelectField('Autor', get_label='nome', allow_blank=False, validators=[DataRequired()])
    submit = SubmitField('Adicionar Livro')