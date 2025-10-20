from flask import Flask, render_template, request

app = Flask(__name__)

tarefas = []

@app.route('/', methods=['GET', 'POST'])
def lista():
    if request.method == 'POST':
        nova_tarefa = {
            'tarefa': request.form['tarefa'],
            'data_limite': request.form['data_limite']
        }
        tarefas.append(nova_tarefa)
        return render_template('show.html', tarefa=nova_tarefa['tarefa'])
    
    return render_template('lista.html', tarefas=tarefas)

if __name__ == '__main__':
    app.run(debug=True)