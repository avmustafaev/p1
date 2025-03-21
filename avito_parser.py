from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

class AvitoParser:
    def __init__(self):
        self.driver = self._setup_driver()

    def _setup_driver(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--blink-settings=imagesEnabled=false")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-software-rasterizer")

        prefs = {
            "profile.managed_default_content_settings.images": 2,
            "profile.managed_default_content_settings.javascript": 2,
        }
        chrome_options.add_experimental_option("prefs", prefs)

        return webdriver.Chrome(options=chrome_options)

    def _extract_param(self, params_soup, param_name):
        for li in params_soup.find_all('li', class_='params-paramsList__item-_2Y2O'):
            span = li.find('span', class_='styles-module-noAccent-l9CMS')
            if span and param_name in span.text:
                value = span.next_sibling.strip()
                return value
        return "Не указано"

    def parse(self, url):
        self.driver.get(url)

        wait = WebDriverWait(self.driver, 1)
        price_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "span[itemprop='price']")))

        page_source = self.driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')

        price_span = soup.find('span', {'itemprop': 'price'})
        price_value = price_span.get('content', 'Не указано') if price_span else 'Не указано'

        params_block = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-marker='item-view/item-params']")))
        params_html = params_block.get_attribute('innerHTML')
        params_soup = BeautifulSoup(params_html, 'html.parser')

        rooms = self._extract_param(params_soup, "Количество комнат")
        total_area = self._extract_param(params_soup, "Общая площадь")
        floor = self._extract_param(params_soup, "Этаж")

        total_area = total_area.replace("\u00A0м\u00B2", "").replace(" м\u00B2", "")
        floor = floor.replace(" из ", "/")

        address_element = self.driver.find_element(By.CSS_SELECTOR, "span.style-item-address__string-wt61A")
        full_address = address_element.text.strip()

        print(f"📍 {full_address}")
        print(f"💵 {price_value}₽")
        print('')
        print(f"🚪 {rooms}комн.")
        print(f"📐 {total_area}м²")
        print(f"🪜 {floor}")

    def close(self):
        self.driver.quit()

if __name__ == "__main__":
    url = 'https://www.avito.ru/ekaterinburg/kvartiry/1-k._kvartira_406_m_69_et._4574477371?context=H4sIAAAAAAAA_wEmANn_YToxOntzOjE6IngiO3M6MTY6Ik9Ra1c5RzE3TUY5c0R2NW8iO32sRl6AJgAAAA'
    parser = AvitoParser()
    parser.parse(url)
    parser.close()