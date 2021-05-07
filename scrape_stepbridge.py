#!/usr/bin/env python3
"""
module string
"""

__author__ = "Joost Langeveld"
__license__ = "MIT"

from collections import OrderedDict

import bs4


def get_board_id(board_tag: bs4.element.Tag) -> str:
    result = board_tag.findChild('th', {'class': 'boardheaderleft'}).text
    result = result.replace('\n', '').replace('            ', ' ')
    return result


def get_board_double_dummy_url(board_tag: bs4.element.Tag) -> str:
    externals = board_tag.find_all(class_='external')
    external = externals[1]
    return external['href']


def get_board_result_dicts(board_tag: bs4.element.Tag, fieldrow_class_name: str) -> list:
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
    for fieldrow in board_tag.find_all(class_=fieldrow_class_name):
        result.append(get_fieldrow_dict(fieldrow))
    return result
