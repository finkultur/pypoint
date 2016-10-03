import unittest

import pypoint.pypoint

class TestDevices(unittest.TestCase):
    """
    Tests the /devices endpoint.
    Since the demo device does not seem to record
    temperature/humidity/pressure, this is tested with an actual Point.
    """
    def setUp(self):
        self.point = pypoint.pypoint.Point('credentials.cfg')

    def tearDown(self):
        pass

    def test_temp(self):
        temp = self.point.get_latest_temperature()['value']
        self.assertTrue(-50.0 < temp < 50.0)

    def test_hum(self):
        hum = self.point.get_latest_humidity()['value']
        self.assertTrue(0.0 <= hum <= 100.0)

    def test_pressure(self):
        pressure = self.point.get_latest_pressure()['value']
        print(pressure)
        min_pressure = 245 # Top at mt everest at -30C (hPA)
        max_pressure = 1075 # Bottom of Dead Sea Shore at -30C (hPa)
        self.assertTrue(min_pressure <= pressure <= max_pressure)
        
class TestUsers(unittest.TestCase):
    def setUp(self):
        self.point = pypoint.pypoint.Point('demo_credentials.cfg')
    
    def tearDown(self):
        pass

    def test_user_id(self):
        user_id = self.point.get_user_id()
        demo_id = '5613e07fb428c6b005514de1' # Might be subject to change
        self.assertEqual(user_id, demo_id)

if __name__ == '__main__':
    print unittest.main()

