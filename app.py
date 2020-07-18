import requests
from dotenv import load_dotenv
import json
import os
load_dotenv()

class NREL(object):
    def __init__(self, address, system_capacity, azimuth, tilt, array_type, module_type, losses):
        self.address = address
        self.system_capacity = system_capacity
        self.azimuth = azimuth
        self.tilt = tilt
        self.array_type = array_type
        self.module_type = module_type
        self.losses = losses

    def get(self):
        r = requests.get(f'https://developer.nrel.gov/api/pvwatts/v6.json?api_key={os.getenv("NREL_API_KEY")}&address={self.address}&system_capacity={self.system_capacity}&azimuth={self.azimuth}&tilt={self.tilt}&array_type={self.array_type}&module_type={self.module_type}&losses={self.losses}')
        # r = requests.get(f'https://developer.nrel.gov/api/pvwatts/v6.json?api_key={os.getenv("NREL_API_KEY")}&address=322+N+7th+ave+beech+grove+in&system_capacity=4&azimuth=180&tilt=40&array_type=1&module_type=1&losses=10')
        print(r.json())

nrel = NREL("322+N+7th+ave+beech+grove+in", 4, 180, 40, 1, 1, 10)
nrel.get()

