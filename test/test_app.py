from flask import Flask, request, jsonify
from app import NREL
from dotenv import load_dotenv
import requests
import os
load_dotenv()

    
def test_one_equals_one():
    a = 1
    b = 1
    assert a == b
    
    
def test_get_system_info():
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


def test_all_functions():
    fe_json = {
          "solarizer_parameters": {
            "name": "example request",
            "address": "1490+Delgany+St+Denver+CO+80202",
            "system_capacity": 4,
            "module_type": 0,
            "array_type": 0,
            "losses": 14,
            "tilt": 20,
            "azimuth": 180
          },
          "historical_kWh": {
            "january": 100,
            "february": 100,
            "march": 100,
            "april": 100,
            "may": 100,
            "june": 100,
            "july": 100,
            "august": 100,
            "september": 100,
            "october": 100,
            "november": 100,
            "december": 100
          }
        }
    results = NREL(fe_json)
    results.get_system_info()
    kwh_rate_info = results.get_kwh_rate_info()
    results.calculate_value(kwh_rate_info)
    assert results.monthly_values["value_monthly"] == [
        43.872415115356446,
        47.50345698547363,
        63.055829528808594,
        66.16632629394532,
        67.38588641357421,
        67.31052465820312,
        66.28732055664062,
        64.52443954467773,
        60.22124554443359,
        53.6966434173584,
        45.53072444152832,
        40.525810928344725
    ]
    assert len(results.monthly_values["value_monthly"]) == 12
    assert type(results.monthly_values["value_monthly"][0]) == float

    results.calculate_offset()
    assert results.percent_offset["percent_offset"] == 517.4062016805012


def test_calculate_offset_returns_empty_string():
    fe_json = {
        "solarizer_parameters": {
            "name": "example request",
            "address": "1490+Delgany+St+Denver+CO+80202",
            "system_capacity": 4,
            "module_type": 0,
            "array_type": 0,
            "losses": 14,
            "tilt": 20,
            "azimuth": 180
        },
        "historical_kWh": {
            "january": "undefined",
            "february": 100,
            "march": 100,
            "april": 100,
            "may": 100,
            "june": 100,
            "july": 100,
            "august": 100,
            "september": 100,
            "october": 100,
            "november": 100,
            "december": 100
        }
    }
    results = NREL(fe_json)
    results.get_system_info()
    results.calculate_offset()
    assert results.percent_offset["percent_offset"] == ""
