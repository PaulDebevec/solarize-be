import json
import os
from flask import Flask, jsonify, request
import requests
from dotenv import load_dotenv
load_dotenv()


# Init app
app = Flask(__name__)


# Get solar system data from NREL API
@app.route('/results', methods=['POST'])
def get_solar_system():
    results = NREL(request.json)
    payload = results.get()
    payload = json.loads(payload.text)
    return jsonify(payload)


class NREL(object):
    def __init__(self, fe_json):
        self.address = fe_json["solarizer_parameters"]['address']
        self.system_capacity = fe_json["solarizer_parameters"]['system_capacity']
        self.azimuth = fe_json["solarizer_parameters"]['azimuth']
        self.tilt = fe_json["solarizer_parameters"]['tilt']
        self.array_type = fe_json["solarizer_parameters"]['array_type']
        self.module_type = fe_json["solarizer_parameters"]['module_type']
        self.losses = fe_json["solarizer_parameters"]['losses']

    def get(self):
        return requests.get(f'https://developer.nrel.gov/api/pvwatts/v6.json?api_key={os.getenv("NREL_API_KEY")}&address={self.address}&system_capacity={self.system_capacity}&azimuth={self.azimuth}&tilt={self.tilt}&array_type={self.array_type}&module_type={self.module_type}&losses={self.losses}')


# Run Server
if __name__ == '__main__':
    app.run(debug=True)
