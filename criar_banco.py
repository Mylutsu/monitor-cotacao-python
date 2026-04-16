import sqlite3 # Biblioteca padrão do Python para bancos de dados

# 1. Conecta ao arquivo do banco (se não existir, ele cria na hora)
conexao = sqlite3.connect('historico_moedas.db')

# 2. O 'cursor' é quem executa os comandos SQL dentro do banco
cursor = conexao.cursor()

# 3. Criamos a tabela usando a linguagem SQL
# Estamos criando colunas para: ID, Nome da Moeda, Valor e Data
cursor.execute('''
    CREATE TABLE IF NOT EXISTS cotacoes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        moeda TEXT NOT NULL,
        valor REAL NOT NULL,
        data TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')

conexao.commit() # Salva as alterações
conexao.close() # Fecha a conexão
print("Banco de dados e tabela criados com sucesso!")