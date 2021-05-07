#!/usr/bin/env python3
"""
Module Docstring
"""

__author__ = "Joost Langeveld"
__version__ = "0.1.0"
__license__ = "MIT"

from collections import OrderedDict
from pprint import pprint

from scrape_double_dummy import get_double_dummy_analysis_dict_for_deal, get_optimal_score_for_deal

import requests
import bs4
from bs4 import BeautifulSoup


def get_board_id(board_tag: bs4.element.Tag) -> str:
    result = board_tag.findChild('th', {'class': 'boardheaderleft'}).text
    result = result.replace('\n', '').replace('            ', ' ')
    return result


def get_board_double_dummy_url(board_tag: bs4.element.Tag) -> str:
    externals = board_tag.find_all(class_='external')
    external = externals[1]
    return external['href']


def get_board_result_dicts(board_tag: bs4.element.Tag) -> list:
    def get_field_row_column_value(fieldrow_column: bs4.element.Tag) -> str:
        if fieldrow_column.findChild('img'):
            return fieldrow_column.text + fieldrow_column.findChild('img').get('alt')
        else:
            return fieldrow_column.text.replace('\n', '')

    def get_fieldrow_dict(field_row: bs4.element.Tag) -> dict:
        keys = ['leider', 'contract', 'resultaat', 'door', 'uitkomst', 'punten', 'score']
        result_fieldrow_dict = OrderedDict([])
        fieldrow_columns = field_row.findChildren('td')
        for fieldrow_column, key in zip(fieldrow_columns, keys):
            result_fieldrow_dict[key] = get_field_row_column_value(fieldrow_column)
        return result_fieldrow_dict

    result = []
    for fieldrow in board_tag.find_all(class_='fieldrow'):  # other results
        result.append(get_fieldrow_dict(fieldrow))
    for fieldrow in board_tag.find_all(class_='fieldrowselected'):  # own result
        result.append(get_fieldrow_dict(fieldrow))
    return result


step_url = 'https://results.stepbridge.nl/tournament/events/show/38602/JoostL'
print('step_url:', step_url)

dds_url = 'https://dds.bridgewebs.com/bsol2/ddummy.htm?club=stepbridge_nl&board=1' \
          + '&dealer=N&vul=None&contract=4C&declarer=E&lead=KH' \
          + '&north=Q86.T763.T82.862&east=K7.54.K97.AQT743&south=A953.AKJ98.J5.J9&west=JT42.Q2.AQ643.K5' \
          + '&analyse=true&title=%3Ch1%3EStepBridge%20Double%20Dummy%20Analysis%3C/h1%3E'
# print('dds_url:', dds_url)

# dds_dict = get_double_dummy_analysis_dict_for_deal(dds_url)
# print('optimal dict:', get_optimal_score_for_deal(dds_url))

page = requests.get(step_url)
soup = BeautifulSoup(page.content, 'html.parser')

board_tags = soup.find_all('table', class_='board')
for i, board_tag in enumerate(board_tags[0:1]):
    board_id = get_board_id(board_tag)
    double_dummy_url = get_board_double_dummy_url(board_tag)
    optimal_score = get_optimal_score_for_deal(double_dummy_url)
    fieldrow_dicts = get_board_result_dicts(board_tag)
    for fieldrow_dict in fieldrow_dicts:
        pprint(fieldrow_dict)
