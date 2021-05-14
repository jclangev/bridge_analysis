#!/usr/bin/env python3
"""
Module Docstring
"""

__author__ = "Joost Langeveld"
__version__ = "0.1.0"
__license__ = "MIT"

import os
import pandas as pd

from pprint import pprint

from scrape_stepbridge import get_stepbridge_tournament_board_tags, \
    get_scrape_row_dict_for_stepbridge_tournament


# stepbridge_overview_url = 'https://portal.stepbridge.nl/tournament/events/index/users/74285'
# df_all_tournament_overview = get_stepbridge_tournament_overview_dataframe(stepbridge_overview_url)
# stepbridge_personal_tournament_url = df_all_tournament_overview[TOURNAMENT_URL_KEY][0]

a_stepbridge_personal_tournament_url = 'https://results.stepbridge.nl/tournament/events/show/38602/JoostL'
my_name = os.path.basename(a_stepbridge_personal_tournament_url)
print(f'[INFO] scraping boards data for {my_name} in tournament {a_stepbridge_personal_tournament_url}')

a_board_tags = get_stepbridge_tournament_board_tags(a_stepbridge_personal_tournament_url)
# a_board_tags = a_board_tags[0:3]

board_row_dicts = [get_scrape_row_dict_for_stepbridge_tournament(a_board_tag, my_name)
                   for a_board_tag in a_board_tags]
df_tournament = pd.DataFrame(board_row_dicts)

print()
select_columns = ['contract', 'result', 'contractsNS', 'contractsEW', 'ddtricks']
# select_columns = ['contract', 'result', 'lead', 'best_leads']
print(df_tournament[select_columns])
# pprint(board_row_dicts, sort_dicts=False, compact=True, width=150)

# print(f'{board_id:16} '
#       + f'our points: {our_points:5}  '
#       # + f'optimal points: {optimal_points:5}  '
#       + f'board {i + 1:2}:  our score: {our_score:6.2f}  '
#       + f'optimal score: {optimal_score:6.2f}  '
#       + f'possible gain: {possible_gain:6.2f}'
#       )

# our_total_score = np.mean(our_scores)
# optimal_total_score = np.mean(optimal_scores)
# total_possible_gain = np.mean(possible_gains)
#
# print()
# print(f'our score:           {our_total_score:6.2f}')
# print(f'total possible gain: {total_possible_gain:6.2f}')
# print(f'possible max score:  {our_total_score + total_possible_gain:6.2f}')

# TODO: extract bidding
# TODO: extract all double dummy contracts

# TODO: later,
# 1 from dds analysis page
# 2 click optimal contract and get reponse dict
# 3 see lead scores vs actual leads
# --> wrong lead detection
