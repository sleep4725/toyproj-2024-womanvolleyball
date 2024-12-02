from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.webdriver import WebDriver

class EngineOfSelenium:

    @staticmethod
    def get_selenium_engine()-> WebDriver:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service)
        return driver