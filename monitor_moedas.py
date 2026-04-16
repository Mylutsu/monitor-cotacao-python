import requests # Importamos a biblioteca para acessar a internet

def consultar_cotacao():
    # Endereço da API (esta é gratuita e não precisa de senha)
    url = "https://economia.awesomeapi.com.br/last/USD-BRL,EUR-BRL,BTC-BRL"
    
    try:
        # O Garçom (API) faz o pedido ao servidor
        requisicao = requests.get(url)
        
        # Transformamos a resposta em um "Dicionário" Python (JSON)
        dados = requisicao.json()
        
        # Extraímos apenas o que nos interessa (o valor de compra 'bid')
        dolar = dados['USDBRL']['bid']
        euro = dados['EURBRL']['bid']
        btc = dados['BTCBRL']['bid']
        
        print("-" * 30)
        print(" COTADOR DE MOEDAS AO VIVO ")
        print("-" * 30)
        print(f"Dólar: R$ {float(dolar):.2f}")
        print(f"Euro:  R$ {float(euro):.2f}")
        print(f"BTC:   R$ {float(btc):.2f}")
        print("-" * 30)

    except Exception as e:
        print(f"Ops, algo deu errado: {e}")

if __name__ == "__main__":
    consultar_cotacao()