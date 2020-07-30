## Solarizer Microservice [![Build Status](https://travis-ci.com/PaulDebevec/solarizer-be.svg?branch=master)](https://travis-ci.com/github/PaulDebevec/solarize-be/builds/177855156)

## Table of Contents

* [About](#about)
  * [Learning Goals](#learning-goals)
* [Getting Started](#getting-started)
  * [Installation](#installation)
  * [Testing](#testing)
* [Solarizer Microservice Endpoints](#solarizer-microservice-endpoints)

## About

This microservice is for our front-end app [Solarizer](https://github.com/PaulDebevec/solarizer). The purpose of this microservice is to reach out to NREL's [pvwatts](https://developer.nrel.gov/docs/solar/pvwatts/v6/), and [Utility Rates](https://developer.nrel.gov/docs/electricity/utility-rates-v3/) API's. Based on user input parameters, the PVWatts API will generate a hypothetical solar energy system as well as the value created by that system. The user also has the option to input their annual energy usage, and a function within the [Solarizer](https://github.com/PaulDebevec/solarizer) application will return information on how much energy their hypothetical solar energy system will offset over the course of a year.

### Learning Goals: 

- To use a culmination of knowledge and skills gained while at [Turing](https://turing.io/).
- Practice an agile process on a 5-person team.
- Two-weeks to learn and utilize a new and unfamilier language and framework.


### Built with:

- Python 3.7
- Flask 1.1.1

***Testing framework***
- Pytest

## Getting Started

To get a local copy up and running follow these simple steps.

### Installation

1. Clone the repo
```sh
git clone git@github.com:PaulDebevec/solarize-be.git
```
2. Create your virtual environment (*NOTE:  this should be installed at the same level as the project directory*)
```sh
python3 -m venv venv
```
3. Activate your virtual environment (*NOTE: drop into the solarize-be directory before activation*)
```sh
source venv/bin/activate
```
4. Install the `requirements.txt` file
```sh
pip install -r requirements.txt

```

### Running
1. In order to run the application, drop into your solarize-be directory and run the following command:
```sh
python app.py
```


### Testing

1. Run the test suite from the root directory of the repository

```sh
pytest
```
2. If you would like more information on the items like local variables, run:
```sh
pytest --showlocals
```


## Solarizer Microservice Endpoints

Retrieve solar energy system information:

* User-input sent in the request body
```sh
{
  "solarizer_parameters": {
    "name": "example request",
    "address": "1490+Delgany+St+Denver+CO+80202",
    "system_capacity": 4,
    "module_type": 0,
    "array_type": 0,
    "losses": 14,
    "tilt": 20,
    "azimuth": 180
  },
  "historical_kWh": {
    "january": 100,
    "february": 100,
    "march": 100,
    "april": 100,
    "may": 100,
    "june": 100,
    "july": 100,
    "august": 100,
    "september": 100,
    "october": 100,
    "november": 100,
    "december": 100
  }
}
```

Request
```sh
POST /results
```

Expected response: 
```sh
{
    "ac_monthly": [
        397.0354309082031,
        429.8955383300781,
        570.6409912109375,
        598.790283203125,
        609.8270263671875,
        609.14501953125,
        599.88525390625,
        583.9315795898438,
        544.9886474609375,
        485.9424743652344,
        412.0427551269531,
        366.7494201660156
    ],
    "percent_offset": 517.4062016805012,
    "solrad_monthly": [
        3.810142755508423,
        4.711258888244629,
        5.75254487991333,
        6.278196811676025,
        6.404174327850342,
        6.974189758300781,
        6.6839070320129395,
        6.462113857269287,
        6.07655668258667,
        5.0663628578186035,
        4.2511725425720215,
        3.53259539604187
    ],
    "value_monthly": [
        43.872415115356446,
        47.50345698547363,
        63.055829528808594,
        66.16632629394532,
        67.38588641357421,
        67.31052465820312,
        66.28732055664062,
        64.52443954467773,
        60.22124554443359,
        53.6966434173584,
        45.53072444152832,
        40.525810928344725
    ]
}
```
