from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService


class BaseClass:

    choice = None

    @classmethod
    def browseSession(cls, url):

        cls.driver = webdriver.Chrome(ChromeDriverManager().install())
        cls.driver.get(url)
        cls.driver.implicitly_wait(10)
        cls.driver.maximize_window()

        return cls.driver

    @classmethod
    def display_menu(cls):
        print(f""" 
        =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

        Bem vindo Prof Lucas! Por favor selecione uma opção:

        Opção 1: Crawler para navegação na páginas dos países.
        Opção 2: Crawler para monitoramento da página dos países.
        Opção 3: Scraping do IMBD.
        Opção 4: Sair.
        
        =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

        """)

    @classmethod
    def ask_choice(cls):
        choice = input("Digite sua escolha (1, 2, 3, 4): ")
        BaseClass.choice = choice
