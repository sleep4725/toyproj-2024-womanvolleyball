import sys
from pathlib import Path
from typing import Optional, List
PROJ_ROOT_PATH :str= str(Path(__file__).resolve().parents[2])
sys.path.append(PROJ_ROOT_PATH)
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import bs4

from teams.common.Util import CommonUtil
from engine.EngineOfSelenium import EngineOfSelenium

class Aipeppers:

    def __init__(self):
        self.team_name = self.__class__.__name__
        self.config = CommonUtil.get_config(team_name= self.team_name)
        self.chrome_driver = EngineOfSelenium.get_selenium_engine()

    def get_players_url_information(self, wait_second :int= 60)-> Optional[List[str]]:
        '''

        :return:
        '''

        try:

            self.chrome_driver.get(url=self.config['url'])
            element = WebDriverWait(self.chrome_driver, wait_second).until(
                EC.visibility_of_element_located((By.ID, "team_sub1_section2"))
            )

            html_content = element.get_attribute('outerHTML')
            bs_soup = BeautifulSoup(html_content, 'html.parser')

            # 원하는 ul 태그 선택
            ul_tag :Optional[bs4.element.Tag]= bs_soup.select_one('div#team_sub1_section2 > ul')
            if not ul_tag: return
            else:
                a_tags :Optional[List[bs4.element.Tag]]= ul_tag.select("li > div.player_thmbs > a")
                return [a.attrs['href'] for a in a_tags if a]

        except Exception as e:
            print(f"태그를 찾는데 실패했습니다. {e}")

    def __del__(self):
        self.chrome_driver.quit()