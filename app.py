from flask import Flask, jsonify
import requests

app = Flask(__name__)

# Configurações das APIs
WEATHER_API_KEY = 'b8021c278106c558d0b3ac31e6fac889'
NEWS_API_KEY = '38d4f1f048494650a0b57226a8493083'

# Função para buscar dados de clima
def obter_clima(cidade):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={cidade}&appid={WEATHER_API_KEY}&units=metric&lang=pt'
    resposta = requests.get(url)
    print(f"Clima Status Code: {resposta.status_code}")  # Depuração
    print(f"Clima JSON: {resposta.json()}")  # Depuração
    return resposta.json() if resposta.status_code == 200 else None

# Função para buscar manchetes de notícias
def obter_noticias():
    url = f'https://newsapi.org/v2/top-headlines?country=br&apiKey={NEWS_API_KEY}'
    resposta = requests.get(url)
    print(f"Notícias Status Code: {resposta.status_code}")  # Depuração
    print(f"Notícias JSON: {resposta.json()}")  # Depuração
    return resposta.json() if resposta.status_code == 200 else None

@app.route('/resumo_diario/<cidade>', methods=['GET'])
def resumo_diario(cidade):
    try:
        # Obtendo dados de clima e notícias
        clima = obter_clima(cidade)
        noticias = obter_noticias()

        if not clima or not noticias:
            return jsonify({'error': 'Erro ao buscar dados.'}), 500

        # Criando o resumo
        resumo = {
            'cidade': cidade,
            'clima': {
                'temperatura': clima['main']['temp'],
                'descricao': clima['weather'][0]['description']
            },
            'noticias': [noticia['title'] for noticia in noticias['articles'][:5]]  # Top 5 manchetes
        }

        return jsonify(resumo)
    except Exception as e:
        print(f"Erro interno: {e}")  # Exibe o erro para depuração
        return jsonify({'error': 'Erro interno no servidor.'}), 500

if __name__ == '__main__':
    app.run(debug=True)
