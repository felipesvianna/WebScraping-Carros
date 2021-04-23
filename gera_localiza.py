from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as soup

def get_localiza_cars():
    base_url = 'https://seminovos.localiza.com/Paginas/resultado-busca.aspx?&yr=2013_2018&pc=25000_500000'

    #Start driver
    driver = webdriver.Firefox()
    driver.implicitly_wait(30)
    driver.get(base_url)

    page_number = 0
    containers = [] #Array to store the cars data
    resume_mining = True

    #Loop to get each car in the current page
    while resume_mining == True:
        print('Page [%d]\r'%page_number, end="")

        page_soup = soup(driver.page_source, "html.parser")
        containers += page_soup.findAll("div", {"class":"col-xs-12 col-md-6 col-lg-12"})

        page_number += 1

        #Click on next page button
        next_page_button = driver.find_element_by_id('ctl00_ctl42_g_f221d036_75d3_4ee2_893d_0d7b40180245_ProximaPaginaSuperior')

        if next_page_button: #exists
            next_page_button.click()
        else:
            resume_mining = False

    driver.quit()

    #Write data in file
    filename = "carros_localiza.csv"
    f = open(filename, "w")

    columns = "empresa_locacao, modelo_carro, quilometragem, ano, preco\n"
    f.write(columns)

    for container in containers:
        a = container.find("span", {"class":"ano"})
        q = container.find("span", {"class":"km"})
        p = container.find("span", {"class":"car-price"})

        modelo = container.img["alt"]
        ano = a.text
        quilometragem = q.text
        preco = p.text

        f.write("Localiza" + "," + modelo + "," + quilometragem + "," + ano + "," + preco + "\n")

    f.close()

#End

get_localiza_cars()
