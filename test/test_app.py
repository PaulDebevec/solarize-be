import unittest
from unittest.mock import patch
from app import NREL


class TestApp(unittest.TestCase):
    def test_req_res(self):
        mock_json = {
            "inputs": {
                "system_capacity": "4",
                "lat": "40",
                "lon": "-105",
                "azimuth": "180",
                "tilt": "40",
                "array_type": "1",
                "module_type": "1",
                "losses": "10"
            },
            "errors": [],
            "warnings": [],
            "version": "1.4.0",
            "ssc_info": {
                "version": 45,
                "build": "Linux 64 bit GNU/C++ Jul  7 2015 14:24:09"
            },
            "station_info": {
                "lat": 40.0099983215332,
                "lon": -105.0199966430664,
                "elev": 1581.8399658203125,
                "tz": -7,
                "location": "None",
                "city": "",
                "state": "Colorado",
                "solar_resource_file": "W10502N4001.csv",
                "distance": 2029
            },
            "outputs": {
                "ac_monthly": [
                    474.4326171875,
                    484.3903503417969,
                    595.7704467773438,
                    592.0599365234375,
                    591.2662353515625,
                    589.3538208007812,
                    583.2352905273438,
                    586.4593505859375,
                    584.8131713867188,
                    561.72314453125,
                    486.12603759765625,
                    445.68817138671875
                ],
                "poa_monthly": [
                    141.48094177246094,
                    145.57119750976562,
                    184.7876434326172,
                    181.55137634277344,
                    186.42808532714844,
                    190.51329040527344,
                    188.74996948242188,
                    190.53981018066406,
                    188.2213134765625,
                    175.4444122314453,
                    146.31704711914062,
                    131.15682983398438
                ],
                "solrad_monthly": [
                    4.563901424407959,
                    5.198971271514893,
                    5.9608917236328125,
                    6.051712512969971,
                    6.0138092041015625,
                    6.350442886352539,
                    6.088708877563477,
                    6.146445274353027,
                    6.274043560028076,
                    5.659497261047363,
                    4.877234935760498,
                    4.230865478515625
                ],
                "dc_monthly": [
                    497.9421081542969,
                    511.1524963378906,
                    634.3223266601562,
                    623.7313842773438,
                    617.8812866210938,
                    615.4278564453125,
                    609.3965454101562,
                    612.7506713867188,
                    610.5584106445312,
                    588.6157836914062,
                    508.07476806640625,
                    465.4272155761719
                ],
                "ac_annual": 6575.31884765625,
                "solrad_annual": 5.618043899536133,
                "capacity_factor": 18.765178680419922
            }
        }

        with patch('app.requests.get') as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.json.return_value = mock_json

        nrel_obj = NREL("322+N+7th+ave+beech+grove+in", 4, 180, 40, 1, 1, 10)
        response = nrel_obj.get()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, mock_json)

if __name__ == "__main__":
    unittest.main()