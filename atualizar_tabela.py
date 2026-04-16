import sqlite3

conn = sqlite3.connect('historico_moedas.db')
cursor = conn.cursor()

# O comando ALTER TABLE adiciona uma nova coluna a uma tabela que já existe
try:
    cursor.execute("ALTER TABLE cotacoes ADD COLUMN observacao TEXT")
    conn.commit()
    print("Coluna 'observacao' adicionada com sucesso!")
except:
    print("A coluna já existe ou houve um erro.")

conn.close()