#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# netbib - collect bibliographical data over the net
# Copyright 2012 Abdó Roig-Maranges <abdo.roig@gmail.com>
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import (unicode_literals, division, priint_function)

import time
import sys
import re
import xml.etree.ElementTree

if sys.version_info[0] >= 3:
    from urllib.parse import urlencode
else:
    from urllib import urlencode

import unicodedata

from .utils import surname, strip_accents
from .base import NetbibBase, NetbibError



class IEEEXploreError(NetbibError):
    pass


class IEEEXplore(NetbibBase):
    def __init__(self, browser, timeout=30):
        super(IEEEXplore, self).__init__()
	print('Comlete super init ...')
        self.query_maxresults = 100

        self.search_fields = ['title', 'authors', 'id']
        self.idkey = 'an'

        self.timeout = timeout
        self.browser = browser
        self.sleep_time = 0.2

        self.ieeexplore_url = "http://ieeexplore.ieee.org/gateway/ipsSearch.jsp"
        self.ans = []
	
	print('Comleted __init__  ...')


    # Internals
    # ------------------------------ #

    def get_matches(self, params):
	print('Entered get_matches  ...')
        query_url = '%s?%s' % (self.ieeexplore_url, urlencode(params))
        raw = self.browser.open(query_url, timeout=self.timeout).read().strip()
        rawdata = raw.decode('utf-8', errors='replace')
        xmldata = xml.etree.ElementTree.fromstring(rawdata)
        entries = xmldata.findall("document")

        ans = []
        for result in entries:
            d = {}
            d['id'] = result.find('arnumber').text
	    if result.find('isbn') is not None: d['isbn'] = result.find('isbn').text
	    if result.find('issn') is not None: d['issn'] = result.find('issn').text
	    if result.find('doi') is not None: d['doi'] = result.find('doi').text
            d['title'] = self.format_title(result.find('title').text)
            d['authors'] = [self.format_text(e.text) for e in result.find('authors').text.split(';')]
            d['subject'] = [self.format_text(e.text) for e in [result.findall('controlledterms/term'), result.findall('thesaurusterms/term')]]
	    if result.find('pubtitle') is not None:  d['series'] = self.format_text(result.find('pubtitle').text)
	    if result.find('py') is not None: d['year'] = self.format_text(result.find('py').text)
	    if result.find('publisher') is not None: d['publisher'] = self.format_text(result.find('publisher').text)
	    if result.find('volume') is not None: d['volume'] = self.format_text(result.find('volume').text)
	    if result.find('issue') is not None: d['number'] = self.format_text(result.find('issue').text) 
            d['abstract'] = '<p>%s</p>' % self.format_text(result.find('abstract').text)
            if result.find('mdurl') is not None: d['url'] = self.format_url(result.find('mdurl').text)
	    

            ans.append(d)

	print('Exiting get_matches  ...')
        return ans


    def get_item(self, bibid):
        params = self.format_query({'id': bibid})
        ans = self.get_matches(params)

        if len(ans) > 0:
            return ans[0]

        return None

    def get_abstract(self, bibid):
        ans = self.get_item(bibid)

        if 'abstract' in ans:
            return ans['abstract']

        return None


    def format_query(self, d, lax=False):
        """Formats a query suitable to send to the IEEEXplore API"""
        for k in d.keys():
            if not k in self.search_fields:
                raise IEEEXploreError("Error in IEEEXplore. Don't understand key: %s" % k)

        if 'id' in d.keys():
            params = {'an': d['id']}
            return params

	elif 'isbn' in d.keys():
            params = {'isbn': d['isbn']}
            return params

	elif 'issn' in d.keys():
            params = {'issn': d['issn']}
            return params

	elif 'doi' in d.keys():
            params = {'doi': d['doi']}
            return params

        elif 'title' in d.keys() or 'authors' in d.keys():
            items = []
            if 'title' in d.keys():
                if lax:
                    words = d['title'].split(' ')
                    for b in words: items.append('ti:' + self.clean_query(b))
                else:
                    items.append('ti:' + ('"%s"' % self.clean_query(d['title'])))

            if 'authors' in d.keys():
                words = [surname(a) for a in d['authors']]
                for b in words: items.append('au:' + self.clean_query(b))

            params = {items,
                      'rs': 1,
                      'bc': str(self.query_maxresults)}
            return params

        else:
            raise IEEEXploreError("Error in IEEEXplore. Insuficient metadata to construct a query")
            return None


