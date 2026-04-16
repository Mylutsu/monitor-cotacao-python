from flask import Flask, render_template, redirect, url_for, request # Adicionamos 'request'
import requests
import sqlite3

app = Flask(__name__)

# --- FUNÇÕES DE BANCO DE DADOS ---

def salvar_no_banco(moeda, valor):
    conn = sqlite3.connect('historico_moedas.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO cotacoes (moeda, valor) VALUES (?, ?)", (moeda, valor))
    conn.commit()
    conn.close()

def buscar_historico():
    conn = sqlite3.connect('historico_moedas.db')
    cursor = conn.cursor()
    # Adicionamos 'id' e 'observacao' na consulta
    cursor.execute("SELECT moeda, valor, data, observacao, id FROM cotacoes ORDER BY data DESC LIMIT 10")
    dados = cursor.fetchall()
    conn.close()
    return dados

def excluir_todos_dados():
    """Função para APAGAR (Delete) os registros da tabela"""
    conn = sqlite3.connect('historico_moedas.db')
    cursor = conn.cursor()
    # O comando DELETE apaga os registros. Sem o 'WHERE', ele limpa a tabela toda.
    cursor.execute("DELETE FROM cotacoes")
    conn.commit()
    conn.close()

def atualizar_observacao(id_registro, texto):
    """Função para ATUALIZAR (Update) um dado específico"""
    conn = sqlite3.connect('historico_moedas.db')
    cursor = conn.cursor()
    # Usamos o WHERE id = ? para garantir que só editaremos UMA linha específica
    cursor.execute("UPDATE cotacoes SET observacao = ? WHERE id = ?", (texto, id_registro))
    conn.commit()
    conn.close()

# --- ROTAS DO SITE ---

@app.route('/')
def index():
    # Mantivemos a lógica anterior
    url = "https://economia.awesomeapi.com.br/last/USD-BRL,EUR-BRL,BTC-BRL"
    try:
        requisicao = requests.get(url)
        dados = requisicao.json()
        
        # Salva no banco e prepara para exibir
        salvar_no_banco("Dólar", float(dados['USDBRL']['bid']))
        salvar_no_banco("Euro", float(dados['EURBRL']['bid']))
        
        cotacoes = {
            "dolar": f"{float(dados['USDBRL']['bid']):.2f}",
            "euro": f"{float(dados['EURBRL']['bid']):.2f}",
            "btc": f"{float(dados['BTCBRL']['bid']):.2f}"
        }
    except:
        cotacoes = None

    historico = buscar_historico()
    return render_template('index.html', moedas=cotacoes, lista=historico)

@app.route('/limpar')
def limpar():
    """Rota que chama a exclusão e volta para a página inicial"""
    excluir_todos_dados()
    # redirect(url_for('index')) faz o navegador voltar para a função 'index'
    return redirect(url_for('index'))

@app.route('/editar/<int:id>', methods=['POST'])
def editar(id):
    """Rota que recebe o formulário e atualiza o banco"""
    # Pegamos o texto que o usuário digitou no campo 'anotacao' do HTML
    novo_texto = request.form.get('anotacao')
    atualizar_observacao(id, novo_texto)
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)