import requests
from bs4 import BeautifulSoup
from lxml import html
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

from abc import ABC, abstractmethod

class BaseLoader(ABC):
    @abstractmethod
    def load(self, url):
        pass

    @abstractmethod
    def process(self, url) -> html:
        pass



class HTMLLoader(BaseLoader):

    def load(self, url):
        response = requests.get(url)
        return response.text

    def process(self, url):
        data = self.load(url)
        soup = BeautifulSoup(data, 'html.parser')
        return html.fromstring(str(soup))

class SeleniumLoader(BaseLoader):

    def __init__(self):
        self.driver_path = "C:\\Users\\User\\Downloads\\chromedriver-win64\\chromedriver-win64\\chromedriver.exe"
        service = Service(executable_path=self.driver_path)

        options = Options()
        options.add_argument('--headless')  # Run Chrome in headless mode
        options.add_argument('--disable-gpu')  # Disable GPU acceleration (useful on Windows)
        options.add_argument('--no-sandbox')  # Bypass OS security model (useful in certain environments)
        options.add_argument('--disable-dev-shm-usage')  # Overcome limited resource problems in Docker

        self.driver = webdriver.Chrome(service=service, options=options)

    def load(self, url):
        self.driver.get(url)
        self.driver.implicitly_wait(2)
        return self.driver.page_source

    def process(self, url):
        data = self.load(url)
        soup = BeautifulSoup(data, 'html.parser')
        return html.fromstring(str(soup))

    def quit(self):
        self.driver.quit()
