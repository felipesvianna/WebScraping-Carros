from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

def generates_page_soup(my_url):
    uClient = uReq(my_url)
    page_html = uClient.read()
    uClient.close()
    return soup(page_html, "html.parser")

def get_unidas_cars():
    base_url = 'https://seminovos.unidas.com.br/veiculos/limit:25/page:'
    page_number = 1
    containers = [] #Array to store the cars data

    #Get the first page
    current_url = base_url + str(page_number)
    page_soup = generates_page_soup(current_url)

    #Loop to get each car in the current page
    while page_number <= 101:
        print('Page [%d/101]\r'%page_number, end="")
        containers += page_soup.findAll("div", {"class":"row no-gutters item-carro item-carro-list row-eq-height"})

        #Defines the next page link
        page_number += 1
        current_url = base_url + str(page_number)
        page_soup = generates_page_soup(current_url) #Get the page

    #Write data in file
    filename = "carros_unidas.csv"
    f = open(filename, "w")

    columns = "empresa_locacao, modelo_carro, quilometragem, ano, preco\n"
    f.write(columns)

    for container in containers:
        modelo = container.h3["title"]

        p = container.findAll("div", {"class":"carro-preco text-primary"})
        preco = p[0].text

        quilometragem_ano_container = container.findAll("li", {"class":"list-inline-item"})
        ano = quilometragem_ano_container[0].text.strip()
        quilometragem = quilometragem_ano_container[1].text.strip()[:-3]

        f.write("Unidas" + "," + modelo + "," + quilometragem + "," + ano + "," + preco + "\n")

    f.close()
#End

get_unidas_cars()
