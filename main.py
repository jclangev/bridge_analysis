#!/usr/bin/env python3
"""
Module Docstring
"""

__author__ = "Joost Langeveld"
__version__ = "0.1.0"
__license__ = "MIT"

import os
import numpy as np
import requests
import bs4

import scrape_stepbridge
import scrape_double_dummy
import util

stepbridge_personal_tournament_url = 'https://results.stepbridge.nl/tournament/events/show/38602/JoostL'
my_name = os.path.basename(stepbridge_personal_tournament_url)

print('step_url:', stepbridge_personal_tournament_url)
print('my name:', my_name)
print()

normal_browser = util.get_browser()
soup = util.get_soup(browser=normal_browser, url=stepbridge_personal_tournament_url)

board_tags = soup.find_all('table', class_='board')
i = 16
a_board_tag = board_tags[i]

# board_id = scrape_stepbridge.get_board_id(a_board_tag)
#
# other_result_dicts = scrape_stepbridge.get_board_result_dicts(a_board_tag, 'fieldrow')
# our_result_dict = scrape_stepbridge.get_board_result_dicts(a_board_tag, 'fieldrowselected')[0]
#
# other_points = [int(fieldrow_dict.get('punten')) for fieldrow_dict in other_result_dicts]
# our_points = int(our_result_dict.get('punten'))
# board_chair_dict = scrape_stepbridge.get_board_chair_dict(a_board_tag)
# flip_optimal_points = (board_chair_dict.get(my_name).upper()) in ['O', 'W']

double_dummy_url = scrape_stepbridge.get_board_double_dummy_url(a_board_tag)
print(double_dummy_url)
dds_parameter_dict = scrape_double_dummy.extract_parameter_dict_from_dds_url(double_dummy_url)
print(dds_parameter_dict)

dds_bidding_query_url = scrape_double_dummy.get_double_dummy_analysis_bidding_query_url(double_dummy_url)
print(dds_bidding_query_url)
dds_bidding_analysis_dict = scrape_double_dummy.get_double_dummy_analysis_dict_for_deal(dds_bidding_query_url)
print(dds_bidding_analysis_dict)

dds_lead_query_url = scrape_double_dummy.get_double_dummy_analysis_lead_query_url(double_dummy_url)
print(dds_lead_query_url)
dds_lead_analysis_dict = scrape_double_dummy.get_double_dummy_analysis_dict_for_deal(dds_lead_query_url)
print(dds_lead_analysis_dict)


cards = dds_lead_analysis_dict.get('sess', {}).get('cards')
card_scores = [card.get('score') for card in cards]
max_card_score = max(card_scores)
best_card_values = [card.get('values') for card in cards if card.get('score') == max_card_score][0]
card_suit_strs = ['S', 'H', 'D', 'C']
card_value_strs = '23456789TJQKA'
best_leads = []
for suit_index, suit_value_indices in enumerate(best_card_values):
    suit_str = card_suit_strs[suit_index]
    for value_index in suit_value_indices:
        value_str = card_value_strs[value_index]
        best_leads.append(value_str + suit_str)

actual_lead = dds_parameter_dict.get('lead')

print()
print('actual lead:', actual_lead)
print('best leads:', best_leads)
if actual_lead in best_leads:
    print('Good lead!')
else:
    print('Bad lead!')

# optimal_points_raw = scrape_double_dummy.get_optimal_points_for_deal(scrape_stepbridge.get_board_double_dummy_url(a_board_tag))
# optimal_points = -optimal_points_raw if flip_optimal_points else optimal_points_raw
#
# our_score = util.convert_dutch_percentage_string_to_float(our_result_dict.get('score'))
# optimal_score = util.calculate_mp_score(other_points + [optimal_points], optimal_points)
# possible_gain = max(0.0, optimal_score - our_score)


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
print()
print('done')

# overview_url = 'https://portal.stepbridge.nl/tournament/events/index/users/74285'
# print('overview_url:', overview_url)
#
# df_all_tournament_overview = scrape_stepbridge.get_stepbridge_tournament_overview_dataframe(overview_url)
# print(df_all_tournament_overview)


# TODO: extract bidding
# TODO: extract all double dummy contracts

# TODO: later,
# 1 from dds analysis page
# 2 click optimal contract and get reponse dict
# 3 see lead scores vs actual leads
# --> wrong lead detection
