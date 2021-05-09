#!/usr/bin/env python3
"""
module string
"""

__author__ = "Joost Langeveld"
__license__ = "MIT"

import bs4
import pandas as pd
import mechanize

import util

from collections import OrderedDict
from private import browser_login_stepbridge

TOURNAMENT_DATE_KEY = 'Date'
TOURNAMENT_CLUB_KEY = 'Club'
TOURNAMENT_SCORE_KEY = 'Score'
TOURNAMENT_PLACE_KEY = 'Place'
TOURNAMENT_URL_KEY = 'Link'


def get_clean_text_with_img_replaced_by_alt(tag: bs4.element.Tag) -> str:
    if tag.findChild('img'):
        suit = tag.find('img').get('alt')
        tag.find('img').replace_with(suit)
    return tag.text.replace('\n', '').strip()


def get_board_id(board_tag: bs4.element.Tag) -> str:
    result = board_tag.findChild('th', {'class': 'boardheaderleft'}).text
    result = result.replace('\n', '').replace('            ', ' ').strip()
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


def get_board_chair_dict(board_tag: bs4.element.Tag) -> OrderedDict:
    board_chair_labels = board_tag.find_all('td', {'class': 'boardchairlabel'})
    board_chairs = [(board_chair_label.text.split('-')[1].replace('/n', '').strip(),
                     board_chair_label.text.split('-')[0].replace('/n', '').strip())
                    for board_chair_label in board_chair_labels]
    return OrderedDict(board_chairs)


def get_other_page_urls_from_overview_page_stepbridge_my_results(page_soup: bs4.element.Tag) -> list:
    try:
        pagination_tag = page_soup.find('ul', {'class': 'pagination'})
        page_items = pagination_tag.find_all('li', {'class': 'page-item'})
        link_items = [page_item.find('a') for page_item in page_items if page_item.find('a') is not None]
        page_urls = [link_item['href'] for link_item in link_items]
        unique_page_urls = list(OrderedDict.fromkeys(page_urls))
        return unique_page_urls
    except AttributeError:
        return []


def get_tournament_result_row_dict(tournament_results_row_tag: bs4.element.Tag) -> OrderedDict:
    tournament_result_keys = [
        TOURNAMENT_DATE_KEY,
        TOURNAMENT_CLUB_KEY,
        TOURNAMENT_SCORE_KEY,
        TOURNAMENT_PLACE_KEY,
        TOURNAMENT_URL_KEY
    ]
    tournament_results_row_cols = tournament_results_row_tag.find_all('td')
    result = OrderedDict([])
    for i, key in enumerate(tournament_result_keys):
        if key == TOURNAMENT_URL_KEY:
            result[key] = tournament_results_row_cols[i].find_all('a')[1]['href']
        else:
            result[key] = tournament_results_row_cols[i].text

    return result


def get_tournament_overview_dataframe(tournament_results_page_soup: bs4.element.Tag) -> pd.DataFrame:
    tournament_results_table_body = tournament_results_page_soup.find('table', {'class': 'table'}).find('tbody')
    tournament_results_rows = tournament_results_table_body.find_all('tr')
    tournament_results_row_dicts = [get_tournament_result_row_dict(tournament_results_row)
                                    for tournament_results_row in tournament_results_rows]
    return pd.DataFrame(tournament_results_row_dicts)


def get_all_tournament_overview_dataframe(browser: mechanize.Browser,
                                          tournament_result_overview_urls: list) -> pd.DataFrame:
    result = None
    for url in tournament_result_overview_urls:
        page_soup = util.get_soup(browser=browser, url=url)
        df_tournament_results_single_page = get_tournament_overview_dataframe(page_soup)
        if result is None:
            result = df_tournament_results_single_page
        else:
            result = result.append(df_tournament_results_single_page)
    result.reset_index(drop=True, inplace=True)
    return result


def get_stepbridge_tournament_overview_dataframe(stepbridge_user_url: str) -> pd.DataFrame:
    logged_in_browser = browser_login_stepbridge(util.get_browser())
    initial_soup = util.get_soup(browser=logged_in_browser,
                                 url=stepbridge_user_url)

    overview_page_urls = [stepbridge_user_url]
    overview_page_urls += get_other_page_urls_from_overview_page_stepbridge_my_results(initial_soup)

    result = get_all_tournament_overview_dataframe(browser=logged_in_browser,
                                                   tournament_result_overview_urls=overview_page_urls)
    return result
