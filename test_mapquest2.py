import mapquest2
import pytest
import requests


@pytest.fixture
def json_data():
    json_data, json_status = mapquest2.urlEncode('Washington, D.C.', 'Baltimore, Md', 'fastest', 'normal')
    
    return json_data

class MockResponse:
    @staticmethod
    def json():
        return {
            'info': {
                'statuscode' : 0
            }
        }

def test_welcomeScreen(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: 1)
    
    assert type(mapquest2.welcomeScreen()) is int

def test_getParameters(mocker):
    mocker.patch('builtins.input', side_effect=['Washington, D.C.', 'Baltimore, Md', 'fastest', 'normal'])
    
    assert mapquest2.getParameters()
    

def test_displayOptions(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: 1)
    
    assert type(mapquest2.displayOptions()) is int

def test_urlEncode_one(monkeypatch):
    def mock_get(*args, **kwargs):
        return MockResponse()
    
    monkeypatch.setattr(requests, 'get', mock_get)
    
    json_data, json_status = mapquest2.urlEncode('Washington, D.C.', 'Baltimore, Md', 'fastest', 'normal')
    
    assert json_status == 0
    
def test_statusIsValid_one():
    assert mapquest2.statusIsValid(0) is True

def test_statusIsValid_two():
    assert mapquest2.statusIsValid(402) is False

def test_statusIsValid_three():
    assert mapquest2.statusIsValid(611) is False

def test_statusIsValid_four():
    assert mapquest2.statusIsValid(123) is False
    
def test_displayData_one(json_data, capsys):
    mapquest2.displayData('Washington, D.C.', 'Baltimore, Md', json_data, 1)
    
    captured = capsys.readouterr()
    assert "Trip Duration" in captured.out

def test_displayData_two(json_data, capsys):
    mapquest2.displayData('Washington, D.C.', 'Baltimore, Md', json_data, 2)
    
    captured = capsys.readouterr()
    
    assert "Distance Travelled" in captured.out

def test_displayData_three(json_data, capsys):
    mapquest2.displayData('Washington, D.C.', 'Baltimore, Md', json_data, 3)
    
    captured = capsys.readouterr()
    
    assert "Directions" in captured.out
    
def test_displayData_four(json_data, capsys):
    mapquest2.displayData('Washington, D.C.', 'Baltimore, Md', json_data, 4)
    
    captured = capsys.readouterr()
    
    print(captured.out)
    
    assert "Directions from" in captured.out

def test_displayData_five(json_data):
    try:
        mapquest2.displayData('Washington, D.C.', 'Baltimore, Md', json_data, 5)
    except SystemExit:
        assert True

def test_settings_one(mocker, capsys):    
    mocker.patch('builtins.input', side_effect = [1,1,2])
    
    mapquest2.settings()
    captured = capsys.readouterr()
    
    assert 'Settings updated' in captured.out

def test_settings_two(mocker, capsys):
    mocker.patch('builtins.input', side_effect = [1,2,2])
    
    mapquest2.settings()
    captured = capsys.readouterr()
    
    assert 'Settings updated' in captured.out

def test_settings_three(monkeypatch):    
    monkeypatch.setattr('builtins.input', lambda _: 2)
    
    assert mapquest2.settings() is None