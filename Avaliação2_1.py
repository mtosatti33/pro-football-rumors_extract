from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd

IS_CHROME = False

# Configurar o driver do Chrome
if IS_CHROME:
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
else:
    from selenium.webdriver.firefox.service import Service
    from webdriver_manager.firefox import GeckoDriverManager
    driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()))

'''
    Importador de Notícias profootballrumors.com 
    que trata das principais notícias do futebol americano

    Páginas estão em inglês.
'''

# URL Modelo
url_model = "https://www.profootballrumors.com/page/{}"

# Lista de URLs Gerados
urls = [url_model.format(x) for x in range(1,6)]

# Lista Mestra
list = []

# Iteração de urls
for url in urls:
    # Pega os dados do site
    driver.get(url)

    # aguarda a carga da página em modo implícito (em segundos)
    driver.implicitly_wait(2)

    # Importação e manipulação das listas
    # Notícias
    news = driver.find_elements(By.XPATH, "//h2[contains(@class, 'hdg_mainColor')]/a")

    # Links
    links = [new.get_attribute('href') for new in news]

    # Importação das Datetimes
    dates = driver.find_elements(By.XPATH, "//div[@class='post-author']/span")
    
    # Lista de notícias retornados em string (Usando Lista de Compreensão)
    news_list = [new.text for new in news]

    # Data
    date_list = [date.text.split('at')[0] for date in dates]

    # Hora
    time_list = [date.text.split('at')[1].split(' ')[1] for date in dates]

    # inclusão das listas em uma lista-mestra 'list'
    x = 0
    for item in news_list:
        list.append([date_list[x], time_list[x], item, links[x]])
        x += 1

# Fechar o navegador
driver.quit()

# Criação do DataFrame do Pandas
df = pd.DataFrame(list)

# Adiciona colunas ao DataFrame
df.columns = ['Date','Time','News','Link']

# Ele vai tentar salvar se o arquivo não estiver em aberto no Excel
try:
    df.to_excel('pro_football_rumors.xlsx',index=False)
    print("\n\nArquivo pro_football_rumors.xlsx criado")
except PermissionError:
    # Caso Contrário ele emite esse aviso 
    # quando a exceção PermissionError for chamada
    print("Não foi possível salvar. Permissão Negada")