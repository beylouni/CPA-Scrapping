import pandas as pd
import re
import requests
import datetime


class Countries:

    elements = ['places_national_flag__row',
                'places_area__row',
                'places_population__row',
                'places_iso__row',
                'places_country__row',
                'places_capital__row',
                'places_continent__row',
                'places_tld__row',
                'places_currency_code__row',
                'places_currency_name__row',
                'places_phone__row',
                'places_postal_code_format__row',
                'places_postal_code_regex__row',
                'places_languages__row',
                'places_neighbours__row'
                ]

    def __init__(self):
        self.__soup = None

    @property
    def soup(self):
        return self.__soup
    
    @soup.setter
    def soup(self, new_soup):
         self.__soup = new_soup

    def save_html(self, html, country_name):
        print('Saving HTML...\n')
        letters_only = re.sub(r"[^a-zA-Z]+", "", country_name)
        with open(f'Countries/HTML/{letters_only}.html', 'w') as f:
            f.write(str(html))

    def find_name(self, url):
        """ Seleciona o nome do pais dentor da URL fornecida """
        match = re.findall(r"/([A-Za-z\s-]+)-\d+$", url)
        letters_only = re.sub(r"[^a-zA-Z]+", "", match[0])
        return letters_only

    def get_sitemap(self):
        sitemap_html = self.download(
            'http://127.0.0.1:8000/places/default/sitemap.xml')
        pages = re.findall('<loc>(.*?)</loc>', sitemap_html)
        return pages

    def download(self, url, user_agent='wswp', num_retries=2, proxies=None):
        """ Download a given URL and return the page content
            args:
                url (str): URL
            kwargs:
                user_agent (str): user agent (default: wswp)
                proxies (dict): proxy dict w/ keys 'http' and 'https', values
                                are strs (i.e. 'http(s)://IP') (default: None)
                num_retries (int): # of retries if a 5xx error is seen (default: 2)
        """
        print('Downloading:', url)
        headers = {'User-Agent': user_agent}
        try:
            resp = requests.get(url, headers=headers, proxies=proxies)
            html = resp.text
            if resp.status_code >= 400:
                print('Download error:', resp.text)
                html = None
                if num_retries and 500 <= resp.status_code < 600:
                    # recursively retry 5xx HTTP errors
                    return self.download(url, num_retries - 1)
        except requests.exceptions.RequestException as e:
            print('Download error:', e)
            html = None
        return html

    def getTimeStamp(self):
        """ Pega a data e horário atual e formata """
        timestamp = datetime.datetime.now().timestamp()
        formatted_time = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
        return formatted_time

    def extractData(self):
        """ Extrai os dados do HTML do pais atual.
            Selecionamos pela classe e o .text retorna a string 'XXXX: YYYYY', 
            então aplicamos o  split e obtemos um vetor aonde a primeira posição corresponde
            ao nome da coluna e a segunda posição corresponde ao valor. Ex: ['Country', 'Brazil'].
            No caso do Country Flag, pegamos o link da imagem da bandeira.
        """
        print('Extracting Data...')
        return dict(map(lambda x:
                        (self.soup.select_one(f'#{x}').text).split(":", maxsplit=1) if x != 'places_national_flag__row'
                        else ['Country Flag', self.soup.select_one('img')['src']], Countries.elements))

    def update_csv(self, dici, idx):
        """ Atualiza o CSV Atual recendo como paramentro
            a nova linha a ser inserida em forma de dicionario e o indice da linha correspondente a ser alterada no csv atual.

            Parametros: 
                - dici: {'Country': 'Brazil', 'Capital': 'Brasilia, ...}
                - idx: (int)
        """
        print('Updating CSV...')
        df = pd.read_csv('Countries/data.csv', sep=',')
        df.loc[idx] = dici

        df.to_csv('Countries/data.csv', sep=',', index=False)