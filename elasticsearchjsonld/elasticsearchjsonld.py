#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
"""
esjson2jsonld

Convert ElasticSearch JSON mappings to a JSON-LD @context
"""
import collections
import codecs
import json
import logging
import optparse
import sys


def walk_esjson_mappings(tree, context, depth=0, vocab=None):
    if hasattr(tree, 'items'):
        for key, value in tree.items():
            print(('  ' * depth, key, value and str(value)[0:20]))
            if value is None:
                continue
            elif hasattr(value, 'items') and u'properties' in value:
                context[key] = collections.OrderedDict()
                ctxt = context[key]
                walk_esjson_mappings(value, ctxt, depth + 1)
            elif key == u'properties':
                walk_esjson_mappings(value, context, depth + 1)
            else:
                context[key] = collections.OrderedDict()
                ctxt = context[key]
                ctxt['@id'] = '%s%s' % (vocab or '', key)  # XXX
                ctxt['@type'] = '@id'     # XXX
    else:
        raise Exception("HERE")


def esjson2jsonld(esjson, vocab=None, default_vocab=None, output=None):
    """
    Generate a JSON-LD context from ElasticSearch JSON

    Arguments:
        esjson (str): path to an ElasticSearch JSON file

    Keyword Arguments:
        vocab (str): default @vocab URI (default: None)
        output (.write()-able): object to write output to

    Returns:
        output: output object
    """
    if output is None:
        output = sys.stdout

    with codecs.open(esjson, 'r', encoding='utf8') as f:
        esm = json.load(f, object_pairs_hook=collections.OrderedDict)

    #key, value = esm.items()[0]
    #raise Exception(type(value), value)
    value = esm.values()[0]['properties']

    context = collections.OrderedDict()
    context['@context'] = collections.OrderedDict()
    ctxt = context['@context']

    # define a default vocabulary
    if default_vocab:
        if default_vocab is not None:
            ctxt['@vocab'] = default_vocab

    walk_esjson_mappings(value, ctxt, vocab=vocab)

    output.write(json.dumps(context, indent=2))  # XXX
    return output


def main(args=None):

    prs = optparse.OptionParser(usage="%prog : args")

    prs.add_option('-v', '--verbose',
                   dest='verbose',
                   action='store_true',)
    prs.add_option('-q', '--quiet',
                   dest='quiet',
                   action='store_true',)
    prs.add_option('-t', '--test',
                   dest='run_tests',
                   action='store_true',)

    if args is None:
        args = sys.argv
    (opts, args) = prs.parse_args(args=args)

    if not opts.quiet:
        logging.basicConfig()

        if opts.verbose:
            logging.getLogger().setLevel(logging.DEBUG)

    if opts.run_tests:
        import sys
        sys.argv = [sys.argv[0]] + args
        import unittest
        exit(unittest.main())

    esjson2jsonld()

if __name__ == "__main__":
    main()
