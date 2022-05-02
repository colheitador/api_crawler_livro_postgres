# API-de-Crawler---Books-to-Scrape


Esta API foi desenvolvida para fins de web scraping, sendo seu alvo um site de livros.

As seguintes funcionalidades são oferecidas:

-Retornar as informações de N livros de uma categoria

-Fazer o crawleamento de uma categoria desejada e salvar as informações no banco de dados

-Apagar as informações de todos os livros de uma categoria

-Retornar os livros de uma categoria com estoque abaixo de N

_______________________________________________________________________________________________

Para utilizar a aplicação de forma não-dockerizada:
Abra o terminal, vá até a pasta onde se encontra o arquivo main.py e utilize o comando "uvicorn main:app --reload" para obter uma url, à qual deverá ser adicionada essa parte final do link:

/docs

Exemplo: http://0.0.0.0:80/docs
