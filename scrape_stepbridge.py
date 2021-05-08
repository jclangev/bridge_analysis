#!/usr/bin/env python3
"""
module string
"""

__author__ = "Joost Langeveld"
__license__ = "MIT"

from collections import OrderedDict

import bs4


def get_clean_text_with_img_replaced_by_alt(tag: bs4.element.Tag) -> str:
    if tag.findChild('img'):
        suit = tag.find('img').get('alt')
        tag.find('img').replace_with(suit)
    return tag.text.replace('\n', '').strip()


def get_board_id(board_tag: bs4.element.Tag) -> str:
    result = board_tag.findChild('th', {'class': 'boardheaderleft'}).text
    result = result.replace('\n', '').replace('            ', ' ')
    return result


def get_board_double_dummy_url(board_tag: bs4.element.Tag) -> str:
    externals = board_tag.find_all(class_='external')
    external = externals[1]
    return external['href']


def get_board_result_dicts(board_tag: bs4.element.Tag, fieldrow_class_name: str) -> list:
    def get_fieldrow_dict(field_row: bs4.element.Tag) -> dict:
        keys = ['leider', 'contract', 'resultaat', 'door', 'uitkomst', 'punten', 'score']
        result_fieldrow_dict = OrderedDict([])
        fieldrow_columns = field_row.findChildren('td')
        for fieldrow_column, key in zip(fieldrow_columns, keys):
            result_fieldrow_dict[key] = get_clean_text_with_img_replaced_by_alt(fieldrow_column)
        return result_fieldrow_dict

    result = []
    for fieldrow in board_tag.find_all(class_=fieldrow_class_name):
        result.append(get_fieldrow_dict(fieldrow))
    return result


def get_our_result(board_tag: bs4.element.Tag) -> str:
    board_tables = board_tag.findChild('tbody').find('tr').find('td').find_all('table')
    our_result_rows = board_tables[2].find_all('tr')
    our_contract_points_tag = our_result_rows[0].find_all('td')[1]
    result_string = get_clean_text_with_img_replaced_by_alt(our_contract_points_tag)
    return result_string


def get_our_score(board_tag: bs4.element.Tag) -> str:
    board_tables = board_tag.findChild('tbody').find('tr').find('td').find_all('table')
    our_result_rows = board_tables[2].find_all('tr')
    our_score_tag = our_result_rows[1].find_all('td')[1]
    score_string = get_clean_text_with_img_replaced_by_alt(our_score_tag)
    return score_string
