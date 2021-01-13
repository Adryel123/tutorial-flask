from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/formulario', methods=['GET'])
def get_form():
    return render_template("formulario.html")


@app.route('/trata-dados', methods=['POST'])
def validate_form():
    dados = request.form
    texto = f"Seu nome é {dados.get('name')}, seu endereço é {dados.get('address')} e você tem {dados.get('age')} anos :)"
    return texto


app.run()
