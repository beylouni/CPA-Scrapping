import pandas as pd
import time
from IMDB.Imdb import Imdb
from BaseClass import BaseClass
from tqdm import tqdm


class ImdbWRKF:

    def run(self):
        print('Opening Browser...')
        driver = BaseClass.browseSession('https://www.imdb.com/?ref_=nv_home')
        imdb = Imdb(driver=driver)
        df = imdb.df

        imdb.click_menu_button()
        time.sleep(2)
        imdb.click_top_250()
        rows = imdb.get_rows()
        time.sleep(2)

        print("Getting data from each Movie")
        for row in tqdm(rows, desc="IMDB"):
            poster_url = imdb.get_poster_url(row)
            poster_image = imdb.get_poster_image(row)
            title = imdb.get_title(row)
            year = imdb.get_year(row)
            directors = imdb.get_directors(row)
            rating = imdb.get_rating(row)
            imdb.download_poster(poster_image, title)

            df_data = pd.DataFrame([{'Title': title, 'Year': year, 'Directors': directors,
                                   'Rating': rating, 'Url': poster_url, 'Image': poster_image}])
            df = pd.concat([df, df_data], ignore_index=True)

        print('Exporting to json')
        df.to_json('IMDB/imbd.json', force_ascii=False,
                   orient='records', indent=4, lines=True)
        driver.quit()
        print("All Done...")
