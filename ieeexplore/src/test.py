#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# mathscinet - mathscinet metadata plugin for calibre
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

from __future__ import (unicode_literals, division, print_function)


# Tests
# To run these test use:
# calibre-debug -e test.py

if __name__ == '__main__':
    from calibre.ebooks.metadata.sources.test import (test_identify_plugin,
         title_test, authors_test)

    tests_list = [
        ({'identifiers': {"an" : "5318908"}},
         [title_test("A 2D Barcode-Based Mobile Payment System"),
          authors_test(['Jerry Gao', 'Vijay Kulkarni', 'Himanshu Ranavat', 'Lee Chang', 'Hsing Mei'])]),

        ({'title': "A 2D Barcode-Based Mobile Payment System", 'authors':['Jerry Gao']},
        [title_test("A 2D Barcode-Based Mobile Payment System", exact=True)])

        ]

    test_identify_plugin("IEEEXplore", tests_list)


# vim: expandtab:shiftwidth=4:tabstop=4:softtabstop=4:textwidth=80
