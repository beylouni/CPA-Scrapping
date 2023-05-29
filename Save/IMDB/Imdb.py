from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
import requests
import pandas as pd

import re


class Imdb:

    Menu_button = (By.XPATH, "//span[@class='ipc-responsive-button__text']")
    Select_250 = (By.CSS_SELECTOR, "a[href='/chart/top/?ref_=nv_mv_250']")
    Table_body = (By.XPATH, "//tbody[@class='lister-list']")
    Table_row = (By.TAG_NAME, 'tr')
    Poster_url = (By.XPATH, ".//td[@class='posterColumn']/a")
    Poster_image = (By.XPATH, ".//td[@class='posterColumn']/a/img")
    Title = (By.XPATH, ".//td[@class='titleColumn']/a")
    Year = (By.XPATH, ".//td[@class='titleColumn']/span")
    Directors = (By.XPATH, ".//td[@class='titleColumn']/a")
    Rating = (By.XPATH, './/td[@class="ratingColumn imdbRating"]/strong')

    def __init__(self, driver):
        self.df = pd.DataFrame(
            columns=['Title', 'Year', 'Directors', 'Rating', 'Url', 'Image'])
        self.driver = driver

    def click_menu_button(self):
        """ Clica no botao Menu """
        self.driver.find_element(*Imdb.Menu_button).click()

    def click_top_250(self):
        """ Seleciona a opção top 250 no dropdown """
        self.driver.find_element(*Imdb.Select_250).click()

    def get_rows(self):
        """ Acessa a tabela e retorna as linhas """
        body = self.driver.find_element(*Imdb.Table_body)
        rows = body.find_elements(*Imdb.Table_row)
        return rows

    def get_poster_url(self, row):
        return row.find_element(*Imdb.Poster_url).get_attribute('href')

    def get_poster_image(self, row):
        return row.find_element(*Imdb.Poster_image).get_attribute('src')

    def get_title(self, row):
        return row.find_element(*Imdb.Title).text

    def get_year(self, row):
        return row.find_element(*Imdb.Year).text

    def get_directors(self, row):
        return row.find_element(*Imdb.Directors).get_attribute('title')

    def get_rating(self, row):
        return row.find_element(*Imdb.Rating).text

    def download_poster(self, url, title: str):
        """ Executa request para a url da imagem e faz o download """
        image_content = requests.get(url).content

        # Substitui caracters não válidos para nomes de arquivos
        title = re.sub(r'[^a-zA-Z0-9\u00C0-\u00FF]', ' ', title)
        with open(f'IMDB/Images/{title}.jpg', 'wb') as f:
            f.write(image_content)
