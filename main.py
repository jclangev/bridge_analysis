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

from collections import OrderedDict

import scrape_stepbridge
from scrape_double_dummy import get_optimal_points_for_deal


def convert_dutch_percentage_string_to_float(text: str) -> float:
    return float(text.replace('%', '').replace(',', '.'))


def calculate_mp_score(all_points: list, points_to_score: int) -> float:
    def triangle_number(number: int) -> int:
        return number * (number + 1) // 2

    num_above = len([points for points in all_points if points > points_to_score])
    num_equal = len([points for points in all_points if points == points_to_score])
    # num_below = len([points for points in all_points if points < points_to_score])
    num_total = len(all_points)

    triangle_above = triangle_number(num_above)
    triangle_equal = triangle_number(num_above + num_equal)

    avg_rank_base_0_equal = (triangle_equal - triangle_above) / num_equal - 1.0

    result_score_base_100 = 100.0 * (num_total - 1.0 - avg_rank_base_0_equal) / (num_total - 1.0)
    return round(result_score_base_100, 2)


def get_board_chair_dict(board_tag: bs4.element.Tag) -> OrderedDict:
    board_chair_labels = board_tag.find_all('td', {'class': 'boardchairlabel'})
    board_chairs = [(board_chair_label.text.split('-')[1].replace('/n', '').strip(),
                    board_chair_label.text.split('-')[0].replace('/n', '').strip())
                    for board_chair_label in board_chair_labels]
    return OrderedDict(board_chairs)


step_url = 'https://results.stepbridge.nl/tournament/events/show/38602/JoostL'
my_name = os.path.basename(step_url)

print('step_url:', step_url)
print('my name:', my_name)
print()

page = requests.get(step_url)
soup = bs4.BeautifulSoup(page.content, 'html.parser')

board_tags = soup.find_all('table', class_='board')

our_scores = []
optimal_scores = []
possible_gains = []
for i, a_board_tag in enumerate(board_tags):
    board_id = scrape_stepbridge.get_board_id(a_board_tag)

    other_result_dicts = scrape_stepbridge.get_board_result_dicts(a_board_tag, 'fieldrow')
    our_result_dict = scrape_stepbridge.get_board_result_dicts(a_board_tag, 'fieldrowselected')[0]

    other_points = [int(fieldrow_dict.get('punten')) for fieldrow_dict in other_result_dicts]
    our_points = int(our_result_dict.get('punten'))

    board_chair_dict = get_board_chair_dict(a_board_tag)
    flip_optimal_points = (board_chair_dict.get(my_name).upper()) in ['O', 'W']
    optimal_points_raw = get_optimal_points_for_deal(scrape_stepbridge.get_board_double_dummy_url(a_board_tag))
    optimal_points = -optimal_points_raw if flip_optimal_points else optimal_points_raw

    our_score = convert_dutch_percentage_string_to_float(our_result_dict.get('score'))
    optimal_score = calculate_mp_score(other_points + [optimal_points], optimal_points)
    possible_gain = max(0.0, optimal_score - our_score)

    our_scores.append(our_score)
    optimal_scores.append(optimal_score)
    possible_gains.append(possible_gain)

    # print('other points:', other_points)
    # print('our points:', our_points)
    # print('optimal points:', optimal_points)
    print(f'board {i + 1:2}:  our points: {our_points:5}  '
          + f'optimal points: {optimal_points:5}  '
          + f'board {i + 1:2}:  our score: {our_score:6.2f}  '
          + f'optimal score: {optimal_score:6.2f}  '
          + f'possible gain: {possible_gain:6.2f}')

our_total_score = np.mean(our_scores)
optimal_total_score = np.mean(optimal_scores)
total_possible_gain = np.mean(possible_gains)

print()
print(f'our score:           {our_total_score:6.2f}')
print(f'total possible gain: {total_possible_gain:6.2f}')
print(f'possible max score:  {our_total_score + total_possible_gain:6.2f}')
print()
print('done')
