from multiprocessing import Pool
import sys
from pathlib import Path
from typing import Optional, List
PROJ_ROOT_PATH :str= str(Path(__file__))
sys.path.append(PROJ_ROOT_PATH)

from teams.aipeppers.Aipeppers import Aipeppers
from teams.aipeppers.CllctAipeppers import CllctPlayerInfo

if __name__ == "__main__":
    aipeppers = Aipeppers()
    players_url :Optional[List[str]]= aipeppers.get_players_url_information()
    if players_url:
        pool = Pool(5)
        async_results = []
        for u in players_url:
            async_result = pool.apply_async(CllctPlayerInfo.get_player_detail_information, args=(u,))
            async_results.append(async_result)

        # 비동기 결과 받기
        final_result = [result.get() for result in async_results]

        for i, r in enumerate(final_result):
            print(f"{i+1}: {r}")

        pool.close()
        pool.join()