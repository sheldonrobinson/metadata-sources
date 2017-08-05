#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#
# IEEEXplore - IEEEXplore metadata plugin for calibre
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

from __future__ import (unicode_literals, division)

import time
import re

from .mysource import MySource
from .netbib.ieeexplore import IEEEXplore as IEEEXploreWorker

from calibre.ebooks.metadata.sources.base import Option
from calibre.ebooks.metadata.book.base import Metadata

class IEEEXplore(MySource):
    name                    = 'IEEEXplore'
    description             = _('Downloads metadata from IEEEXplore')
    author                  = 'Sheldon Robinson'
    supported_platforms     = ['windows', 'osx', 'linux']
    version                 = (1,3,0)
    minimum_calibre_version = (1,0,0)

    capabilities = frozenset(['identify'])
    touched_fields = frozenset(['identifier:arnumber','identifier:isbn','identifier:doi','identifier:isbn',
                                'title', 'authors', 'comments', 'publisher','languages',
                                'pubdate', 'series', 'series_index', 'tags'])


    # Plugin Options
    has_html_comments = True
    supports_gzip_transfer_encoding = False

    # My Options
    idkey = 'arnumber'
    maxresults = 1
    sleep_time = 0.5
    worker_class = IEEEXploreWorker
    abstract_title = "Abstract:"



# vim: expandtab:shiftwidth=4:tabstop=4:softtabstop=4:textwidth=80
