import json
import unittest
from types import SimpleNamespace

import psycopg2
import pytest
import os
import tempfile
import testing.postgresql

from main import app



TEST_DB = 'test.db'


class MyTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        dsn = "dbname='" + "d31l1458rvtpdh" + "' user='" + "bawfkbhotaauai" + "' host='ec2-44-193-111-218.compute-1.amazonaws.com' password='" + "4498aa8d9bf9269256f361238ead8e6a431f0882fd393693fd8e38655f484ca3" + "'"
        dbConn = psycopg2.connect(dsn)
        self.postgresql = psycopg2.connect(dsn)
        self.app = app.test_client()

    # executed after each test
    def tearDown(self):
        pass

    # self.postgresql.stop()

    ###############
    #### tests ####
    ###############

    def test_main_page(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def login(self, username, password):
        return self.app.post(
            '/login',
            data=dict(User_Name=username, Password=password),
            follow_redirects=True
        )

    def test_valid_user_registration(self):
        response = self.login('youngpanawan', '12345678')
        self.assertEqual(response.status_code, 200)
        self.assertIn("Logged in", response.headers['message'])


if __name__ == '__main__':
    unittest.main()
