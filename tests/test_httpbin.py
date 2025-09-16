import pytest
import requests
import xml.etree.ElementTree as ET
import uuid
from utilities.helpers import Helpers

helpers = Helpers()
base_url = helpers.config['base_url']

@helpers.retry()
def make_request(method, endpoint, **kwargs):
    url = base_url + endpoint
    response = requests.request(method, url, **kwargs)
    response.raise_for_status()  # Raise exception for non-2xx status
    return response

@pytest.mark.allure_description("Test JSON response format")
def test_response_format_json():
    resp = make_request('GET', '/json')
    assert resp.status_code == 200
    assert resp.headers['Content-Type'] == 'application/json'
    data = resp.json()
    assert isinstance(data, dict)
    assert 'slideshow' in data

@pytest.mark.allure_description("Test XML response format")
def test_response_format_xml():
    resp = make_request('GET', '/xml')
    assert resp.status_code == 200
    assert 'xml' in resp.headers['Content-Type']
    ET.fromstring(resp.text)  # Validates XML parsing

@pytest.mark.allure_description("Test HTML response format")
def test_response_format_html():
    resp = make_request('GET', '/html')
    assert resp.status_code == 200
    assert 'html' in resp.headers['Content-Type']
    assert '<html>' in resp.text.lower()

@pytest.mark.allure_description("Test request inspection with query params")
def test_request_inspection_params():
    params = helpers.generate_random_query_params()
    resp = make_request('GET', '/get', params=params)
    assert resp.status_code == 200
    assert resp.json()['args'] == params

@pytest.mark.allure_description("Test request inspection with headers")
def test_request_inspection_headers():
    headers = helpers.generate_random_headers()
    resp = make_request('GET', '/headers', headers=headers)
    assert resp.status_code == 200
    resp_headers = resp.json()['headers']
    assert resp_headers['Custom-Header'] == headers['Custom-Header']
    assert resp_headers['User-Agent'] == headers['User-Agent']

@pytest.mark.allure_description("Test request inspection with user-agent")
def test_request_inspection_user_agent():
    user_agent = helpers.fake.user_agent()
    headers = {'User-Agent': user_agent}
    resp = make_request('GET', '/user-agent', headers=headers)
    assert resp.status_code == 200
    assert resp.json()['user-agent'] == user_agent

@pytest.mark.allure_description("Test dynamic data with UUID")
def test_dynamic_data_uuid():
    resp = make_request('GET', '/uuid')
    assert resp.status_code == 200
    uuid_str = resp.json()['uuid']
    uuid.UUID(uuid_str)  # Validates UUID format

@pytest.mark.allure_description("Test dynamic data with delay")
def test_dynamic_data_delay():
    resp = make_request('GET', '/delay/2')  # 2-second delay
    assert resp.status_code == 200
    assert 'origin' in resp.json()

@pytest.mark.allure_description("Test dynamic data with POST")
def test_dynamic_data_post():
    data = helpers.generate_random_json_data()
    resp = make_request('POST', '/post', json=data)
    assert resp.status_code == 200
    assert resp.json()['json'] == data