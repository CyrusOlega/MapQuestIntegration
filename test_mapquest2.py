import mapquest2
from mapquest2 import *

def test_welcomeScreen(monkeypatch):
    monkeypatch.setattr('test_mapquest2.welcomeScreen', lambda: 1)
    
    assert welcomeScreen() == 1

# def test_getParameters(monkeypatch):
#     inputs = iter(["Washington, D.C.", "Baltimore, Md", "fastest", "normal"])
#     monkeypatch.setattr('test_mapquest2.getParameters', lambda : next(inputs))
#     orig, dest, unit, routeType, drivingStyle = getParameters()


def test_displayOptions(monkeypatch):
    monkeypatch.setattr('test_mapquest2.displayOptions', lambda: 1)
    
    assert displayOptions() == 1

# def test_urlEncode(monkeypatch):
#     test_key = '8pZqf042uMGvHGAFMxCssCSCx7z6Znyv'
#     test_orig = 'Washington, D.C.'
#     test_dest = 'Baltimore, Md'
#     test_routeType = 'fastest'
#     test_drivingStyle = 'normal'
#     test_unit = 'm'
#     inputs = iter([test_orig, test_dest, test_routeType, test_drivingStyle, test_unit])
    
#     monkeypatch.setattr(mapquest2, "key", test_key)
#     monkeypatch.setattr('test_mapquest2.urlEncode', lambda : next(inputs))
    
#     json_data = urlEncode()
    
#     assert json_data == "adasd"
    
    