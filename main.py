from IMDB.ImdbWRKF import ImdbWRKF
from Countries.CountriesWRKF import CountriesWRKF
from BaseClass import BaseClass

def main():


    countries = CountriesWRKF()
    imdb = ImdbWRKF()

    while True:
        BaseClass.display_menu()
        BaseClass.ask_choice()
        
        match BaseClass.choice:
            case "1":
                countries.run()
            case "2":
                countries.crawler()
            case "3":
                imdb.run()
            case "4":
                print('May the force be with you ...')
                exit()

if __name__ == '__main__':
    main()
