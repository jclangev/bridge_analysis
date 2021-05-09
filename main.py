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

# from scrape_double_dummy import get_optimal_points_for_deal
# from scrape_stepbridge import get_board_chair_dict
import scrape_stepbridge
# from util import convert_dutch_percentage_string_to_float, calculate_mp_score

# step_url = 'https://results.stepbridge.nl/tournament/events/show/38602/JoostL'
# step_url = 'https://results.stepbridge.nl/tournament/events/show/32185/JoostL'
# my_name = os.path.basename(step_url)
#
# print('step_url:', step_url)
# print('my name:', my_name)
# print()
#
# page = requests.get(step_url)
# soup = bs4.BeautifulSoup(page.content, 'html.parser')
#
# our_point_list = []
# optimal_point_List = []
# our_scores = []
# optimal_scores = []
# possible_gains = []
# for i, a_board_tag in enumerate(soup.find_all('table', class_='board')[0:1]):
#     board_id = scrape_stepbridge.get_board_id(a_board_tag)
#
#     other_result_dicts = scrape_stepbridge.get_board_result_dicts(a_board_tag, 'fieldrow')
#     our_result_dict = scrape_stepbridge.get_board_result_dicts(a_board_tag, 'fieldrowselected')[0]
#
#     other_points = [int(fieldrow_dict.get('punten')) for fieldrow_dict in other_result_dicts]
#     our_points = int(our_result_dict.get('punten'))
#     board_chair_dict = get_board_chair_dict(a_board_tag)
#     flip_optimal_points = (board_chair_dict.get(my_name).upper()) in ['O', 'W']
#     optimal_points_raw = get_optimal_points_for_deal(scrape_stepbridge.get_board_double_dummy_url(a_board_tag))
#     optimal_points = -optimal_points_raw if flip_optimal_points else optimal_points_raw
#
#     our_score = convert_dutch_percentage_string_to_float(our_result_dict.get('score'))
#     optimal_score = calculate_mp_score(other_points + [optimal_points], optimal_points)
#     possible_gain = max(0.0, optimal_score - our_score)
#
#     # add to result list
#     our_point_list.append(our_points)
#     optimal_point_List.append(optimal_points)
#     our_scores.append(our_score)
#     optimal_scores.append(optimal_score)
#     possible_gains.append(possible_gain)
#
#     print(f'{board_id:16} '
#           + f'our points: {our_points:5}  '
#           + f'optimal points: {optimal_points:5}  '
#           + f'board {i + 1:2}:  our score: {our_score:6.2f}  '
#           + f'optimal score: {optimal_score:6.2f}  '
#           + f'possible gain: {possible_gain:6.2f}')
#
# our_total_score = np.mean(our_scores)
# optimal_total_score = np.mean(optimal_scores)
# total_possible_gain = np.mean(possible_gains)
#
# print()
# print(f'our score:           {our_total_score:6.2f}')
# print(f'total possible gain: {total_possible_gain:6.2f}')
# print(f'possible max score:  {our_total_score + total_possible_gain:6.2f}')
# print()
# print('done')


overview_url = 'https://portal.stepbridge.nl/tournament/events/index/users/74285'
print('overview_url:', overview_url)

df_all_tournament_overview = scrape_stepbridge.get_stepbridge_tournament_overview_dataframe(overview_url)
print(df_all_tournament_overview)
