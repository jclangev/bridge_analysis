#!/usr/bin/env python3
"""
Module Docstring
"""

__author__ = "Joost Langeveld"
__version__ = "0.1.0"
__license__ = "MIT"

from pprint import pprint

from scrape_double_dummy import get_optimal_points_for_deal

import requests
from bs4 import BeautifulSoup

from scrape_stepbridge import get_board_id, get_board_double_dummy_url, get_board_result_dicts

step_url = 'https://results.stepbridge.nl/tournament/events/show/38602/JoostL'
print('step_url:', step_url)

page = requests.get(step_url)
soup = BeautifulSoup(page.content, 'html.parser')

board_tags = soup.find_all('table', class_='board')
for i, board_tag in enumerate(board_tags[0:1]):
    board_id = get_board_id(board_tag)
    optimal_points = get_optimal_points_for_deal(get_board_double_dummy_url(board_tag))
    other_result_dicts = get_board_result_dicts(board_tag, 'fieldrow')
    our_result_dict = get_board_result_dicts(board_tag, 'fieldrowselected')[0]
    other_points = [int(fieldrow_dict.get('punten')) for fieldrow_dict in other_result_dicts]
    our_points = int(our_result_dict.get('punten'))

    print('other points:', other_points)
    print('our points:', our_points)
    print('optimal points:', optimal_points)
