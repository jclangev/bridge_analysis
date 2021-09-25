#!/usr/bin/env python3
"""
Scrape results and board details from bridge.nl
"""

__author__ = "Joost Langeveld"
__license__ = "MIT"

import bs4
import pandas as pd
import re


from util import get_browser, get_soup


def scrape_cards_bridge_nl(url: str, browser=get_browser()) -> dict:
    winds_bridge_nl = 'NWES'
    soup = get_soup(browser=browser, url=url)
    hand_tags = soup.find_all('div', class_='vierkant33procent spelverdeling_hand')
    return {wind: hand_tag.text.split('\n')[1:5] for wind, hand_tag in zip(winds_bridge_nl, hand_tags)}


bridge_nl_url_prefix = 'https://uitslagen.bridge.nl/ords/'
bridge_nl_overview_url_suffix = 'f?p=300:2010:8013769507611::NO:RP:P0_VER_ID_NBB:2043'
bridge_nl_overview_url = bridge_nl_url_prefix + bridge_nl_overview_url_suffix

player_name = 'Joost Langeveld'

url = bridge_nl_overview_url
normal_browser = get_browser()
soup = get_soup(browser=normal_browser, url=url)

#
a_tournament_tags = soup.find_all('td', class_='t-Report-cell', headers="STAND")
for i, a_tournament_tag in enumerate(a_tournament_tags):
    tournament_name = a_tournament_tag.find('a').text
    tournament_url = bridge_nl_url_prefix + a_tournament_tag.find('a')['href']
    # print(f'{i:2} tournament_name={tournament_name:60} url={tournament_url}')

url = tournament_url
soup = get_soup(browser=normal_browser, url=url)
a_result_tags = soup.find_all('td', class_='t-Report-cell', headers="NAAM_000")
for i, a_result_tag in enumerate(a_result_tags):
    result_name = a_result_tag.find('a').text
    result_url = bridge_nl_url_prefix + a_result_tag.find('a')['href']
    # print(f'{i:2} result_name={result_name:60} url={result_url}')

    if player_name.lower().strip() in result_name.lower():
        player_result_url = result_url

url = player_result_url
soup = get_soup(browser=normal_browser, url=url)
tags = soup.find_all('td', class_='t-Report-cell', headers=re.compile('SPELNUMMER*'))
for i, tag in enumerate(tags):
    name = tag.find('a').text
    url = bridge_nl_url_prefix + tag.find('a')['href']
    print(scrape_cards_bridge_nl(url, normal_browser))






