from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

def generates_page_soup(my_url):
    uClient = uReq(my_url)
    page_html = uClient.read()
    uClient.close()
    return soup(page_html, "html.parser")

def get_movida_cars():
    base_url = 'https://busca.movidaseminovos.com.br/filtros/class/usado?sort=11&page='

    page_number = 1
    containers = [] #Array to store the cars data

    #Get the first page
    current_url = base_url + str(page_number)
    page_soup = generates_page_soup(current_url)

    #Loop to get each car in the current page
    while len(page_soup.findAll("div", {"class":"nm-not-found-message"})) == 0:
        print('Page [%d]\r'%page_number, end="")
        containers += page_soup.findAll("li", {"class":"nm-product-item"})

        #Defines the next page link
        page_number += 1
        current_url = base_url + str(page_number)
        page_soup = generates_page_soup(current_url) #Get the page

    #Write data in file
    filename = "carros_movida.csv"
    f = open(filename, "w")

    columns = "empresa_locacao, modelo_carro, quilometragem, ano, preco\n"
    f.write(columns)

    for container in containers:
        modelo = container.a["title"]

        quilometragem_ano_container = container.findAll("ul", {"class":"nm-group-details"})
        p = container.findAll("div", {"class":"nm-price-container"})
        q = quilometragem_ano_container[0].findAll("li", {"class":"nm-fuel"})
        a = quilometragem_ano_container[0].findAll("li", {"class":"nm-calendar"})

        quilometragem = q[0].span.text.strip()
        ano = a[0].span.text.strip()
        preco = p[0].text.strip()

        f.write("Movida" + "," + modelo + "," + quilometragem + "," + ano + "," + preco + "\n")

    f.close()
#End

get_movida_cars()
