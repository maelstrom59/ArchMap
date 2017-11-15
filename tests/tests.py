#!/usr/bin/env python3
import logging
import os
import pickle
import unittest

import archmap


archmap.log.setLevel(logging.CRITICAL)


class WikiParserTestCase(unittest.TestCase):
    """These tests test the wiki parser in the get_users() function
    """

    # 'ArchMap_List-stripped.html' is a stripped down page of HTML
    # including the tags needed for parsing and some test data
    wiki_html = 'tests/ArchMap_List-stripped.html'

    # 'raw_users.txt' contains the extracted list from 'ArchMap_List-stripped.html'
    # The trailing newline needs to be stripped to match the output from 'get_users'
    with open('tests/raw_users.txt', 'r') as raw_users:
        raw_users = raw_users.read().rstrip('\n')

    def setUp(self):
        # Set 'maxDiff' to 'None' to be able to see long diffs when something goes wrong.
        self.maxDiff = None

    def test_wiki_parser(self):
        output_get_users = archmap.get_users(local=self.wiki_html)
        self.assertEqual(self.raw_users, output_get_users)


class ListParserTestCase(unittest.TestCase):
    """These tests test that the list parser is working correctly
    """

    # 'raw_users.txt' contains an unformatted 'raw' sample list
    with open('tests/raw_users.txt', 'r') as raw_users_file:
        raw_users = raw_users_file.read()

    # 'sample_users.txt' contains a formatted sample list equivilent to the raw version above
    with open('tests/sample-archmap_users.txt', 'r') as sample_users_file:
        sample_users = sample_users_file.read()

    # 'sample_parsed_users.pickle' is a pickled list that was generated with a known good list
    # ('get_users' was run on 'sample_users.txt' and the output was pickled)
    with open('tests/sample_parsed_users.pickle', 'rb') as pickled_input:
        sample_parsed_users = pickle.load(pickled_input)

    def setUp(self):
        # Set 'maxDiff' to 'None' to be able to see long diffs when something goes wrong.
        self.maxDiff = None

    def test_list_parser_raw(self):
        parsed_raw_users = archmap.parse_users(self.raw_users)
        self.assertEqual(parsed_raw_users, self.sample_parsed_users)

    def test_list_parser_cleaned(self):
        parsed_cleaned_users = archmap.parse_users(self.sample_users)
        self.assertEqual(parsed_cleaned_users, self.sample_parsed_users)


class OutputTestCase(unittest.TestCase):
    """These tests compare the output of ``make_geojson()``, ``make_kml()``  and ``make csv()``
    with pre-generated versions that have been checked manually, these *sample* files were
    generated by runing ``archmap.py`` on the stripped-down/handmade ``ArchMap_List-stripped.html'``.
    """

    # 'sample_parsed_users.pickle' is a pickled list that was generated with a known good list
    # ('get_users' was run on 'sample_users.txt' and the output was pickled)
    with open('tests/sample_parsed_users.pickle', 'rb') as pickled_input:
        parsed_users = pickle.load(pickled_input)

    def setUp(self):
        self.sample_users = 'tests/sample-archmap_users.txt'
        self.output_users = 'tests/output-archmap_users.txt'
        self.sample_pretty_users = 'tests/sample-archmap_pretty_users.txt'
        self.output_pretty_users = 'tests/output-archmap_pretty_users.txt'
        self.sample_geojson = 'tests/sample-archmap.geojson'
        self.output_geojson = 'tests/output-archmap.geojson'
        self.sample_kml = 'tests/sample-archmap.kml'
        self.output_kml = 'tests/output-archmap.kml'
        self.sample_csv = 'tests/sample-archmap.csv'
        self.output_csv = 'tests/output-archmap.csv'

        # Set 'maxDiff' to 'None' to be able to see long diffs when something goes wrong.
        self.maxDiff = None

    def tearDown(self):
        try:
            os.remove(self.output_users)
            os.remove(self.output_pretty_users)
            os.remove(self.output_geojson)
            os.remove(self.output_kml)
            os.remove(self.output_csv)
        except FileNotFoundError:
            pass

    def test_users(self):
        archmap.make_users(self.parsed_users, self.output_users)

        with open(self.sample_users, 'r') as file:
            sample_users = file.read()
        with open(self.output_users, 'r') as file:
            output_users = file.read()

        self.assertEqual(sample_users, output_users)

    def test_pretty_users(self):
        archmap.make_users(self.parsed_users, self.output_pretty_users, pretty=True)

        with open(self.sample_pretty_users, 'r') as file:
            sample_pretty_users = file.read()
        with open(self.output_pretty_users, 'r') as file:
            output_pretty_users = file.read()

        self.assertEqual(sample_pretty_users, output_pretty_users)

    def test_geojson(self):
        archmap.make_geojson(self.parsed_users, self.output_geojson)

        with open(self.sample_geojson, 'r') as file:
            sample_geojson = file.read()
        with open(self.output_geojson, 'r') as file:
            output_geojson = file.read()

        self.assertEqual(sample_geojson, output_geojson)

    def test_kml(self):
        archmap.make_kml(self.parsed_users, self.output_kml)

        with open(self.sample_kml, 'r') as file:
            sample_kml = file.read()
        with open(self.output_kml, 'r') as file:
            output_kml = file.read()

        self.assertEqual(sample_kml, output_kml)

    def test_csv(self):
        archmap.make_csv(self.parsed_users, self.output_csv)

        with open(self.sample_csv, 'r') as file:
            sample_csv = file.read()
        with open(self.output_csv, 'r') as file:
            output_csv = file.read()

        self.assertEqual(sample_csv, output_csv)


if __name__ == '__main__':
    unittest.main()
