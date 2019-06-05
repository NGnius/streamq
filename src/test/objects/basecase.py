import unittest
import os
from ...main.repo import gherkin

TEST_DATABASE = './streamq_test.db'
gherkin.set_db(TEST_DATABASE)

class BaseCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass
