import unittest
import pytest
import os
import tempfile
from main import app

from flask import Flask
from flask_login import UserMixin, login_user, login_required, logout_user, LoginManager
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, RadioField
from wtforms.fields.html5 import EmailField
from wtforms.validators import InputRequired, Email, Length



class MyTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        # dsn = "dbname='" + "SOEN341" + "' user='" + "postgres" + "' host='localhost' password='" + "000Poda19996934*" + "'"
        # dbConn = psycopg2.connect(dsn)
        # self.postgresql = psycopg2.connect(dsn)
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


if __name__ == '__main__':
    unittest.main()
