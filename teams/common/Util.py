import os
from pathlib import Path
PROJ_ROOT_PATH :str= str(Path(__file__).resolve().parents[2])
import yaml
from typing import Dict
##
# @author Teddy
# @email sleep4725@gmail.com
##
class CommonUtil:

    @classmethod
    def is_exists_file(cls, file_path: str):
        ''' 파일이 존재하지 확인하는 함수

        :param file_path:
        :return:
        '''
        response :bool= os.path.exists(file_path)
        if not response:
            raise FileNotFoundError(f"파일({file_path})이 존재하지 않습니다. ")

    @classmethod
    def get_config(cls, team_name: str)-> Dict:
        '''

        :return:
        '''
        conn_file_path :str= os.path.join(PROJ_ROOT_PATH, f'config/{team_name}/info.yaml')
        CommonUtil.is_exists_file(conn_file_path)
        with open(conn_file_path, "r", encoding="utf-8") as fr:
            conn :dict= yaml.safe_load(fr)
            return conn

    @classmethod
    def position_name(cls, pos: str):
        '''
        
        :param pos:
        :return:
        '''