from flask import Flask, request
from inspirational_quotes import quote
from twilio.twiml.messaging_response import MessagingResponse
import time
import requests
import random

app = Flask(__name__)

API_KEY = "222edc7b8231694f092a8aa13a50e300"
endpoint = 'convert'
access_key = '8e603277fdca98bf0ed7766911237473'

def typing_delay(seconds=2):
    time.sleep(seconds)

def random_motivation():
    q = quote()
    return f"{q['quote']} - {q['author']}"

def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric&lang=pt_br"
    response = requests.get(url).json()
    temp = response['main']['temp']
    temp_description = response['weather'][0]['description']
    return f"A temperatura em {city} agora é de {temp}°C com {temp_description}."

def random_book(query="books"):
    url = f"https://www.googleapis.com/books/v1/volumes?q={query}&maxResults=40"
    response = requests.get(url).json()
    if 'items' in response:
        book = random.choice(response['items'])
        tittle = book['volumeInfo'].get('title', 'Título não disponível')
        author = ', '.join(book['volumeInfo'].get('authors', ['Autor desconhecido']))
        return f'{tittle} - {author}'
    return "Nenhum livro encontrado."

def get_exchange():
     url = f"https://api.exchangeratesapi.io/v1/latest?access_key={access_key}&symbols=USD,BRL"
     response = requests.get(url).json()
     usd_to_eur = 1 /  response['rates']['USD']
     usd_to_brl = usd_to_eur * response['rates']['BRL']
     return f"O dólar hoje está cotado a R${usd_to_brl:.2f}"

@app.route("/whatsapp", methods=['POST'])
def whatsapp_bot():
    incoming_msg = request.values.get('Body', '').lower()
    contact_name = request.values.get('ProfileName', 'usuário')
    resp = MessagingResponse()
    msg = resp.message()

    if any(x in incoming_msg for x in ['oi', 'olá', 'ola', 'dia', 'tarde', 'noite']):
        typing_delay(2) 
        msg.body(f"Olá, {contact_name}! Sou o seu assistente virtual. O que deseja saber ou fazer hoje?") #type: ignore
        return str(resp)
    
    if 'temperatura' in incoming_msg or 'clima' in incoming_msg:
        typing_delay(2)
        city = "Vila Velha"
        msg.body(get_weather(city))  #type: ignore
        return str(resp)
    
    if any(x in incoming_msg for x in ['cotacao', 'cotação', 'preco', 'valor', 'usd', 'dolar', 'dólar']):
        typing_delay(2)
        msg.body(get_exchange()) #type: ignore
        return str(resp)

        
    if 'livro' in incoming_msg or 'recomenda' in incoming_msg:
        typing_delay(2)
        msg.body(random_book()) #type: ignore
        return str(resp) 
    
    if 'frase' in incoming_msg or 'motivacao' in incoming_msg:
        typing_delay(2)
        msg.body(random_motivation())  # type: ignore
        return str(resp)

    typing_delay(2)
    msg.body("Desculpe, não entendi. Pode tentar perguntar de outro jeito?") #type: ignore
    return str(msg)

if __name__ == "__main__":
    app.run(port=5000)
