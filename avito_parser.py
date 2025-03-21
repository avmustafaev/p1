import requests
from bs4 import BeautifulSoup

class AvitoParser:
    def __init__(self):
        self.price_value = None
        self.full_address = None
        self.rooms = None
        self.total_area = None
        self.floor = None

    def _extract_param(self, params_soup, param_name):
        for li in params_soup.find_all('li', class_='params-paramsList__item-_2Y2O'):
            span = li.find('span', class_='styles-module-noAccent-l9CMS')
            if span and param_name in span.text:
                return span.next_sibling.strip()
        return "Не указано"

    def parse(self, url):
        # Отправляем GET-запрос на страницу
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            raise Exception(f"Ошибка при загрузке страницы: {response.status_code}")

        # Парсим HTML
        soup = BeautifulSoup(response.text, 'html.parser')

        # Извлекаем цену
        price_span = soup.find('span', {'itemprop': 'price'})
        self.price_value = price_span.get('content', 'Не указано') if price_span else 'Не указано'

        if params_block := soup.find(
            'div', {'data-marker': 'item-view/item-params'}
        ):
            self._extracted_from_parse_20(params_block)
        # Извлекаем адрес
        address_element = soup.find('span', class_='style-item-address__string-wt61A')
        self.full_address = address_element.text.strip() if address_element else "Не указано"

    # TODO Rename this here and in `parse`
    def _extracted_from_parse_20(self, params_block):
        params_soup = BeautifulSoup(params_block.decode_contents(), 'html.parser')
        self.rooms = self._extract_param(params_soup, "Количество комнат")
        self.total_area = self._extract_param(params_soup, "Общая площадь")
        self.floor = self._extract_param(params_soup, "Этаж")

        # Очищаем данные
        self.total_area = self.total_area.replace("\u00A0м\u00B2", "").replace(" м\u00B2", "")
        self.floor = self.floor.replace(" из ", "/")


if __name__ == "__main__":
    url = 'https://www.avito.ru/ekaterinburg/kvartiry/1-k._kvartira_406_m_69_et._4574477371?context=H4sIAAAAAAAA_wEmANn_YToxOntzOjE6IngiO3M6MTY6Ik9Ra1c5RzE3TUY5c0R2NW8iO32sRl6AJgAAAA'
    parser = AvitoParser()
    parser.parse(url)
    print(f"📍 {parser.full_address}")
    print(f"💵 {parser.price_value}₽")
    print('')
    print(f"🚪 {parser.rooms}комн.")
    print(f"📐 {parser.total_area}м²")
    print(f"🪜 {parser.floor}")