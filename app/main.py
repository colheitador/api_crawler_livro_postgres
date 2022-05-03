# importar pacotes importantes

from fastapi import FastAPI, HTTPException # para trabalhar com a API
import psycopg2 # banco de dados
import json # trabalhar com dicionários
import requests # parte de crawlear de novo
from bs4 import BeautifulSoup # parte de crawlear de novo
import datetime # registrar a data de crawleamento
import socket # obter o IP do host

# nome para chamar o FastAPI
app = FastAPI()


## parâmetros pra conectar com o banco de dados
dbname = "livros"
user = "postgres"
password = "postgresql"
#agora vamos usar o pacote "socket" para obter o ip pra colocar em "host"
host_name = socket.gethostname()
ip_local = socket.gethostbyname(host_name)
host = ip_local

# juntar os parâmetros pra fazer a conexão
conn_string = "host={0} user={1} dbname={2} password={3}".format(host, user, dbname, password)
con2 = psycopg2.connect(conn_string)
cursor2 = con2.cursor()

# criar a tabela do banco de dados, caso ela não exista
@app.post("/books4/crawlear_tudo")
def crawlear_tudo(sim_ou_nao : str): ## função para crawlear, tendo a categoria e seu link como parâmetros (serão especificados depois)
        
    # tratamento de erro pro caso de o usuário digitar uma categoria não catalogada
    if f'{sim_ou_nao}' not in ["sim","Sim","s","S","crawlear","Crawlear","crawl","Crawl","scrape","Scrape"]:
        raise HTTPException(
            status_code=404,
            detail={'Se quiser mesmo crawlear tudo, digite alguma dessas opções':' "sim","Sim","s","S","crawlear","Crawlear","crawl","Crawl","scrape","Scrape"'},
            headers={"Erro": "Crawleamento não executado"},
        )
    else:
        # se o usuário pediu pra crawlear:

        response_tudo = requests.get("https://books.toscrape.com/index.html")
        deletar1 = 'DROP TABLE IF EXISTS tab_livros'
        cursor2.execute(deletar1)
        propriedades_tabela_crawlear_tudo = "CREATE TABLE IF NOT EXISTS tab_livros (titulo VARCHAR(300), descricao TEXT, preco REAL, disponibilidade VARCHAR(150), categoria VARCHAR(150), data TEXT)"
        cursor2.execute(propriedades_tabela_crawlear_tudo)

        # caso o código bugue, executar essa linha do rollback aí pode resolver
        #cursor2.execute("ROLLBACK")
        #con2.commit()

        page1 = BeautifulSoup(response_tudo.content, 'html.parser')

        def crawlear_todas_as_categorias(category, link):
            urlBase_tudo = "https://books.toscrape.com/"

            response_tudo = requests.get(urlBase_tudo + link)
            page_tudo = BeautifulSoup(response_tudo.content, 'html.parser')

            for item in page_tudo.find_all('article', 'product_pod'): # iterar todos os livros listados
                bookUrl_tudo = urlBase_tudo + item.find('a').attrs['href'].replace("../../../", "catalogue/")
                bookResponse_tudo = requests.get(bookUrl_tudo)
                bookPage_tudo = BeautifulSoup(bookResponse_tudo.content, 'html.parser')

                paragraphs_tudo = bookPage_tudo.find("article", "product_page").find_all("p")
                title_tudo = bookPage_tudo.find('h1').text
                title2_tudo = title_tudo.replace("'"," ") ## replace pra ignorar as aspas duplas
                description_tudo = paragraphs_tudo[3]
                description2_tudo = description_tudo.text.replace("'"," ") ## replace pra ignorar as aspas duplas
                price_tudo = paragraphs_tudo[0].text[1:]
                availability_tudo = paragraphs_tudo[1].text.strip()[10:12]
                day_tudo = str(datetime.date.today())
                print("=================================")
                print("Title: " + title2_tudo)
                print("Price: " + price_tudo)
                print("In stock: " + availability_tudo)
                print("Category: " + category)
                print("Description: " + description2_tudo)
                print("Data de crawleamento: " + day_tudo)
        
                cursor2.execute(f"INSERT INTO tab_livros (titulo, descricao, preco, disponibilidade, categoria, data) VALUES ('{title2_tudo}', '{description2_tudo}', '{price_tudo}', '{availability_tudo}', '{category}', '{day_tudo}')")
    
            next_tudo = page_tudo.find("li", "next") # checar se há uma nova página
            if next_tudo is not None:
                nextLink_tudo = next_tudo.find("a").attrs["href"]
                parts_tudo = link_tudo.split("/") ## essa parte é pra corrigir o problema de não listar todos os livros com o botão Next
                parts_tudo[-1] = nextLink_tudo
                nextLink_tudo = "/".join(parts_tudo)
                crawlear_todas_as_categorias(category, nextLink_tudo)

        urlBase_tudo = "https://books.toscrape.com/"

        for item in page1.find('aside').find_all('li')[1:]: # iterar por categorias
            link_tudo = item.find('a').attrs['href']
            category = item.text.strip()
            crawlear_todas_as_categorias(category, link_tudo)

    return "Todas as categorias foram crawleadas"


###---------------------------------------------------------------------------------------
###---------------------------------------------------------------------------------------
###---------------------------------------------------------------------------------------
###---------------------------------------------------------------------------------------
###---------------------------------------------------------------------------------------


# função para que a API peça uma categoria e um número N de livros para exibir o resultado
@app.get("/books/")
def ler_n_livros_de_tal_categoria(category: str, n_books: int = 10):
	
	
# para isso, vamos criar um filtro para que apenas a categoria desejada seja mostrada	
	selecionar = f"SELECT * FROM tab_livros WHERE categoria = '{category.title()}'"
	lista_de_dicionarios = []
	cursor2.execute(selecionar, f'{(category.title(),)}')

# tratamento de erro pro caso de o usuário digitar uma categoria não catalogada
	if f'{category.title()}' not in ["Travel","Mystery","Historical Fiction","Sequential Art","Classics","Philosophy","Romance","Womens Fiction","Fiction","Childrens","Religion","Nonfiction","Music","Default","Science Fiction","Sports and Games","Add a comment","Fantasy","New Adult","Young Adult","Science","Poetry","Paranormal","Art","Psychology","Autobiography","Parenting","Adult Fiction","Humor","Horror","History","Food and Drink","Christian Fiction","Business","Biography","Thriller","Contemporary","Spirituality","Academic","Self Help","Historical","Christian","Suspense","Short Stories","Novels","Health","Politics","Cultural","Erotica","Crime"]:
		raise HTTPException(
            status_code=404,
            detail={'A categoria tem que ser alguma dessas':' "Travel","Mystery","Historical Fiction","Sequential Art","Classics","Philosophy","Romance","Womens Fiction","Fiction","Childrens","Religion","Nonfiction","Music","Default","Science Fiction","Sports and Games","Add a comment","Fantasy","New Adult","Young Adult","Science","Poetry","Paranormal","Art","Psychology","Autobiography","Parenting","Adult Fiction","Humor","Horror","History","Food and Drink","Christian Fiction","Business","Biography","Thriller","Contemporary","Spirituality","Academic","Self Help","Historical","Christian","Suspense","Short Stories","Novels","Health","Politics","Cultural","Erotica","Crime"'},
            headers={"Erro": "Ta errado aí bicho"},
        )
	
# voltando ao caso de o usuário digitar certo	
	armazenar_dados2 = cursor2.fetchall()
	for cada_livro_dessa_cat in armazenar_dados2:
		cada_dicionario_de_livro = {
        "titulo": cada_livro_dessa_cat[0],
        "descricao": cada_livro_dessa_cat[1],
        "preco": cada_livro_dessa_cat[2],
		"disponibilidade": cada_livro_dessa_cat[3],
		"categoria": cada_livro_dessa_cat[4],
        "data de crawleamento": cada_livro_dessa_cat[5]
		}
		
# adicionar os dicionários (com conteúdo de livros) a uma lista para mostrar na tela
		lista_de_dicionarios.append(cada_dicionario_de_livro)


#----------------------------------------------------------


## agora vamos definir o numero "n" de livros mostrados
	
	if len(lista_de_dicionarios) < n_books:
		mostrar_quantos_puder = len(lista_de_dicionarios)
	else:
		mostrar_quantos_puder = n_books

	lista_de_n_dicionarios_retorno = lista_de_dicionarios[:mostrar_quantos_puder]
	
#----------------------------------------------------------

# resultado da função em .json:

	return json.dumps(lista_de_n_dicionarios_retorno)




## caso queira o resultado da função sem o formato .json:

#	return lista_de_n_dicionarios_retorno



###---------------------------------------------------------------------------------------
###---------------------------------------------------------------------------------------
###---------------------------------------------------------------------------------------
###---------------------------------------------------------------------------------------
###---------------------------------------------------------------------------------------

# nova função: deletar categorias do banco de dados
@app.delete("/books2/del/")
def deletar_categoria(category:str):

	deletar_db = f"DELETE FROM tab_livros WHERE categoria = '{category.title()}'"
	cursor2.execute(deletar_db, f'{(category.title(),)}')
    # tratamento de erro pro caso de o usuário digitar uma categoria não catalogada
	if f'{category.title()}' not in ["Travel","Mystery","Historical Fiction","Sequential Art","Classics","Philosophy","Romance","Womens Fiction","Fiction","Childrens","Religion","Nonfiction","Music","Default","Science Fiction","Sports and Games","Add a comment","Fantasy","New Adult","Young Adult","Science","Poetry","Paranormal","Art","Psychology","Autobiography","Parenting","Adult Fiction","Humor","Horror","History","Food and Drink","Christian Fiction","Business","Biography","Thriller","Contemporary","Spirituality","Academic","Self Help","Historical","Christian","Suspense","Short Stories","Novels","Health","Politics","Cultural","Erotica","Crime"]:
		raise HTTPException(
            status_code=404,
            detail={'A categoria tem que ser alguma dessas':' "Travel","Mystery","Historical Fiction","Sequential Art","Classics","Philosophy","Romance","Womens Fiction","Fiction","Childrens","Religion","Nonfiction","Music","Default","Science Fiction","Sports and Games","Add a comment","Fantasy","New Adult","Young Adult","Science","Poetry","Paranormal","Art","Psychology","Autobiography","Parenting","Adult Fiction","Humor","Horror","History","Food and Drink","Christian Fiction","Business","Biography","Thriller","Contemporary","Spirituality","Academic","Self Help","Historical","Christian","Suspense","Short Stories","Novels","Health","Politics","Cultural","Erotica","Crime"'},
            headers={"Erro": "Ta errado aí bicho"},
        )
	con2.commit()
	
    

	return "categoria deletada"



###---------------------------------------------------------------------------------------
###---------------------------------------------------------------------------------------
###---------------------------------------------------------------------------------------
###---------------------------------------------------------------------------------------
###---------------------------------------------------------------------------------------

# função para crawlear uma única categoria
@app.put("/books3/crawlear_uma_categoria")
def crawlear_categoria(categoria_digitada : str): ## função para crawlear, tendo a categoria e seu link como parâmetros (serão especificados depois)
    import datetime
        
        # tratamento de erro pro caso de o usuário digitar uma categoria não catalogada
    if f'{categoria_digitada.title()}' not in ["Travel","Mystery","Historical Fiction","Sequential Art","Classics","Philosophy","Romance","Womens Fiction","Fiction","Childrens","Religion","Nonfiction","Music","Default","Science Fiction","Sports and Games","Add a comment","Fantasy","New Adult","Young Adult","Science","Poetry","Paranormal","Art","Psychology","Autobiography","Parenting","Adult Fiction","Humor","Horror","History","Food and Drink","Christian Fiction","Business","Biography","Thriller","Contemporary","Spirituality","Academic","Self Help","Historical","Christian","Suspense","Short Stories","Novels","Health","Politics","Cultural","Erotica","Crime"]:
        raise HTTPException(
            status_code=404,
            detail={'A categoria tem que ser alguma dessas':' "Travel","Mystery","Historical Fiction","Sequential Art","Classics","Philosophy","Romance","Womens Fiction","Fiction","Childrens","Religion","Nonfiction","Music","Default","Science Fiction","Sports and Games","Add a comment","Fantasy","New Adult","Young Adult","Science","Poetry","Paranormal","Art","Psychology","Autobiography","Parenting","Adult Fiction","Humor","Horror","History","Food and Drink","Christian Fiction","Business","Biography","Thriller","Contemporary","Spirituality","Academic","Self Help","Historical","Christian","Suspense","Short Stories","Novels","Health","Politics","Cultural","Erotica","Crime"'},
            headers={"Erro": "Ta errado aí bicho"},
        )


    def crawlPage2(categoria_digitada : str, link_da_categoria):
    
        urlBase_cada_categoria = "https://books.toscrape.com/" ## essa é a url à qual serão adicionadas outras partes de link

        response_para_a_categoria = requests.get(urlBase_cada_categoria + link_da_categoria) ## adiciona à urlBase o link obtido láaa embaixo no código
        page_categoria = BeautifulSoup(response_para_a_categoria.content, 'html.parser') ## coloca em "page" o conteúdo da página lido pelo beautifulsoup

        #print(page_categoria)
    
        # iterar todos os livros listados
        for item in page_categoria.find_all('article', 'product_pod'): ## passa por todos os livros (demarcados por "article" e "product_pod")
            bookUrl = urlBase + item.find('a').attrs['href'].replace("../../../", "catalogue/") ## adiciona à urlBase o link da categoria
            bookResponse = requests.get(bookUrl) ## bota o requests pra entrar nessa nova url (de cada categoria)
            bookPage = BeautifulSoup(bookResponse.content, 'html.parser') ## usa o beautifulsoup pra ler a página como html

            paragraphs = bookPage.find("article", "product_page").find_all("p")
            title = bookPage.find('h1').text
            title2 = title.replace("'"," ") ## replace pra ignorar as aspas duplas
            description = paragraphs[3]
            description2 = description.text.replace("'"," ") ## replace pra ignorar as aspas duplas
            price = paragraphs[0].text[1:]
            availability = paragraphs[1].text.strip()[10:12]
            day = str(datetime.date.today())
            print("=================================")
            print("Title: " + title2)
            print("Price: " + price)
            print("In stock: " + availability)
            print("Category: " + categoria_digitada)
            print("Description: " + description2)
            print("Data de Crawleamento: " + day)
        
            cursor2.execute(f"INSERT INTO tab_livros (titulo, descricao, preco, disponibilidade, categoria, data) VALUES ('{title2}', '{description2}', '{price}', '{availability}', '{categoria_digitada}', '{day}')")
        
        con2.commit()
        return "os dados dessa categoria foram salvos em 'db_pra_uma_categoria.db'"
    
        next = page_categoria.find("li", "next") # checar se há uma nova página
        if next is not None:
            nextLink = next.find("a").attrs["href"]
            parts = link_da_categoria.split("/") ## essa parte é pra corrigir o problema de não listar todos os livros com o botão Next
            parts[-1] = nextLink
            nextLink = "/".join(parts)
            crawlPage2(categoria_digitada.title(), nextLink)
    





    # agora vamos pegar as informações pra botar na tabela
    response_para_categoria = requests.get("https://books.toscrape.com/index.html")
    page_para_categoria = BeautifulSoup(response_para_categoria.content, 'html.parser') ## usa o beautifulsoup pra ler o conteúdo como html 
    #print(page) ## printa pra que vejamos as <tags> pra nos orientar na busca dos dados
    urlBase = "https://books.toscrape.com/"

    # iterar por categorias

    categorias_e_links = {}

    for item in page_para_categoria.find('aside').find_all('li')[1:]: ##encontrar as categorias (marcadas por "li") e excluir a primeira (books)
        link = item.find('a').attrs['href'] ##pegar o link (marcado por "href" em "a")
        category = item.text.strip() ## a categoria é o nome escrito no item e strip é pra tirar os espaços
        categorias_e_links.update({category:link}) ## faz um dicionário com categorias e seus respectivos links
    #print(categorias_e_links)

    #agora vamos transformar o dicionario em json para facilitar a busca pelo link de uma categoria desejada
    import json
    dict_cat_link_em_json = json.dumps(categorias_e_links) ## transforma em .json
    buscar_link_da_categoria = json.loads(dict_cat_link_em_json) ## permite a busca pelo valor de uma chave
    # categoria_digitada = "suspense" # para testes
    link_da_categoria = buscar_link_da_categoria[categoria_digitada.title()] ## pega o link da categoria entre colchetes
    #print(buscar_link_da_categoria[categoria_digitada])
    crawlPage2(categoria_digitada.title(), link_da_categoria) ## chama a função de crawlear
    
    return "categoria adicionada"
    

###---------------------------------------------------------------------------------------
###---------------------------------------------------------------------------------------
###---------------------------------------------------------------------------------------
###---------------------------------------------------------------------------------------
###---------------------------------------------------------------------------------------



# função para mostrar livros com estoque abaixo de N (em uma única categoria)
@app.get("/books4/mostrar_livros_com_estoque_abaixo_de")
def menos_que_n_livros_e_categoria_especifica(category: str, menos_de_n_em_estoque: int = 10):

# para isso, vamos criar um filtro para que apenas a categoria desejada seja mostrada	
	selecionar5 = f"SELECT * FROM tab_livros WHERE categoria = '{category.title()}'"
	lista_de_dicionarios5 = []
	cursor2.execute(selecionar5, f'{(category.title(),)}')

# tratamento de erro pro caso de o usuário digitar uma categoria não catalogada
	if f'{category.title()}' not in ["Travel","Mystery","Historical Fiction","Sequential Art","Classics","Philosophy","Romance","Womens Fiction","Fiction","Childrens","Religion","Nonfiction","Music","Default","Science Fiction","Sports and Games","Add a comment","Fantasy","New Adult","Young Adult","Science","Poetry","Paranormal","Art","Psychology","Autobiography","Parenting","Adult Fiction","Humor","Horror","History","Food and Drink","Christian Fiction","Business","Biography","Thriller","Contemporary","Spirituality","Academic","Self Help","Historical","Christian","Suspense","Short Stories","Novels","Health","Politics","Cultural","Erotica","Crime"]:
		raise HTTPException(
            status_code=404,
            detail={'A categoria tem que ser alguma dessas':' "Travel","Mystery","Historical Fiction","Sequential Art","Classics","Philosophy","Romance","Womens Fiction","Fiction","Childrens","Religion","Nonfiction","Music","Default","Science Fiction","Sports and Games","Add a comment","Fantasy","New Adult","Young Adult","Science","Poetry","Paranormal","Art","Psychology","Autobiography","Parenting","Adult Fiction","Humor","Horror","History","Food and Drink","Christian Fiction","Business","Biography","Thriller","Contemporary","Spirituality","Academic","Self Help","Historical","Christian","Suspense","Short Stories","Novels","Health","Politics","Cultural","Erotica","Crime"'},
            headers={"Erro": "Ta errado aí bicho"},
        )
	
    # voltando ao caso de o usuário digitar certo	
	armazenar_dados5 = cursor2.fetchall()
	for cada_livro_dessa_cat in armazenar_dados5:
		cada_dicionario_de_livro5 = {
        "titulo": cada_livro_dessa_cat[0],
        "descricao": cada_livro_dessa_cat[1],
        "preco": cada_livro_dessa_cat[2],
		"disponibilidade": cada_livro_dessa_cat[3],
		"categoria": cada_livro_dessa_cat[4],
		"data de crawleamento": str(datetime.date.today())
		}
		dicionarios5_json = json.dumps(cada_dicionario_de_livro5) #transformando em json para facilitar a leitura dos valores de disponibilidade
		procurar_valores_de_disponibilidade = json.loads(dicionarios5_json)
#print(int(procurar_valores_de_disponibilidade["disponibilidade"]))
		if (int(procurar_valores_de_disponibilidade["disponibilidade"])) < menos_de_n_em_estoque:
				lista_de_dicionarios5.append(dicionarios5_json) # adicionar os dicionários (com conteúdo de livros) que tenham estoque menor que o informado pelo usuário
                
				# caso queira mostrar sem o formato.json, comente a linha acima e descomente a de baixo
				# lista_de_dicionarios5.append(cada_dicionario_de_livro5) # adicionar os dicionários (com conteúdo de livros) que tenham estoque menor que o informado pelo usuário


	return lista_de_dicionarios5



# caso o código bugue, executar essa função aí pode resolver
@app.post("/books6/rollback")
def rollback_executar_se_der_erro500(sim_ou_nao : str): ## função para crawlear, tendo a categoria e seu link como parâmetros (serão especificados depois)
        
    # tratamento de erro pro caso de o usuário digitar uma categoria não catalogada
    if f'{sim_ou_nao}' not in ["sim","Sim","s","S","rollback","Rollback"]:
        raise HTTPException(
            status_code=404,
            detail={'Se quiser mesmo fazer o rollback, digite alguma dessas opções':' "sim","Sim","s","S","rollback","Rollback"'},
            headers={"Erro": "Rollback não executado"},
        )
    else:
        #se o usuário pediu pra fazer o rollback:
        cursor2.execute("ROLLBACK")
        con2.commit()
        return "rollback feito"