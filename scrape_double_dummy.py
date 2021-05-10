#!/usr/bin/env python3
"""
module string
"""

__author__ = "Joost Langeveld"
__license__ = "MIT"

import json
import urllib.request


PARAMETER_SEPARATOR = '&'
KEY_VALUE_SEPARATOR = '='


def convert_dds_bridgewebs_com_url_to_parameter_dict(dds_bridgewebs_com_url: str) -> dict:
    parameter_separator = '&'
    key_value_separator = '='
    return {
        pair.split(key_value_separator)[0]: pair.split(key_value_separator)[1]
        for pair in dds_bridgewebs_com_url.split(parameter_separator)
    }


def get_double_dummy_analysis_bidding_query_url(double_dummy_analysis_url: str) -> str:
    """"For bidding analysis"""
    def make_bidding_deal_str(parameter_dict: dict) -> str:
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
    dds_url_deal_str = make_bidding_deal_str(convert_dds_bridgewebs_com_url_to_parameter_dict(double_dummy_analysis_url))
    return dds_url_prefix + dds_url_deal_str


def get_double_dummy_analysis_lead_query_url(double_dummy_analysis_url: str) -> str:
    """"For lead analysis"""

    def make_lead_deal_str(parameter_dict: dict) -> str:
        deal_string_key = 'dealstr'
        hand_separator = 'x'
        hands_keys = ['west', 'north', 'east', 'south']
        deal_str_result = parameter_separator + deal_string_key
        deal_str_result += key_value_separator + parameter_dict.get(hands_keys[0])
        for hand_key in hands_keys[1:]:
            deal_str_result += hand_separator + parameter_dict.get(hand_key)

        return deal_str_result

    def declarer_to_leader_str(parameter_dict: dict) -> str:
        declarer_key = 'declarer'
        leader_key = 'leader'
        declarer_to_leader_translation_dict = {'W': 'n', 'N': 'o', 'O': 'z', 'Z': 'w'}
        leader_str_result = parameter_separator + leader_key + key_value_separator
        leader_str_result += declarer_to_leader_translation_dict.get(parameter_dict.get(declarer_key))
        return leader_str_result

    def contract_to_trumps_str(parameter_dict: dict) -> str:
        trump_key = 'trumps'
        contract_key = 'contract'
        contract = parameter_dict.get(contract_key)
        trumps = contract[-1]
        return parameter_separator + trump_key + key_value_separator + trumps

    def copied_parameters_str(parameter_dict: dict) -> str:
        key_value_keys = ['vul']
        parameters_str_result = ''
        for key in key_value_keys:
            parameters_str_result += parameter_separator + key + key_value_separator + parameter_dict.get(key)
        return parameters_str_result

    url_parameter_dict = convert_dds_bridgewebs_com_url_to_parameter_dict(double_dummy_analysis_url)

    dds_url = 'https://dds.bridgewebs.com/cgi-bin/bsol2/ddummy'
    dds_url += make_lead_deal_str(url_parameter_dict)
    dds_url += declarer_to_leader_str(url_parameter_dict)
    dds_url += contract_to_trumps_str(url_parameter_dict)
    dds_url += copied_parameters_str

    return dds_url


def get_double_dummy_analysis_dict_for_deal(double_dummy_analysis_url: str) -> int:
    """"
    takes URL for Double Dummy Solver at dds.bridgewebs.com and returns optimal score for deal in that URL
    """
    response = urllib.request.urlopen(double_dummy_analysis_url)
    response_string = response.read().decode('utf-8')
    response_dict = json.loads(response_string)

    return response_dict


def get_optimal_points_from_double_dummy_analysis_dict(double_dummy_analysis_dict: dict) -> dict:
    optimal_points_key = 'scoreNS'
    optimal_points_prefix = 'NS '
    optimal_points_raw_string = double_dummy_analysis_dict.get(optimal_points_key, optimal_points_prefix)
    optimal_points_string = optimal_points_raw_string.replace(optimal_points_prefix, '')
    result = int(optimal_points_string)
    return result


def get_optimal_points_for_deal(double_dummy_analysis_url: str) -> int:
    """"
    takes URL for Double Dummy Solver at dds.bridgewebs.com and returns optimal score for deal in that URL
    """
    double_dummy_analysis_dict = get_double_dummy_analysis_dict_for_deal(double_dummy_analysis_url)
    return get_optimal_points_from_double_dummy_analysis_dict(double_dummy_analysis_dict)