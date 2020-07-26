import json
import os
from flask import Flask, jsonify, request
import requests
from dotenv import load_dotenv
load_dotenv()

# DEBUGGING TOOLS
# import code
# code.interact(local=dict(globals(), **locals()))


# Init app
app = Flask(__name__)


# Get solar system data from NREL API
@app.route('/results', methods=['POST'])
def get_solar_data():
    results = NREL(request.json)  # create new instance of an NREL object that takes in FE request info
    system_payload = results.get_system_info()  # Uses new NREL object to make API call to get solar energy system info
    value_payload = results.get_kwh_rate_info()  # Uses new NREL object to make API call to get user's kWh utility rate
    calculated_value = results.calculate_value(value_payload)  # Takes kWh utility rate and generates values in an array
    system_and_value_payload = {**system_payload, **calculated_value}  # Merges everything to be sent to FE
    return jsonify(system_and_value_payload)  # Coverts to json and sends over info to FE


# Main class that deconstructs FE request, makes API calls, and generates info to be returned to FE
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
        self.energy_output = None
        self.value_monthly = {
            "value_monthly": ""
        }

    # API call to get solar energy system info, set monthly energy output as an "instance variable", and deletes keys
    def get_system_info(self):
        response = requests.get(f'https://developer.nrel.gov/api/pvwatts/v6.json?api_key={os.getenv("NREL_API_KEY")}&address={self.address}&system_capacity={self.system_capacity}&azimuth={self.azimuth}&tilt={self.tilt}&array_type={self.array_type}&module_type={self.module_type}&losses={self.losses}')
        # line 47 sets the `self.energy_output` "instance variable" equal to the system's monthly output for use later
        # `json.loads essentially converts the response into json format for easier manipulation
        self.energy_output = json.loads(response.text)['outputs']['ac_monthly']
        # lines 50 to 55 takes any unnecessary keys out of the response to the front end, returning only what's needed
        # key deletion could be moved to helper function
        outputs = json.loads(response.text)['outputs']
        keys_to_remove = ('solrad_annual', 'poa_monthly', 'dc_monthly', 'ac_annual', 'capacity_factor')
        for key in keys_to_remove:
            if key in outputs:
                del outputs[key]
        return outputs

    # API call that extracts the user's kWr rate to be used in value calculation
    def get_kwh_rate_info(self):
        response = requests.get(f'https://developer.nrel.gov/api/utility_rates/v3.json?api_key={os.getenv("NREL_API_KEY")}&address={self.address}')
        return json.loads(response.text)['outputs']['residential']

    # this function ultimately generates an array of value data to be returned to the FE
    def calculate_value(self, kwh_rate):
        # line 65 grabs energy_output from the API call made in `get_system_info` and sets it equal to variable
        energy_output = self.energy_output
        # line 68 is generating the `value_monthly` response to FE as an array of values
        # it's iterating thru each element of the array, multiplying it by the kWh, and saving the answers ina new array
        values_to_add = list(map(lambda monthly_output: monthly_output * kwh_rate, energy_output))
        # before returning, it passes thru a helper function
        return self.update_value_dict(values_to_add)

    # this function updates `value_monthly` dictionary with a value equal to the user's month over month value array
    def update_value_dict(self, value_list):
        value_dict = self.value_monthly
        value_dict['value_monthly'] = value_list
        return value_dict

    # now write a function to generate user offset percentage


# Run Server
if __name__ == '__main__':
    app.run(debug=True)
