import datetime
import locale
import requests

def data_atual_formatada():
    locale.setlocale(locale.LC_TIME, 'pt_BR')
    data_atual = datetime.datetime.now()
    dia_da_semana = data_atual.strftime('%A')
    data_formatada = f"{dia_da_semana.capitalize()} {data_atual.strftime('%d/%m/%Y')}"
    return data_formatada

def dia_string():
    locale.setlocale(locale.LC_TIME, 'pt_BR')
    data_atual = datetime.datetime.now()
    dia_da_semana = data_atual.strftime('%A')
    return dia_da_semana.capitalize()

def dia_amanha_string():
    data_atual = datetime.datetime.now() + datetime.timedelta(days=1)
    dia_da_semana = data_atual.strftime('%A')
    return dia_da_semana.capitalize()

def dia_atual():
    data_atual = datetime.datetime.now()
    dia = data_atual.day
    return dia

def mes_atual():
    data_atual = datetime.datetime.now()
    mes = data_atual.month
    return mes

def ano_atual():
    data_atual = datetime.datetime.now()
    ano = data_atual.year
    return ano

def hora_atual():
    return datetime.datetime.now().strftime("%H:%M:%S")

def clima():
    cidade = "NUMERO_DA_CIDADE|EX: 3445679"
    chave_api = "CHAVE_DA_API"
    url = f"https://api.openweathermap.org/data/2.5/weather?id={cidade}&appid={chave_api}&units=metric&lang=pt"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        descricao_clima = data['weather'][0]['description'].capitalize()
        temperatura = data['main']['temp']
        umidade = data['main']['humidity']
        return f"Clima em NOME_DA_CIDADE: {descricao_clima}, Temperatura: {temperatura}°C, Umidade: {umidade}%"
    else:
        return f"Não foi possível obter os dados do clima."