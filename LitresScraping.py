import time
import requests
from bs4 import BeautifulSoup
import json

ENDPOINT_URL = "https://www.litres.ru/popular/"

class LitresScrapper:
    def __init__(self, start_url):
        self.start_url = start_url
        self.info_about_films = []

    def get_html_string(self, url,):
        try:
            response = requests.get(url)
            response.raise_for_status()
        except Exception as e:
            time.sleep(1)
            print(e)
            return None
        return response.text

    @staticmethod
    def get_dom(html_string):
        return BeautifulSoup(html_string, "html.parser")

    def run(self):
        self.paginate(self.start_url)
        for page_number in range(2, 5):
            "/?page ="
            url = self.start_url + "?keywords=page&page=" + str(page_number)
            print(url)
            self.paginate(url)

    def get_info_from_element(self, element):
        info = {}
        info['name'] = element.find(
            attrs={
                "class": "ArtInfo_title__h_5Ay"
            }
        ).text
        print("name]",info['name'])
        info['avtor'] = element.find(
            attrs={
                "ArtInfo_author__0W3GJ"
            }
        ).text
        try:
            info['status'] = element.find(
                attrs={
                    "MarketLabel_label__eEoDr MarketLabel_label__hit__HkvRH"
                }
            ).text
            print("status", info['status'])

            info['rating_stars'] = element.find(
                attrs={
                    "ArtRating_rating__ntve8"
                }
            ).text
            print("rating_stars", info['rating_stars'])
            info['rating_votes'] = element.find(
                attrs={
                    "ArtRating_votes__MIJS1"
                }
            ).text
            info['rating_votes'] = float(info['rating_votes'])
            print("rating_votes", info['rating_votes'])

            info['price'] = element.find(
                attrs={
                    "ArtPriceFooter_ArtPriceFooterPrices__final__7AMjB"
                }
            ).text
            info['price'] = info['price'].replace("\xa0₽","")
            info['price'] = float(info['price'])
            print("price", info['price'])
        except AttributeError as e:
            print(e)
        except ValueError as e:
            print(e)

        print()
        return info

    def parse_page(self, response):
        pass

    def save_info_about_films(self, info):
        with open("info_book.json", "w") as f:
            json.dump(json.dumps(info), f)
        pass

    def paginate(self, url):
        html_string = self.get_html_string(url)
        if html_string is None:
            print("There was an error")
            return

        soup = LitresScrapper.get_dom(html_string)
        film_elements = soup.find_all(
            attrs={
                "class": "ArtsGrid_artWrapper__LXa0O"
            }
        )
        for element in film_elements:
            info = self.get_info_from_element(element)
            self.info_about_films.append(info)
            print("info",info)
        print()

if __name__ == "__main__":
    scraper = LitresScrapper(ENDPOINT_URL)
    scraper.run()
    #scraper.save_info_about_films()