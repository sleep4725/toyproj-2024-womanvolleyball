import requests
from typing import Optional,List, Dict
from bs4 import BeautifulSoup
import bs4
from teams.common.Position import Position
from teams.common.UrlRequInfo import UrlRequInfo
##
# Aipeppers
##
class CllctPlayerInfo:

    @staticmethod
    def get_player_ddetail_info(info: bs4.element.Tag)-> Optional[Dict]:
        '''
        :param info:
        :return:
        '''
        template :Dict= {
            '생년월일': {'Y': None, 'M': None, 'D': None},
            '출신학교': {'P': None, 'M': None, 'H': None},
            '신장': None
        }
        span_tag :Optional[bs4.element.Tag]= info.select_one('div.player_detail_info > span')
        if not span_tag: return None
        result = [str(part).strip() for part in str(span_tag.text).lstrip('\n').rstrip('\r\n ').split('\r\n')]
        for r in result:
            k, v = str(r).split(":")
            _k = str(k).strip()
            _v = str(v).strip()

            if _k == '생년월일' and _v:
                b_list = [int(str(b).lstrip('0')) for b in _v.split('.')]
                template[_k]['Y'], template[_k]['M'],template[_k]['D'] = b_list
            elif _k == '출신학교' and _v:
                school :List[str]= [str(s).strip() for s in _v.split('/')]
                for s in school:
                    if s[-1] == '초': template[_k]['P'] = s
                    elif s[-1] == '중': template[_k]['M'] = s
                    elif s[-1] == '고': template[_k]['H'] = s
            elif _k == '신장' and _v:
                template[_k] = int(str(_v).replace('cm', ''))

        return template

    @staticmethod
    def get_player_img(info: bs4.element.Tag)-> Optional[str]:
        ''' 선수 이미지 url을 리턴

        :param info:
        :return:
        '''
        img_tag :Optional[bs4.element.Tag]= info.select_one('div.player_detail_photo > img')
        if not img_tag: return None

        src :Optional[str]= img_tag.attrs['src']
        if src: return src
        else: return None

    @staticmethod
    def get_player_position(info: bs4.element.Tag)-> Optional[str]:
        ''' 선수 position 을 리턴

        :param info:
        :return:
        '''
        detail_info_tag :Optional[bs4.element.Tag]= info.select_one('div.player_detail_info')
        if not detail_info_tag: return None
        h3_tag :Optional[bs4.element.Tag]= detail_info_tag.select_one('h3')
        if not h3_tag: return None
        position :Optional[str]= str(h3_tag.string).strip(' ')
        if position:
            if position == Position.LIBERO: return "Libero" ## 리베로
            elif position == Position.SETTER: return "Setter" ## 세터
            elif position == Position.MIDDLE_BLOCKER: return "Middle-Blocker" ## 미들블러커
            elif position == Position.OPPOSITE: return "Opposite" ## 아포짓
            elif position == Position.OUTSIDE_HITTER: return "Outside-Hitter"
            else: return "-"
        else: return None

    @staticmethod
    def get_player_number(info: bs4.element.Tag)-> Optional[str]:
        '''

        :param info:
        :return:
        '''
        detail_info_tag: Optional[bs4.element.Tag] = info.select_one('div.player_detail_info')
        if not detail_info_tag: return None
        h2_tag :Optional[bs4.element.Tag]= detail_info_tag.select_one('h2')
        if not h2_tag: return None
        number :Optional[str]= str(h2_tag.string).strip(' ').replace("No.", "")
        if number: return number
        else: return None

    @staticmethod
    def get_player_name(info: bs4.element.Tag)-> Optional[List[str]]:
        '''

        :param info:
        :return:
        '''
        detail_info_tag: Optional[bs4.element.Tag] = info.select_one('div.player_detail_info')
        if not detail_info_tag: return None
        p_tag :Optional[bs4.element.Tag]= detail_info_tag.select_one('p')
        if not p_tag: return None
        return [part.strip() for part in str(p_tag.text).lstrip('\r\n ').split('\r\n')]

    @staticmethod
    def get_player_detail_information(url):
        '''

        :param url:
        :return:
        '''
        player_info = {
            'img': 'http://www.aipeppers.kr{player_img_url}',
            'position': None,
            'number': None,
            'english_name': None,
            'korea_name': None,
            'birthday': None,
            'school': None,
            'height': None
        }
        response = requests.get(url, headers= UrlRequInfo.headers)
        if response.status_code != 200: return None
        bs_obj = BeautifulSoup(response.text, "html.parser")
        player_detail :Optional[bs4.element.Tag]= bs_obj.select_one('div.player_detail')
        if not player_detail: return None

        src :Optional[str]= CllctPlayerInfo.get_player_img(info= player_detail)
        position :Optional[str]= CllctPlayerInfo.get_player_position(info= player_detail)
        number :Optional[str]= CllctPlayerInfo.get_player_number(info= player_detail)
        name :List[str]= CllctPlayerInfo.get_player_name(info= player_detail)
        dd_info :Optional[Dict]= CllctPlayerInfo.get_player_ddetail_info(info= player_detail)

        if src: player_info['img'] = player_info['img'].format(player_img_url= src)
        if position: player_info['position'] = position
        if number: player_info['number'] = number
        if name and (len(name) == 2):
            player_info['english_name'] = name[0]
            player_info['korea_name'] = name[1]
        if dd_info:
            if dd_info['생년월일']: player_info['birthday'] = dd_info['생년월일']
            if dd_info['출신학교']: player_info['school'] = dd_info['출신학교']
            if dd_info['신장']: player_info['height'] = dd_info['신장']

        return player_info