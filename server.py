from flask import Flask, render_template, request
import telepot
import urllib3

# ------------------------------------------- #
proxy_url = "http://proxy.server:3128"
telepot.api._pools = {
    'default': urllib3.ProxyManager(proxy_url=proxy_url, num_pools=3, maxsize=10, retries=False, timeout=30),
}
telepot.api._onetime_pool_spec = (urllib3.ProxyManager, dict(
    proxy_url=proxy_url, num_pools=1, maxsize=1, retries=False, timeout=30))
# ------------------------------------------- #

TOKEN = 'seu token'
usuario = 'seu usuario do PA'
webhook = 'seu_segredo, pode ser o token do bot, por exemplo'

bot = telepot.Bot(TOKEN)
bot.setWebhook(
    f"https://{usuario}.pythonanywhere.com/{webhook}", max_connections=1)

app = Flask(__name__)


@app.route(f'/{webhook}', methods=["post"])
def trata_mensagem():
    """rota para receber requisições webhook do telegram"""
    mensagem = request.get_json()
    texto = mensagem["message"]["text"]
    id = mensagem["message"]["chat"]["id"]

    if texto.startsWith("/form"):
        bot.sendMessage(id, f"https://{usuario}.pythonanywhere.com/formulario")
    return "ok"


@app.route('/formulario', methods=['GET'])
def get_form():
    """rota para o formulário"""
    return render_template("formulario.html")


@app.route('/trata-dados', methods=['POST'])
def validate_form():
    """rota que recebe os dados do formulário"""
    dados = request.form
    texto = f"Seu nome é {dados.get('name')}, seu endereço é {dados.get('address')} e você tem {dados.get('age')} anos :)"
    try:
        bot.sendMessage(dados.get('id_telegram'), texto)
    except:
        pass

    return texto
