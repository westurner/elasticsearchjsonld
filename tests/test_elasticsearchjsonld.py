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
        input_ = 'faers_mapping.json'
        vocab = 'http://openfda/%s#' % input_.rstrip('.json')
        input_ = os.path.join(here, 'openfda-schemas', input_)
        with open(input_) as f:
            print("INPUT\n=================")
            print(f.read())
        output = StringIO()
        output = elasticsearchjsonld.esjson2jsonld(
            input_,
            vocab=vocab,
            output=output)
        output.seek(0)
        print("OUTPUT\n=================")
        jsonstr = output.read()
        print(jsonstr)
        self.assertTrue(jsonstr)

        # TODO: import PyLD // rdflib-jsonld and verify
        # XXX TODO: real assertions

    def test_02_esjson2jsonld(self):
        INPUTS = [
            'faers_mapping.json',
            'maude_mapping.json',
            'res_mapping.json',
            'spl_mapping.json']

        for input_ in INPUTS:
            vocab = 'http://openfda/%s#' % input_.rstrip('.json')
            input_ = os.path.join(here, 'openfda-schemas', input_)
            with open(input_) as f:
                print("INPUT\n=================")
                print(f.read())
            output = StringIO()
            elasticsearchjsonld.esjson2jsonld(
                input_,
                vocab=vocab,
                output=output)
            output.seek(0)
            print("OUTPUT\n=================")
            jsonstr = output.read()
            print(jsonstr)
            self.assertTrue(jsonstr)

            # TODO: import PyLD // rdflib-jsonld and verify
            # XXX TODO: real assertions

        # raise Exception()  # XXX: testing with ipdbplugin

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
