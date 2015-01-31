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


# http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/mapping-types.html
# http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/mapping-core-types.html
ESTYPE_JSONLDTYPE_MAP = {
    'string': 'xsd:string',

    'date': 'xsd:date',   # UTC

    # number
    'float': 'xsd:float',
    'double': 'xsd:double',
    'byte': 'xsd:byte',
    'short': 'xsd:short',
    'long': 'xsd:long',

    'boolean': 'xsd:boolean',
    'binary': 'xsd:base64Binary',
    'attachment': 'xsd:base64Binary',
}


def walk_esjson_mappings(tree, context, depth=0, vocab=None):
    if hasattr(tree, 'items'):
        for key, value in tree.items():
            print(('  ' * depth, key, value and str(value)[0:20]))
            if value is None:
                continue
            elif hasattr(value, 'items') and u'properties' in value:
                context[key] = collections.OrderedDict()
                ctxt = context[key]
                walk_esjson_mappings(value, ctxt, depth=depth + 1, vocab=vocab)
            elif key == u'properties':
                walk_esjson_mappings(value, context, depth=depth + 1, vocab=vocab)
            else:
                context[key] = collections.OrderedDict()
                ctxt = context[key]
                ctxt['@id'] = '%s%s' % (vocab or '', key)  # XXX

                estype = value.get('type')
                if estype == 'multi_field':
                    esfieldtypes = []
                    for key, value in value['fields'].items():
                        esfieldtypes.append(value.get('type'))
                    if len(set(esfieldtypes)) > 1:
                        # TODO: pick the 'not_analyzed' copy?
                        raise NotImplementedError(esfieldtypes)
                    jsonldtype = ESTYPE_JSONLDTYPE_MAP.get(esfieldtypes[0])
                else:
                    jsonldtype = ESTYPE_JSONLDTYPE_MAP.get(estype)
                    if jsonldtype is None:
                        raise NotImplementedError("ElasticSearch %r type not yet implemented" % estype)
                ctxt['@type'] = jsonldtype
            # TODO: 'lists': http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/mapping-array-type.html
            # TODO: type=object: http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/mapping-object-type.html
            # TODO: type=nested: http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/mapping-nested-type.html
            # TODO: type=ip: http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/mapping-ip-type.html
            # TODO: type=geo_point: http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/mapping-geo-point-type.html
            # TODO: type=geo_shape: http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/mapping-geo-shape-type.html
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
