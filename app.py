from flask import Flask, request, jsonify
import requests
from dotenv import load_dotenv
import os
load_dotenv()

# Init app
app = Flask(__name__)

# Get NREL solar system data
@app.route('/results/<fe_json>', methods=['GET'])
def get_solar_system(fe_json):
    results = NREL(fe_json)
    return results.get()



class NREL(object):
    def __init__(self, fe_json):
        self.address = fe_json['address']
        self.system_capacity = fe_json['system_capacity']
        self.azimuth = azimuth
        self.tilt = tilt
        self.array_type = array_type
        self.module_type = module_type
        self.losses = losses

    def get(self):
        r = requests.get(f'https://developer.nrel.gov/api/pvwatts/v6.json?api_key={os.getenv("NREL_API_KEY")}&address={self.address}&system_capacity={self.system_capacity}&azimuth={self.azimuth}&tilt={self.tilt}&array_type={self.array_type}&module_type={self.module_type}&losses={self.losses}')
        # print(r.json())

nrel = NREL("322+N+7th+ave+beech+grove+in", 4, 180, 40, 1, 1, 10)
nrel.get()

# Run Server
if __name__ == '__main__':
    app.run(debug=True)