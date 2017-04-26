import requests
from flask import Flask, Response
from bs4 import BeautifulSoup
import json
import urllib.request
import shutil

app = Flask(__name__)

urlGlobal = 'http://repositorio.uniceub.br'
@app.route('/')
def index():

    # download()

    primeiroValor = [] ;
    segundoValor = [] ;

    url = urlGlobal + '/handle/123456789/1650/browse?type=author&submit_browse=Todos+os+autores'
    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, "html")

    for td in soup.find_all('td', {'class': 'oddRowOddCol'}):
       for link in td.find_all('a'):
           href = link.get('href')
           # print(td.text)
           # print(href)
           primeiroValor.append(primeiroPC(href))

    for td in soup.find_all('td', {'class': 'evenRowOddCol'}):
       for link in td.find_all('a'):
           href = link.get('href')
           # print(td.text)
           # print(href)
           segundoValor.append(primeiroPC(href))

    valores = primeiroValor + segundoValor
    return Response(json.dumps(valores), mimetype='application/json')



def primeiroPC(href):
    url = urlGlobal + href
    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, "html")
    for td in soup.find_all('td', {'headers': 't2'}):
       for link in td.find_all('a'):
           href = link.get('href')
           # print(href)
           pdf = segundoPC(href)
           return pdf

def segundoPC(href):
    url = urlGlobal + href
    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, "html")
    for td in soup.find_all('td', {'align': 'center'}):
       for link in td.find_all('a'):
           href = link.get('href')
           # print(urlGlobal+href)
           return {'linkPDF':urlGlobal+href}

def download():
    url = 'http://repositorio.uniceub.br/bitstream/123456789/3139/2/20516680.pdf'

    with urllib.request.urlopen(url) as response, open("novoarquivo", 'wb') as out_file:
        shutil.copyfileobj(response, out_file)

if __name__ == '__main__':
    app.run(debug=True)
