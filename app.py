import json
import os
from flask import Flask, jsonify, request
import requests
from dotenv import load_dotenv
load_dotenv()


app = Flask(__name__)


@app.route('/results', methods=['POST'])
def get_solar_data():
    results = NREL(request.json)
    system_payload = results.get_system_info()
    value_payload = results.get_kwh_rate_info()
    calculated_value = results.calculate_value(value_payload)
    system_and_value_payload = {**system_payload, **calculated_value}
    offset_payload = results.calculate_offset()
    total_payload = {**system_and_value_payload, **offset_payload}
    return jsonify(total_payload)


class NREL(object):
    def __init__(self, fe_json):
        params = fe_json['solarizer_parameters']
        self.address = params['address']
        self.system_capacity = params['system_capacity']
        self.azimuth = params['azimuth']
        self.tilt = params['tilt']
        self.array_type = params['array_type']
        self.module_type = params['module_type']
        self.losses = params['losses']
        self.historical_values = fe_json['historical_kWh']
        self.energy_output = None
        self.monthly_values = {
            "value_monthly": ""
        }
        self.percent_offset = {
            "percent_offset": ""
        }


    def get_system_info(self):
        response = requests.get(f'https://developer.nrel.gov/api/pvwatts/v6.json?api_key={os.getenv("NREL_API_KEY")}&address={self.address}&system_capacity={self.system_capacity}&azimuth={self.azimuth}&tilt={self.tilt}&array_type={self.array_type}&module_type={self.module_type}&losses={self.losses}')
        self.energy_output = json.loads(response.text)['outputs']['ac_monthly']
        outputs = json.loads(response.text)['outputs']
        keys_to_remove = ('solrad_annual', 'poa_monthly', 'dc_monthly', 'ac_annual', 'capacity_factor')
        for key in keys_to_remove:
            if key in outputs:
                del outputs[key]
        return outputs

    def get_kwh_rate_info(self):
        response = requests.get(f'https://developer.nrel.gov/api/utility_rates/v3.json?api_key={os.getenv("NREL_API_KEY")}&address={self.address}')
        return json.loads(response.text)['outputs']['residential']

    def calculate_value(self, kwh_rate):
        energy_output = self.energy_output
        values_to_add = list(map(lambda monthly_output: monthly_output * kwh_rate, energy_output))
        return self.update_value_dict(values_to_add)

    def update_value_dict(self, value_list):
        value_dict = self.monthly_values
        value_dict['value_monthly'] = value_list
        return value_dict

    def calculate_offset(self):
        if self.historical_values['january'] == "undefined":
            return self.percent_offset
        else:
            summed_historical = sum(self.historical_values.values())
            summed_output = sum(self.energy_output)
            percentage = (summed_output / summed_historical) * 100
            self.percent_offset['percent_offset'] = percentage
            return self.percent_offset


if __name__ == '__main__':
    app.run(debug=True)
