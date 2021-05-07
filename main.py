#!/usr/bin/env python3
"""
Module Docstring
"""

__author__ = "Joost Langeveld"
__version__ = "0.1.0"
__license__ = "MIT"

from webscraping import get_double_dummy_analysis_dict_for_deal, get_optimal_score_for_deal

url = 'https://dds.bridgewebs.com/bsol2/ddummy.htm?club=stepbridge_nl&board=1'\
      + '&dealer=N&vul=None&contract=4C&declarer=E&lead=KH' \
      + '&north=Q86.T763.T82.862&east=K7.54.K97.AQT743&south=A953.AKJ98.J5.J9&west=JT42.Q2.AQ643.K5'\
      + '&analyse=true&title=%3Ch1%3EStepBridge%20Double%20Dummy%20Analysis%3C/h1%3E'
print('url:', url)
dds_dict = get_double_dummy_analysis_dict_for_deal(url)
print('optimal dict:', get_optimal_score_for_deal(url))
