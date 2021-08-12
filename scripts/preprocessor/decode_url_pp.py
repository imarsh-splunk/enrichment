#!python
#!/bin/env python
# --
# File: decode_url_pp.py
#
# Copyright (c) 2020 Splunk Inc.
#
# SPLUNK CONFIDENTIAL - Use or disclosure of this material in whole or in part
# without a valid written license from Splunk Inc. is PROHIBITED."""
# --

import sys
import re
import urllib.parse
import html.parser

#decoding rewritten url from PP
def rewrittenurl(url_):
	if url_:
		rewrittenurl = url_.replace('&amp;','&')
		match = re.search(r'https://urldefense.proofpoint.com/(v[0-9])/', rewrittenurl)
		url = ''
		if match:
			if match.group(1) == 'v1':
				url = decodev1(rewrittenurl)
			elif match.group(1) == 'v2':
				url = decodev2(rewrittenurl)
			else:
				print('Unrecognized version in: ', rewrittenurl)

		else:
			print('No valid URL found in input: ', rewrittenurl)
	if not url:
		return url_
	else:
		return url
def decodev1 (rewrittenurl):
	match = re.search(r'u=(.+?)&k=',rewrittenurl)
	if match:
		urlencodedurl = match.group(1)
		htmlencodedurl = urllib.parse.unquote(urlencodedurl)
		url = html.parser.HTMLParser().unescape(htmlencodedurl)
		return url
	else:
		print('Error parsing URL')

def decodev2 (rewrittenurl):
	match = re.search(r'u=(.+?)&[dc]=',rewrittenurl)
	if match:
		specialencodedurl = match.group(1)
		trans = str.maketrans('-_', '%/')
		urlencodedurl = specialencodedurl.translate(trans)
		htmlencodedurl = urllib.parse.unquote(urlencodedurl)
		url = html.parser.HTMLParser().unescape(htmlencodedurl)
		return url
	else:
		print('Error parsing URL')


#url_ = 'https://urldefense.proofpoint.com/v2/url?u=https-3A__service.eu.sumologic.com_ui_index.html-23section_search_xvPtwie1Snlbd9vYkgPHebXkUm8PpwsPKs6DOUky5mI04CiEOdKZaXkoLCfdzySXKfDB602xM1oRmgmE726Kp5yYMG5E9UTqEYXQc3kZoFJUmla4lBXKfP7uJK9nY9c4&d=DwMCaQ&c=xbbKDa1CXQMejoORxEnUuQ&r=dkcyV7hK1wj1G_xz3JegRYfDtz_Z7IPnsv-8KHOLGsRaSfl__oKRBDa1bC1RfsTP&m=dqEoGgsX4bqczDURxlkljl0F5VN1rWHWfqt5Tnk46G0&s=OUPqMb9v5PC1OozczrnILyKMu6SXUytbGoWkyLThKPc&e='

#open('o.txt','w').write(rewrittenurl(url_))
