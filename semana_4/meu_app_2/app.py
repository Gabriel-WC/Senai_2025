import os
from datetime import datetime
from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SelectField
from wtforms.fields import DateField
from wtforms.validators import DataRequired, Email, ValidationError

# --- Configuração da Aplicação Flash ---
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

# Validador personalizado para data
def validar_data_futura(form, field):
    if field.data and field.data < datetime.now().date():
        raise ValidationError('A data do evento deve ser futura.')

# --- Definição do Formulário com WTForms ---
class EventoForm(FlaskForm):
    """Define os campos e validadores para o formulário de evento."""
    nome_evento = StringField(
        'Nome do Evento',
        validators=[DataRequired(message="O campo nome do evento é obrigatório.")]
    )
    data_evento = DateField(
        'Data do Evento',
        format='%Y-%m-%d',
        validators=[
            DataRequired(message="O campo data do evento é obrigatório."),
            validar_data_futura
        ]
    )
    organizador = StringField(
        'Organizador',
        validators=[DataRequired(message="O campo organizador é obrigatório.")]
    )
    email = StringField(
        'E-mail',
        validators=[
            DataRequired(message="O campo e-mail é obrigatório."),
            Email(message="Por favor, insira um e-mail válido.")
        ]
    )
    tipo_evento = SelectField(
        'Tipo de Evento',
        choices=[
            ('', 'Selecione...'),
            ('palestra', 'Palestra'),
            ('workshop', 'Workshop'),
            ('meetup', 'Meetup'),
            ('outro', 'Outro')
        ],
        validators=[DataRequired(message="Por favor, selecione o tipo do evento.")]
    )
    descricao = TextAreaField('Descrição')
    enviar = SubmitField('Enviar')

    # Validação condicional para descrição
    def validate_descricao(self, field):
        if self.tipo_evento.data == 'outro' and not field.data:
            raise ValidationError('Por favor, forneça uma descrição para o evento do tipo "Outro".')

# --- Definição de um Objeto para Simulação ---
class Evento:
    def __init__(self, nome_evento, data_evento, organizador, email, tipo_evento, descricao=""):
        self.nome_evento = nome_evento
        self.data_evento = data_evento
        self.organizador = organizador
        self.email = email
        self.tipo_evento = tipo_evento
        self.descricao = descricao

# --- Rotas da Aplicação ---
@app.route("/")
def index():
    return render_template('index.html')

@app.route('/vazio', methods=['GET', 'POST'])
def formulario_vazio():
    """Cenário 1: Formulário Vazio."""
    form = EventoForm()
    
    if form.validate_on_submit():
        nome_evento = form.nome_evento.data
        return render_template('sucesso.html', nome_evento=nome_evento)
    
    return render_template(
        'formulario.html',
        form=form,
        title="1. Formulário Vazio"
    )

@app.route("/via-argumentos", methods=['GET', 'POST'])
def formulario_via_argumentos():
    """Cenário 2: Formulário Preenchido via Argumentos."""
    form = EventoForm()
    
    if form.validate_on_submit():
        nome_evento = form.nome_evento.data
        return render_template('sucesso.html', nome_evento=nome_evento)
    
    elif not form.is_submitted():
        dados_iniciais = {
            'nome_evento': 'Tech Conference 2023',
            'data_evento': datetime(2023, 12, 31).date(),
            'organizador': 'João da Silva',
            'email': 'joao.silva@email.com',
            'tipo_evento': 'palestra',
            'descricao': 'Uma conferência sobre as últimas tendências em tecnologia.'
        }
        form = EventoForm(**dados_iniciais)
    
    return render_template(
        'formulario.html',
        form=form,
        title="2. Formulário Preenchido via Argumentos"
    )

@app.route("/via-objeto", methods=['GET', 'POST'])
def formulario_via_objeto():
    """Cenário 3: Formulário Preenchido via Objeto."""
    form = EventoForm()
    
    if form.validate_on_submit():
        nome_evento = form.nome_evento.data
        return render_template('sucesso.html', nome_evento=nome_evento)
    
    elif not form.is_submitted():
        evento_mock = Evento(
            nome_evento="Workshop de Python",
            data_evento=datetime(2023, 11, 15).date(),
            organizador="Maria Oliveira",
            email="maria.o@email.net",
            tipo_evento="workshop",
            descricao="Um workshop prático sobre desenvolvimento em Python."
        )
        form = EventoForm(obj=evento_mock)
    
    return render_template(
        'formulario.html',
        form=form,
        title="3. Formulário Preenchido via Objeto"
    )

# --- Execução da Aplicação ---
if __name__ == '__main__':
    app.run(debug=True)