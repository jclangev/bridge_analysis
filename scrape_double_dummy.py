#!/usr/bin/env python3
"""
module string
"""

__author__ = "Joost Langeveld"
__license__ = "MIT"

import json
import urllib.request


DDS_QUERY_URL_PREFIX = 'https://dds.bridgewebs.com/cgi-bin/bsol2/ddummy?'
DDS_QUERY_PARAMETER_SEPARATOR = '&'
DDS_QUERY_KEY_VALUE_SEPARATOR = '='


def extract_parameter_dict_from_dds_url(dds_bridgewebs_com_url: str) -> dict:
    query_parameter_string = dds_bridgewebs_com_url.split('?')[1]
    return {
        pair.split(DDS_QUERY_KEY_VALUE_SEPARATOR)[0]: pair.split(DDS_QUERY_KEY_VALUE_SEPARATOR)[1]
        for pair in query_parameter_string.split(DDS_QUERY_PARAMETER_SEPARATOR)
    }


def make_lead_deal_str(parameter_dict: dict) -> str:
    deal_string_key = 'dealstr'
    hand_separator = 'x'
    hands_keys = ['west', 'north', 'east', 'south']
    deal_str_result = DDS_QUERY_PARAMETER_SEPARATOR + deal_string_key
    deal_str_result += DDS_QUERY_KEY_VALUE_SEPARATOR + parameter_dict.get(hands_keys[0])
    for hand_key in hands_keys[1:]:
        deal_str_result += hand_separator + parameter_dict.get(hand_key)
    return deal_str_result


def make_bidding_deal_str(parameter_dict: dict) -> str:
    hand_separator = 'x'
    hands_keys = ['west', 'north', 'east', 'south']
    deal_str_result = DDS_QUERY_PARAMETER_SEPARATOR + 'dealstr' + DDS_QUERY_KEY_VALUE_SEPARATOR
    deal_str_result += 'W:' + parameter_dict.get(hands_keys[0])
    for hand_key in hands_keys[1:]:
        deal_str_result += hand_separator + parameter_dict.get(hand_key)
    return deal_str_result


def declarer_to_leader_str(parameter_dict: dict) -> str:
    declarer_key = 'declarer'
    leader_key = 'leader'
    declarer_to_leader_translation_dict = {'W': 'n', 'N': 'o', 'O': 'z', 'Z': 'w'}
    leader_str_result = DDS_QUERY_PARAMETER_SEPARATOR + leader_key + DDS_QUERY_KEY_VALUE_SEPARATOR
    leader_str_result += declarer_to_leader_translation_dict.get(parameter_dict.get(declarer_key))
    return leader_str_result


def contract_to_trumps_str(parameter_dict: dict) -> str:
    trump_key = 'trumps'
    contract_key = 'contract'
    contract = parameter_dict.get(contract_key)
    trumps = contract[-1]
    return DDS_QUERY_PARAMETER_SEPARATOR + trump_key + DDS_QUERY_KEY_VALUE_SEPARATOR + trumps


def copied_parameters_str(parameter_dict: dict) -> str:
    key_value_keys = ['vul']
    parameters_str_result = ''
    for key in key_value_keys:
        parameters_str_result += DDS_QUERY_PARAMETER_SEPARATOR + key
        parameters_str_result += DDS_QUERY_KEY_VALUE_SEPARATOR + parameter_dict.get(key)
    return parameters_str_result


def get_double_dummy_analysis_bidding_query_url(double_dummy_analysis_url: str) -> str:
    """"For bidding analysis"""
    url_parameter_dict = extract_parameter_dict_from_dds_url(double_dummy_analysis_url)
    dds_url = DDS_QUERY_URL_PREFIX + 'request' + DDS_QUERY_KEY_VALUE_SEPARATOR + 'm'
    dds_url += make_bidding_deal_str(url_parameter_dict)
    dds_url += copied_parameters_str(url_parameter_dict)
    return dds_url


def get_double_dummy_analysis_lead_query_url(double_dummy_analysis_url: str) -> str:
    """"For lead analysis"""
    url_parameter_dict = extract_parameter_dict_from_dds_url(double_dummy_analysis_url)
    dds_url = DDS_QUERY_URL_PREFIX + 'request' + DDS_QUERY_KEY_VALUE_SEPARATOR + 'g'
    dds_url += make_lead_deal_str(url_parameter_dict)
    dds_url += declarer_to_leader_str(url_parameter_dict)
    dds_url += contract_to_trumps_str(url_parameter_dict)
    dds_url += copied_parameters_str(url_parameter_dict)
    return dds_url


def get_double_dummy_analysis_dict_for_deal(double_dummy_analysis_url: str) -> dict:
    """"
    takes URL for Double Dummy Solver at dds.bridgewebs.com and returns optimal score for deal in that URL
    """
    response = urllib.request.urlopen(double_dummy_analysis_url)
    response_string = response.read().decode('utf-8')
    response_dict = json.loads(response_string)
    return response_dict


def get_optimal_points_from_double_dummy_analysis_dict(double_dummy_analysis_dict: dict) -> int:
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


def get_best_leads_for_optimal_contract(double_dummy_url: str) -> list:
    dds_lead_query_url = get_double_dummy_analysis_lead_query_url(double_dummy_url)
    dds_lead_analysis_dict = get_double_dummy_analysis_dict_for_deal(dds_lead_query_url)

    cards = dds_lead_analysis_dict.get('sess', {}).get('cards')
    card_scores = [card.get('score') for card in cards]
    max_card_score = max(card_scores)
    best_card_values = [card.get('values') for card in cards if card.get('score') == max_card_score][0]
    card_suit_strs = ['S', 'H', 'D', 'C']
    card_value_strs = '23456789TJQKA'
    result = []
    for suit_index, suit_value_indices in enumerate(best_card_values):
        suit_str = card_suit_strs[suit_index]
        for value_index in suit_value_indices:
            value_str = card_value_strs[value_index]
            result.append(value_str + suit_str)

    return result
