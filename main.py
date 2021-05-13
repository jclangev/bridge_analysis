#!/usr/bin/env python3
"""
Module Docstring
"""

__author__ = "Joost Langeveld"
__version__ = "0.1.0"
__license__ = "MIT"

import os

from pprint import pprint

from scrape_stepbridge import get_board_result_dicts, get_board_chair_dict, \
    get_board_double_dummy_url, get_points_other_players, sign_optimal_points
from scrape_double_dummy import get_dds_analysis_dict, get_optimal_points
from util import get_browser, get_soup, convert_dutch_percentage_string_to_float, calculate_mp_score

DEBUG = False


# stepbridge_overview_url = 'https://portal.stepbridge.nl/tournament/events/index/users/74285'
# df_all_tournament_overview = get_stepbridge_tournament_overview_dataframe(stepbridge_overview_url)
# stepbridge_personal_tournament_url = df_all_tournament_overview[TOURNAMENT_URL_KEY][0]

stepbridge_personal_tournament_url = 'https://results.stepbridge.nl/tournament/events/show/38602/JoostL'
my_name = os.path.basename(stepbridge_personal_tournament_url)
# print('step_url:', stepbridge_personal_tournament_url)
print('my name:', my_name)

if DEBUG: print('DEBUG:', 'scraping boards data for single tournament...')
normal_browser = get_browser()
soup = get_soup(browser=normal_browser, url=stepbridge_personal_tournament_url)
board_tags = soup.find_all('table', class_='board')
i = 0  # error!
# i = 16
a_board_tag = board_tags[i]

row_dict = {}

double_dummy_url = get_board_double_dummy_url(a_board_tag)
dds_analysis_dict = get_dds_analysis_dict(double_dummy_url)
row_dict = row_dict | dds_analysis_dict
if DEBUG: pprint(dds_analysis_dict)

translation_dict_wind_richting = {'N': 'north', 'O': 'east', 'Z': 'south', 'W': 'west'}
players_dict = {translation_dict_wind_richting.get(wind_richting): player
                for player, wind_richting in get_board_chair_dict(a_board_tag).items()}
if DEBUG: print('players_dict:', players_dict)
row_dict['players'] = players_dict

our_result_dict_raw = get_board_result_dicts(a_board_tag, 'fieldrowselected')[0]
if DEBUG: print('our_result_dict_raw:', our_result_dict_raw)
our_result_dict_chosen_keys_dict = {
    'resultaat': 'result',
    'punten': 'our_points',
    'score': 'our_score'
}
our_result_dict = {new_key: our_result_dict_raw.get(old_key)
                   for old_key, new_key in our_result_dict_chosen_keys_dict.items()}
row_dict = row_dict | our_result_dict
row_dict['our_points'] = int(row_dict.get('our_points'))
row_dict['all_other_points'] = get_points_other_players(a_board_tag)
row_dict['optimal_points'] = sign_optimal_points(a_board_tag, my_name) * get_optimal_points(dds_analysis_dict)

row_dict['our_score'] = convert_dutch_percentage_string_to_float(row_dict.get('our_score'))
row_dict['optimal_score'] = calculate_mp_score(row_dict.get('all_other_points') + [row_dict.get('optimal_points')],
                                               row_dict.get('optimal_points'))
row_dict['optimal_score_gain'] = max(0.0, row_dict.get('optimal_points') - row_dict.get('our_score'))

print()
pprint(row_dict, sort_dicts=False, compact=True, width=150)

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
