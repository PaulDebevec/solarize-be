import requests

def pretty_print_request(request):
    print( '\n{}\n{}\n\n{}\n\n{}\n'.format(
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

    url = "https://developer.nrel.gov/api/pvwatts/v6.json?api_key=ACywfpUB7wmEqVhJiIyhX7QV6bOZidNARR1Cm6Ot&address=155+beryl+way+broomfield&system_capacity=4&azimuth=180&tilt=40&array_type=1&module_type=1&losses=10"

    response = requests.get(url)

    assert response.status_code == 200
    response_body = response.json()

    assert response_body["inputs"]["address"] == '155 beryl way broomfield'
    assert response_body["inputs"]["system_capacity"] == '4'
    assert response_body["inputs"]["azimuth"] == '180'
    assert response_body["inputs"]["tilt"] == '40'
    assert response_body["inputs"]["array_type"] == '1'
    assert response_body["inputs"]["module_type"] == '1'
    assert response_body["inputs"]["losses"] == '10'

    # pretty_print_request(response.request)
    # pretty_print_response(response)
