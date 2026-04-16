from flask import Flask, render_template
import requests
import sqlite3 # Importamos o banco aqui também

app = Flask(__name__)

def salvar_no_banco(moeda, valor):
    """Função para INSERIR (Create) dados no SQL"""
    conn = sqlite3.connect('historico_moedas.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO cotacoes (moeda, valor) VALUES (?, ?)", (moeda, valor))
    conn.commit()
    conn.close()

def buscar_historico():
    """Função para LER (Read) os últimos 5 registros"""
    conn = sqlite3.connect('historico_moedas.db')
    cursor = conn.cursor()
    # SQL para pegar os últimos 5 registros do mais novo para o mais antigo
    cursor.execute("SELECT moeda, valor, data FROM cotacoes ORDER BY data DESC LIMIT 5")
    dados = cursor.fetchall()
    conn.close()
    return dados

def pegar_cotacoes():
    url = "https://economia.awesomeapi.com.br/last/USD-BRL,EUR-BRL,BTC-BRL"
    try:
        requisicao = requests.get(url)
        dados = requisicao.json()
        
        # Salvando as cotações no banco de dados toda vez que atualiza
        salvar_no_banco("Dólar", float(dados['USDBRL']['bid']))
        salvar_no_banco("Euro", float(dados['EURBRL']['bid']))
        
        return {
            "dolar": f"{float(dados['USDBRL']['bid']):.2f}",
            "euro": f"{float(dados['EURBRL']['bid']):.2f}",
            "btc": f"{float(dados['BTCBRL']['bid']):.2f}"
        }
    except:
        return None

@app.route('/')
def index():
    cotacoes = pegar_cotacoes()
    historico = buscar_historico() # Buscamos a lista do banco
    return render_template('index.html', moedas=cotacoes, lista=historico)

if __name__ == "__main__":
    app.run(debug=True)