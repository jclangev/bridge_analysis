#!/usr/bin/env python3
"""
module string
"""

__author__ = "Joost Langeveld"
__license__ = "MIT"

import bs4
import mechanize

from http import cookiejar


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


def get_browser() -> mechanize.Browser:
    cj = cookiejar.CookieJar()
    br = mechanize.Browser()
    br.set_handle_robots(False)
    br.set_cookiejar(cj)
    return br


def get_soup(browser: mechanize.Browser, url: str) -> bs4.element.Tag:
    browser.open(url)
    content = browser.response().read()
    return bs4.BeautifulSoup(content, 'html.parser')
