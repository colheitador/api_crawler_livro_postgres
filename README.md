# API-de-Crawler---Books-to-Scrape


Esta API foi desenvolvida para fins de web scraping, sendo seu alvo um site de livros.

As seguintes funcionalidades são oferecidas:

-Retornar as informações de N livros de uma categoria

-Fazer o crawleamento de uma categoria desejada e salvar as informações no banco de dados

-Apagar as informações de todos os livros de uma categoria

-Retornar os livros de uma categoria com estoque abaixo de N

_______________________________________________________________________________________________

Para utilizar a aplicação na forma dockerizada:
Utilize o terminal para ir até o diretório onde o dockerfile se encontra.
Crie a imagem da seguinte forma: docker build -t <nome_para_a_imagem> .

Ex: docker build -t imagem_api_crawler_livro .


Em seguida, crie o container, lembrando-se de especificar as portas para conexão.
Utilize o seguinte formato: docker run --rm --name <nome_para_o_container> -p <porta>:<porta> <nome_ou_id_da_imagem>
  
Ex: docker run --rm --name container_api_crawler_livro -p 80:80 imagem_api_crawler_livro

Então, copie a url retornada pelo terminal e adicione "/docs" a ela para utilizar a aplicação no navegador.
Ex: http://0.0.0.0:80/docs

_______________________________________________________________________________________________

Para utilizar a aplicação de forma não-dockerizada:
Abra o terminal, vá até a pasta onde se encontra o arquivo main.py e utilize o comando "uvicorn main:app --reload" para obter uma url, à qual deverá ser adicionada essa parte final do link:

/docs

Exemplo: http://0.0.0.0:80/docs
