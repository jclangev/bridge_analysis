#!/usr/bin/env python3
"""
Module Docstring
"""

__author__ = "Joost Langeveld"
__version__ = "0.1.0"
__license__ = "MIT"

import json
import urllib.request


def get_double_dummy_analysis_dict_for_deal(double_dummy_analysis_url: str) -> int:
    """"
    takes URL for Double Dummy Solver at dds.bridgewebs.com and returns optimal score for deal in that URL
    """

    def convert_dds_bridgewebs_com_url_to_parameter_dict(dds_bridgewebs_com_url: str) -> dict:
        parameter_separator = '&'
        key_value_separator = '='
        return {
            pair.split(key_value_separator)[0]: pair.split(key_value_separator)[1]
            for pair in dds_bridgewebs_com_url.split(parameter_separator)
        }

    def make_deal_str(parameter_dict: dict) -> str:
        deal_string_prefix = 'W:'
        hand_separator = 'x'
        parameter_separator = '&'
        key_value_separator = '='

        hands_keys = ['west', 'north', 'east', 'south']
        deal_str_result = deal_string_prefix + parameter_dict.get(hands_keys[0])
        for hand_key in hands_keys[1:]:
            deal_str_result += hand_separator + parameter_dict.get(hand_key)

        key_value_keys = ['vul']
        for key in key_value_keys:
            deal_str_result += parameter_separator + key + key_value_separator + parameter_dict.get(key)

        return deal_str_result

    dds_url_prefix = 'https://dds.bridgewebs.com/cgi-bin/bsol2/ddummy?request=m&dealstr='
    dds_url_deal_str = make_deal_str(convert_dds_bridgewebs_com_url_to_parameter_dict(double_dummy_analysis_url))
    dds_url = dds_url_prefix + dds_url_deal_str

    response = urllib.request.urlopen(dds_url)
    response_string = response.read().decode('utf-8')
    response_dict = json.loads(response_string)

    return response_dict


def get_optimal_score_from_double_dummy_analysis_dict(double_dummy_analysis_dict: dict) -> dict:
    optimal_score_key = 'scoreNS'
    optimal_score_prefix = 'NS '
    optimal_score_raw_string = double_dummy_analysis_dict.get(optimal_score_key, optimal_score_prefix)
    optimal_score_string = optimal_score_raw_string.replace(optimal_score_prefix, '')
    result = int(optimal_score_string)
    return result


def get_optimal_score_for_deal(double_dummy_analysis_url: str) -> int:
    """"
    takes URL for Double Dummy Solver at dds.bridgewebs.com and returns optimal score for deal in that URL
    """
    double_dummy_analysis_dict = get_double_dummy_analysis_dict_for_deal(double_dummy_analysis_url)
    return get_optimal_score_from_double_dummy_analysis_dict(double_dummy_analysis_dict)


url = 'https://dds.bridgewebs.com/bsol2/ddummy.htm?club=stepbridge_nl&board=1'\
      + '&dealer=N&vul=None&contract=4C&declarer=E&lead=KH' \
      + '&north=Q86.T763.T82.862&east=K7.54.K97.AQT743&south=A953.AKJ98.J5.J9&west=JT42.Q2.AQ643.K5'\
      + '&analyse=true&title=%3Ch1%3EStepBridge%20Double%20Dummy%20Analysis%3C/h1%3E'
print('url:', url)
dds_dict = get_double_dummy_analysis_dict_for_deal(url)
print('optimal dict:', get_optimal_score_for_deal(url))
