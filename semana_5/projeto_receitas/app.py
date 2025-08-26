from flask import Flask, render_template, request, flash, redirect, url_for

app = Flask(__name__)
app.secret_key = 'minha_chave_secreta'

@app.route('/')
def index():
    return redirect(url_for('nova_receita'))

@app.route('/nova-receita', methods=['GET', 'POST'])
def nova_receita():
    if request.method == 'POST':
        nome = request.form.get('nome', '').strip()
        ingredientes = request.form.get('ingredientes', '').strip()
        modo_preparo = request.form.get('modo_preparo', '').strip()
        
        # Validação simples
        if not nome:
            flash('O nome da receita é obrigatório', 'erro')
        elif not ingredientes:
            flash('Os ingredientes são obrigatórios', 'erro')
        elif not modo_preparo:
            flash('O modo de preparo é obrigatório', 'erro')
        else:
            # Se tudo estiver preenchido, mostra a receita
            return render_template('receita_criada.html', 
                                 nome=nome, 
                                 ingredientes=ingredientes, 
                                 modo_preparo=modo_preparo)
    
    return render_template('receita.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)