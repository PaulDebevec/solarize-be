from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from unittest import TestCase
from app import app
from sqlalchemy import create_engine
import config
import requests
import os
load_dotenv()


class TestApplication(TestCase):

    app = Flask(__name__)
    os.environ["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres@localhost/solarizer_test"
    engine = create_engine(os.getenv("SQLALCHEMY_DATABASE_URI"))
    TESTING = True
    db = SQLAlchemy(app)


    def setUp(self):
        self.app.config_app('testing')
        app.config.from_object("app_config.testing")
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()


    def test_one_equals_one():
        a = 1
        b = 1
        assert a == b


    def test_get_nrel_request_and_response():
        url = f"https://developer.nrel.gov/api/pvwatts/v6.json?api_key={os.getenv('NREL_API_KEY')}&address=155+beryl+way+broomfield&system_capacity=4&azimuth=180&tilt=40&array_type=1&module_type=1&losses=10"

        response = requests.get(url)

        assert response.status_code == 200
        response_body = response.json()

        # Verify input parameters
        assert response_body["inputs"]["address"] == '155 beryl way broomfield'
        assert response_body["inputs"]["system_capacity"] == '4'
        assert response_body["inputs"]["azimuth"] == '180'
        assert response_body["inputs"]["tilt"] == '40'
        assert response_body["inputs"]["array_type"] == '1'
        assert response_body["inputs"]["module_type"] == '1'
        assert response_body["inputs"]["losses"] == '10'

        # Verify output values
        assert response_body["outputs"]["solrad_annual"] == 5.62701940536499
        assert response_body["outputs"]["solrad_monthly"][0] == 4.519073009490967
        assert response_body["outputs"]["solrad_monthly"][1] == 5.297043800354004
        assert response_body["outputs"]["solrad_monthly"][2] == 5.921163558959961
        assert response_body["outputs"]["ac_annual"] == 6605.365234375
        assert response_body["outputs"]["ac_monthly"][0] == 479.64813232421875
        assert response_body["outputs"]["ac_monthly"][1] == 493.1632385253906
        assert response_body["outputs"]["ac_monthly"][2] == 599.2940673828125


    def test_eco_tips(setUp):
        tip1 = EcoTip("Hello Tip Test 1")
        tip2 = EcoTip("Tip Test 2")
        db.session.add(tip1)
        db.session.add(tip2)
        db.session.commit()