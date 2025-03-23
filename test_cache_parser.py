import os
import requests
from bs4 import BeautifulSoup
import hashlib

class AvitoParser:
    def __init__(self, cache_dir="cache"):
        self.price_value = None
        self.full_address = None
        self.rooms = None
        self.total_area = None
        self.floor = None
        self.cache_dir = cache_dir
        # Создаем директорию для кэша, если её нет
        os.makedirs(self.cache_dir, exist_ok=True)

    def _get_cache_filename(self, url):
        # Хэшируем URL для создания уникального имени файла
        url_hash = hashlib.md5(url.encode()).hexdigest()
        return os.path.join(self.cache_dir, f"{url_hash}.html")

    def _download_html(self, url):
        cache_file = self._get_cache_filename(url)

        # Если файл с кэшем существует, читаем из него
        if os.path.exists(cache_file):
            print(f'Файл {cache_file} существует')
            with open(cache_file, "r", encoding="utf-8") as file:
                return file.read()

        # Если файла нет, скачиваем HTML
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(url, headers=headers)
        print(f'Адрес новый, скачиваем файл: {cache_file}')
        if response.status_code != 200:
            raise Exception(f"Ошибка при загрузке страницы: {response.status_code}")

        # Сохраняем HTML в кэш
        with open(cache_file, "w", encoding="utf-8") as file:
            file.write(response.text)

        return response.text
    
    def _process_address(self, address):
        parts = address.split(',')
        if 'ул.' in parts[-2]:
            processed_parts = [part + '\n 📍' for part in parts[:-2]]
            processed_parts.append(f"{parts[-2]},{parts[-1]}")
        else:
            processed_parts = [part + '\n 📍' for part in parts[:-1]]
            processed_parts.append(parts[-1])
        address = ''.join(processed_parts)
        return address
    

    # Остальные методы класса остаются без изменений
    def _extract_param(self, params_soup, param_name):
        for li in params_soup.find_all('li', class_='params-paramsList__item-_2Y2O'):
            span = li.find('span', class_='styles-module-noAccent-l9CMS')
            if span and param_name in span.text:
                return span.next_sibling.strip()
        return "Не указано"

    def parse(self, url):
        # Скачиваем HTML
        html = self._download_html(url)

        # Парсим HTML
        soup = BeautifulSoup(html, 'html.parser')

        # Извлекаем цену
        price_span = soup.find('span', {'itemprop': 'price'})
        self.price_value = price_span.get('content', 'Не указано') if price_span else 'Не указано'

        if params_block := soup.find('div', {'data-marker': 'item-view/item-params'}):
            self._extracted_from_parse_20(params_block)

        # Извлекаем адрес
        address_element = soup.find('span', class_='style-item-address__string-wt61A')
        self.full_address = address_element.text.strip() if address_element else "Не указано"
        self.full_address = self._process_address(self.full_address)
        return f"⛳️ {self.full_address}\n💵 {self.price_value}₽\n🚪 {self.rooms}комн.\n📐 {self.total_area}м²\n🪜 {self.floor}\n"


    def _extracted_from_parse_20(self, params_block):
        params_soup = BeautifulSoup(params_block.decode_contents(), 'html.parser')
        self.rooms = self._extract_param(params_soup, "Количество комнат")
        self.total_area = self._extract_param(params_soup, "Общая площадь")
        self.floor = self._extract_param(params_soup, "Этаж")

        # Очищаем данные
        self.total_area = self.total_area.replace("\u00A0м\u00B2", "").replace(" м\u00B2", "")
        self.floor = self.floor.replace(" из ", "/")



if __name__ == "__main__":
    url0 = 'https://www.avito.ru/ekaterinburg/kvartiry/1-k._kvartira_406_m_69_et._4574477371?context=H4sIAAAAAAAA_wEmANn_YToxOntzOjE6IngiO3M6MTY6Ik9Ra1c5RzE3TUY5c0R2NW8iO32sRl6AJgAAAA'
    url1 = 'https://www.avito.ru/ekaterinburg/kvartiry/kvartira-studiya_57_m_1625_et._7243069890?context=H4sIAAAAAAAA_wEmANn_YToxOntzOjE6IngiO3M6MTY6InlOcXhNSHk4bHg4MkxjWlQiO33jAkacJgAAAA'
    url2 = 'https://www.avito.ru/ekaterinburg/kvartiry/svob._planirovka_50_m_44_et._5122336744?context=H4sIAAAAAAAA_wEmANn_YToxOntzOjE6IngiO3M6MTY6IlpGY3FYb0UxMkk3VUxjMFAiO31DR3s7JgAAAA'
    url3 = 'https://www.avito.ru/verhnyaya_salda/komnaty/komnata_135_m_v_1-k._45_et._1333252089?context=H4sIAAAAAAAA_wEmANn_YToxOntzOjE6IngiO3M6MTY6Imt5dWRNS29pa25CeWg0VXYiO30K98gkJgAAAA'
    url4 = 'https://www.avito.ru/verhnee_dubrovo/doma_dachi_kottedzhi/dom_1274_m_na_uchastke_76_sot._7252674869?context=H4sIAAAAAAAA_wEmANn_YToxOntzOjE6IngiO3M6MTY6Ik5od2N2Z1BHaVJhaVpVOHAiO31XgMClJgAAAA'
    url5 = 'https://www.avito.ru/dvurechensk/doma_dachi_kottedzhi/dacha_18_m_na_uchastke_10_sot._3203306502?context=H4sIAAAAAAAA_wEmANn_YToxOntzOjE6IngiO3M6MTY6IjJzRTNyWEZDQVBvYkRKdUgiO30NWGFWJgAAAA'
    url6 = 'https://www.avito.ru/ekaterinburg/doma_dachi_kottedzhi/kottedzh_200_m_na_uchastke_8_sot._3080749310?context=H4sIAAAAAAAA_wEmANn_YToxOntzOjE6IngiO3M6MTY6IlVsSnpzSWphTVd5c29tdXgiO33Z6DWlJgAAAA'
    url7 = 'https://www.avito.ru/verhnee_dubrovo/doma_dachi_kottedzhi/taunhaus_134_m_na_uchastke_2_sot._7221450986?context=H4sIAAAAAAAA_wEmANn_YToxOntzOjE6IngiO3M6MTY6IlhnajNUQ0lVZU8yeFBTRkwiO33NMB-aJgAAAA'
    url8 = 'https://www.avito.ru/verhnyaya_pyshma/zemelnye_uchastki/uchastok_6_sot._izhs_1387175700?context=H4sIAAAAAAAA_wEmANn_YToxOntzOjE6IngiO3M6MTY6ImcxMEFvZ3hrU1FWUDIxenMiO320OK3wJgAAAA'
    url9 = 'https://www.avito.ru/ekaterinburg/zemelnye_uchastki/uchastok_5_ga_snt_dnp_4611091619?context=H4sIAAAAAAAA_wEmANn_YToxOntzOjE6IngiO3M6MTY6InRxbFgwQ0R4cEl0Q0NuSmsiO303-IQAJgAAAA'
    url10 = 'https://www.avito.ru/pervouralsk/garazhi_i_mashinomesta/garazh_22_m_4837910861?context=H4sIAAAAAAAA_wEmANn_YToxOntzOjE6IngiO3M6MTY6IlZtNVUyYjdXT3hyQVdxbUciO30bKPsiJgAAAA'
    url11 = 'https://www.avito.ru/ekaterinburg/garazhi_i_mashinomesta/mashinomesto_15_m_4547294076?context=H4sIAAAAAAAA_wEmANn_YToxOntzOjE6IngiO3M6MTY6IjhrOVdjRmdwVmRoMkFtQloiO30uAaclJgAAAA'
    parser = AvitoParser()
    print(parser.parse(url0))
    print(parser.parse(url1))
    print(parser.parse(url2))
    print(parser.parse(url3))
    print(parser.parse(url4))
    print(parser.parse(url5))
    print(parser.parse(url6))
    print(parser.parse(url7))
    print(parser.parse(url8))
    print(parser.parse(url9))
    print(parser.parse(url10))
    print(parser.parse(url11))
    