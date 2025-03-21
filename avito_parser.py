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
        chrome_options.add_argument("--disable-setuid-sandbox")
        chrome_options.add_argument("--disable-background-networking")
        chrome_options.add_argument("--disable-background-timer-throttling")
        chrome_options.add_argument("--disable-backgrounding-occluded-windows")
        chrome_options.add_argument("--disable-breakpad")
        chrome_options.add_argument("--disable-client-side-phishing-detection")
        chrome_options.add_argument("--disable-component-update")
        chrome_options.add_argument("--disable-default-apps")
        chrome_options.add_argument("--disable-domain-reliability")
        chrome_options.add_argument("--disable-features=AudioServiceOutOfProcess")
        chrome_options.add_argument("--disable-hang-monitor")
        chrome_options.add_argument("--disable-ipc-flooding-protection")
        chrome_options.add_argument("--disable-popup-blocking")
        chrome_options.add_argument("--disable-prompt-on-repost")
        chrome_options.add_argument("--disable-renderer-backgrounding")
        chrome_options.add_argument("--disable-sync")
        chrome_options.add_argument("--force-color-profile=srgb")
        chrome_options.add_argument("--metrics-recording-only")
        chrome_options.add_argument("--no-first-run")
        chrome_options.add_argument("--safebrowsing-disable-auto-update")
        chrome_options.add_argument("--enable-automation")
        chrome_options.add_argument("--password-store=basic")
        chrome_options.add_argument("--use-mock-keychain")

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
    url0 = 'https://www.avito.ru/ekaterinburg/kvartiry/1-k._kvartira_406_m_69_et._4574477371?context=H4sIAAAAAAAA_wEmANn_YToxOntzOjE6IngiO3M6MTY6Ik9Ra1c5RzE3TUY5c0R2NW8iO32sRl6AJgAAAA'
    url1 = 'https://www.avito.ru/ekaterinburg/kvartiry/kvartira-studiya_333_m_2232_et._4655353841?context=H4sIAAAAAAAA_wFOALH_YToyOntzOjM6InNyYyI7czo4OiJmZWF0dXJlZCI7czoxOiJ4IjtzOjMxOiJqenR6ZTFxOTRrazF6bDFzdmhrbnEwdmJ2MWF2eXI2Ijt9PAzBz04AAAA'
    url2 = 'https://www.avito.ru/ekaterinburg/kvartiry/2-k._kvartira_416_m_210_et._4733833349?context=H4sIAAAAAAAA_wEmANn_YToxOntzOjE6IngiO3M6MTY6IldxVDhpbG12M1FZTXUwU0ciO33KGfC6JgAAAA'
    parser = AvitoParser()
    parser.parse(url0)
    parser.parse(url1)
    parser.parse(url2)
    parser.close()