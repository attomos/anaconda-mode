import test.helper

from unittest import TestCase
from start_jedi import jedi
import os


class TestJedi(TestCase):

    def test_unsupported_command(self):
        """Should raise exception on adjective command requests."""

        request = {
            'command': 'some_strange_command',
            'attributes': {
                'source': '''\nimport datetime\ndatetime.da''',
                'line': 3,
                'column': 14,
                'path': ''
            }
        }

        self.assertRaises(jedi.AdjectiveOperation, jedi.process, **request)

    def test_missing_attributes(self):
        """Should raise exception on incomplete source code."""

        request = {
            'command': 'candidates',
            'attributes': {}
        }

        self.assertRaises(jedi.MissingSource, jedi.process, **request)

    def test_autocomplete(self):
        """Jedi must complete correct sources."""

        request = {
            'command': 'candidates',
            'attributes': {
                'source': '''\nimport datetime\ndatetime.da''',
                'line': 3,
                'column': 14,
                'path': ''
            }
        }

        response = ['date', 'datetime', 'datetime_CAPI']

        self.assertEqual(response, jedi.process(**request))

    def test_definition_search(self):
        """Jedi must find correct definitions."""

        request = {
            'command': 'location',
            'attributes': {
                'source': '''
def my_func():
    print 'called'

alias = my_func
my_list = [1, None, alias]
inception = my_list[2]

inception()''',
                'line': 9,
                'column': 1,
                'path': 'example.py'
            }
        }

        response = [{
            'module_path': os.getcwd() + '/example.py',
            'line': 7,
            'column': 0
        }]

        self.assertEqual(response, jedi.process(**request))