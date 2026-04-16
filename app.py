from flask import Flask, render_template
import requests

app = Flask(__name__)

def pegar_cotacoes():
    url = "https://economia.awesomeapi.com.br/last/USD-BRL,EUR-BRL,BTC-BRL"
    try:
        requisicao = requests.get(url)
        dados = requisicao.json()
        
        # Criamos um dicionário organizado para enviar ao HTML
        valores = {
            "dolar": f"{float(dados['USDBRL']['bid']):.2f}",
            "euro": f"{float(dados['EURBRL']['bid']):.2f}",
            "btc": f"{float(dados['BTCBRL']['bid']):.2f}"
        }
        return valores
    except:
        return None

# Definimos que, ao acessar a página inicial ('/'), o Python roda isso:
@app.route('/')
def index():
    cotacoes = pegar_cotacoes()
    # Aqui passamos a variável 'cotacoes' para dentro do index.html
    return render_template('index.html', moedas=cotacoes)

if __name__ == "__main__":
    app.run(debug=True)