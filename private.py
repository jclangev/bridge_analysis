#!/usr/bin/env python3
"""
module string
"""

__author__ = "Joost Langeveld"
__license__ = "MIT"

import mechanize


def browser_login_stepbridge(browser: mechanize.Browser) -> mechanize.Browser:
	login_url_stepbridge = 'https://portal.stepbridge.nl/login'
	browser.open(login_url_stepbridge)

	browser.select_form(nr=0)
	browser.form['username'] = 'JoostL'
	browser.form['password'] = '970008'
	browser.submit()

	return browser
