from Countries.CountriesClass import Countries
from bs4 import BeautifulSoup
import pandas as pd


class CountriesWRKF:

    def run(self):

        countries_class = Countries()
        sitemap_list = countries_class.get_sitemap()

        dici_list = []
        for country_url in sitemap_list:

            html = countries_class.download(country_url)
            countries_class.soup = BeautifulSoup(html, 'html5lib')

            dici = countries_class.extractData()
            time_stamp = countries_class.getTimeStamp()
            dici.update({'Time Stamp': time_stamp})
            dici_list.append(dici)
            dici['Country'] = dici['Country'].strip()

            countries_class.save_html(html, dici['Country'])

        df = pd.DataFrame(dici_list)
        print('Saved new CSV')
        df.to_csv('Countries/data.csv', index=False)
        print('All Done')

    def crawler(self):

        countries_class = Countries()
        new_sitemap_list = countries_class.get_sitemap()
        choice = None

        while True:
            for i, new_country_url in enumerate(new_sitemap_list):

                new_html = countries_class.download(new_country_url)
                new_html = BeautifulSoup(new_html, 'html5lib')
                name_country = countries_class.find_name(new_country_url)
                try:
                    with open(f'Countries/HTML/{name_country}.html', 'r') as f:
                        current_html = BeautifulSoup(f.read(), 'html5lib')
                except:
                    print(f'File {name_country}.html Not Found')
                    continue

                if new_html != current_html:
                    print('Changes detected...\n')
                    countries_class.soup = new_html
                    dici = countries_class.extractData()
                    time_stamp = countries_class.getTimeStamp()
                    dici.update({'Time Stamp': time_stamp})

                    countries_class.update_csv(dici=dici, idx=i)
                    countries_class.save_html(
                        html=new_html, country_name=dici['Country'])

                else:
                    print('No changes were detected\n')

            print('Foram verificadas todas as informções dos paises')
            choice = input('Gostaria de verificar novamente y/n:').upper()
            if choice == "N":
                break
