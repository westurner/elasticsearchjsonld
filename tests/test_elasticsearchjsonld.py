#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_elasticsearchjsonld
----------------------------------

Tests for `elasticsearchjsonld` module.
"""

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

import os
import unittest

from elasticsearchjsonld import elasticsearchjsonld

here = os.path.dirname(os.path.abspath(__file__))


class TestElasticsearchjsonld(unittest.TestCase):

    def setUp(self):
        pass

    def test_01_esjson2jsonld(self):
        input_ = os.path.join(here, 'openfda-schemas', 'faers_mapping.json')
        with open(input_) as f:
            print("INPUT\n=================")
            print(f.read())
        output = StringIO()
        output = elasticsearchjsonld.esjson2jsonld(input_, vocab='http://openfda/faers#', output=output)
        output.seek(0)
        print("OUTPUT\n=================")
        print(output.read())
        raise Exception()  # XXX: testing with ipdbplugin

    # def test_02_esjson2jsonld(self):
        # INPUTS = [
            #'faers_mapping.json',
            #'maude_mapping.json',
            #'res_mapping.json',
            #'spl_mapping.json']

        # for input_ in INPUTS:
            #output = StringIO()
            #elasticsearchjsonld.esjson2jsonld(input_, output)
            # output.seek(0)
            # print(output.read())

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
