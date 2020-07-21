import requests
from dotenv import load_dotenv
import os

load_dotenv()

# app = Flask(__name__)

def pretty_print_request(request):
    print('\n{}\n{}\n\n{}\n\n{}\n'.format(
        '-----------Request----------->',
        request.method + ' ' + request.url,
        '\n'.join('{}: {}'.format(k, v) for k, v in request.headers.items()),
        request.body)
    )


def pretty_print_response(response):
    print('\n{}\n{}\n\n{}\n\n{}\n'.format(
        '<-----------Response-----------',
        'Status code:' + str(response.status_code),
        '\n'.join('{}: {}'.format(k, v) for k, v in response.headers.items()),
        response.text)
    )


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
