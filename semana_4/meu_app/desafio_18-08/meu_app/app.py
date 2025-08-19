from flask import Flask, render_template, flash, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo

app = Flask(__name__)
app.config['SECRET_KEY'] = 'uma_chave_de_seguranca_muito_dificil'

class FormularioRegistro(FlaskForm):
    nome = StringField('Nome Completo', validators=[DataRequired('Campo Obrigatório')])
    email = StringField('Email', validators=[
        DataRequired(message='Campo Obrigatório'),
        Email(message='Por favor, insira um e-mail válido')
    ])
    senha = PasswordField('Senha', validators=[
        DataRequired(message='Campo Obrigatório'),
        Length(min=8, message='A senha deve ter pelo menos 8 caracteres')
    ])
    confirmar_senha = PasswordField('Confirmar Senha', validators=[
        DataRequired(message='Campo Obrigatório'),
        EqualTo('senha', message='As senhas devem coincidir')
    ])
    biografia = TextAreaField('Biografia (opcional)')
    aceitar_termos = BooleanField('Aceito os Termos de Serviço', validators=[
        DataRequired(message='Você deve aceitar os termos para continuar')
    ])
    submit = SubmitField('Registrar')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    form = FormularioRegistro()

    if form.validate_on_submit():
        nome_usuario = form.nome.data
        bio_usuario = form.biografia.data

        mensagem = f'Bem-vindo(a), {nome_usuario}! '
        if bio_usuario:
            mensagem += f'Sua biografia: "{bio_usuario[:50]}..."'
        flash(mensagem, 'success')

        return redirect(url_for('registro'))

    return render_template('registro.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)
