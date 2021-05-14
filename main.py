#!/usr/bin/env python3
"""
Module Docstring
"""

__author__ = "Joost Langeveld"
__version__ = "0.1.0"
__license__ = "MIT"

import os
import pandas as pd

from scrape_stepbridge import scrape_tournament_dataframe

SCRAPED_DIRECTORY = 'scraped'


def determine_scraped_filename(tournament_id: str, player_name: str) -> str:
    return f'scraped-stepbridge-tournament_{tournament_id}_{player_name}.pkl'


# stepbridge_overview_url = 'https://portal.stepbridge.nl/tournament/events/index/users/74285'
# df_all_tournament_overview = get_stepbridge_tournament_overview_dataframe(stepbridge_overview_url)
# stepbridge_personal_tournament_url = df_all_tournament_overview[TOURNAMENT_URL_KEY][0]

# a_stepbridge_personal_tournament_url = 'https://results.stepbridge.nl/tournament/events/show/38602/JoostL'
# my_name = os.path.basename(a_stepbridge_personal_tournament_url)
# a_tournament_id = os.path.basename(os.path.split(a_stepbridge_personal_tournament_url)[0])
# print(f'[INFO] scraping boards data for {my_name} in tournament {a_tournament_id}.' +
#       f' url={a_stepbridge_personal_tournament_url}')
# df_tournament = scrape_tournament_dataframe(a_stepbridge_personal_tournament_url, my_name)
# tournament_file_name = determine_scraped_filename(tournament_id=a_tournament_id, player_name=my_name)
# tournament_file_path = os.path.join(SCRAPED_DIRECTORY, tournament_file_name)
# df_tournament.to_pickle(tournament_file_path)

tournament_file_name = r'scraped-stepbridge-tournament_38602_JoostL.pkl'
df_tournament = pd.read_pickle(os.path.join(SCRAPED_DIRECTORY, tournament_file_name))

print()
select_columns = ['contract', 'result', 'contractsNS', 'contractsEW', 'ddtricks']
# select_columns = ['contract', 'result', 'lead', 'best_leads']
print(df_tournament[select_columns])

# TODO: extract bidding
# TODO: extract all double dummy contracts
