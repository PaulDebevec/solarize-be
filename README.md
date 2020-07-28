## Solarizer Microservice

## Table of Contents

* [About](#about)
  * [Learning Goals](#learning-goals)
  * [Tech Stack](#tech-stack)
* [Getting Started](#getting-started)
  * [Installation](#installation)
  * [Testing](#testing)
* [Sweater Weather Access Points](#sweater-weather-access-points)

## About

This microservice is for our front-end app [Solarizer](https://github.com/PaulDebevec/solarizer). The purpose of this microservice is to reach out to NREL's [pvwatts](https://developer.nrel.gov/docs/solar/pvwatts/v6/), and [Utility Rates](https://developer.nrel.gov/docs/electricity/utility-rates-v3/) API's. Based on user input parameters, the PVWatts API will generate a hypothetical solar energy system as well as the value created by that system. The user also has the option to input their annual energy usage, and a function within the [Solarizer](https://github.com/PaulDebevec/solarizer) application will return information on how much energy their hypothetical solar energy system will offset over the course of a year.

### Learning Goals: 

- To use a culmination of knowledge and skills gained while at [Turing](https://turing.io/).
- Practice an agile process on a 5-person team.
- Two-weeks to learn and utilize a new and unfamilier language and framework.


### Built with:

- Ruby: 2.5.1
- PostgreSQL: 12.2
- Rails: 6.0.3
- Bcrypt (password encryption)
- fast_jsonapi

***Testing framework***
- RSpec
- Capybara
- Simplecov
- Shoulda-matchers
- Pry (For debugging)

## Getting Started

To get a local copy up and running follow these simple steps.

### Installation

1. Clone the repo
```sh
git clone git@github.com:PaulDebevec/sweater_weather.git
```
2. Install the Gem File
```sh
bundle install
```
3. Create your environment
```sh
rails db:create
rails db:migrate
```
4. Install Figaro
```sh
figaro install
```
5. Visit the Google API, OpenWeather and Unsplash site to retrieve your API keys. The keys must be stored securely in the `application.yml` file of your `app/config` directory.

```sh
WEATHER_API_KEY: <YOUR OPEN WEATHER API KEY>
GOOGLE_API_KEY: <YOUR GOOGLE API KEY>

UNSPLASH_API_KEY: <YOUR UNSPLASH API KEY>
UNSPLASH_SECRET: <YOUR UNSPLASH SECRET>

ZOMATO_API_KEY: <YOUR ZOMATO API KEY>
```

### Testing

1. Install RSpec

```sh
bundle install rspec
```
2. Require `webmock` in the `spec_helper.rb` file

```sh
require 'webmock/rspec'
```

3. Include the `vcr` config block in the `rails_helper.rb` file:

```sh 
require 'vcr'
require 'webmock/rspec'

VCR.configure do |config|
  config.cassette_library_dir = 'spec/cassettes'
  config.hook_into :webmock
  config.configure_rspec_metadata!
  config.allow_http_connections_when_no_cassette = true
  config.filter_sensitive_data('<WEATHER-API-KEY>') {ENV['WEATHER_API_KEY']}
  config.filter_sensitive_data('<GOOGLE_API_KEY>') {ENV['GOOGLE_API_KEY']}
  config.filter_sensitive_data('<UNSPLASH-API-KEY>') {ENV['UNSPLASH_API_KEY']}
  config.filter_sensitive_data('<UNSPLASH-SECRET>') {ENV['UNSPLASH_SECRET']}
end
```
4. Run the test suite from the root directory of the repository

```sh
rspec
```

## Sweater Weather Endpoints

Retrieve a background picture for a specific location:
```sh
GET api/v1/backgrounds?location=<location_name_here>
```
Expected response: 
```sh
{
    "data": {
        "id": 23723,
        "type": "background",
        "attributes": {
            "url": "image_link_here"
        }
    }
}
```
Retrieve weather forecast for a specific location:
```sh
GET api/v1/forecast?location=<location_name>
```
Expected response: 
```sh
{:data=>
  {:id=>"1",
   :type=>"forecast_info",
   :attributes=>
    {:id=>1,
     :today_forecast=>
      {:hourly_weather=>
        {:hourly_weather=>
          [{:time=>"8:00 PM", :temp=>55.81},
           {:time=>"9:00 PM", :temp=>54.32},
           {:time=>"10:00 PM", :temp=>53.71},
           {:time=>"11:00 PM", :temp=>52.54},
           {:time=>"12:00 AM", :temp=>50.38},
           {:time=>"1:00 AM", :temp=>49.41},
           {:time=>"2:00 AM", :temp=>46.36},
           {:time=>"3:00 AM", :temp=>46.15}]},
       :description=>"light rain",
       :location=>"Berthoud, Colorado",
       :temp_average=>55.81,
       :temp_high=>55.81,
       :temp_low=>51.53,
       :feels_like=>35.96,
       :humidity=>54,
       :visibility=>10,
       :uv_index=>8.96,
       :sunrise=>"05:30 AM",
       :sunset=>"08:28 PM"},
     :weekly_forecast=>
      {:daily_notes=>
        [{:day=>"Monday", :description=>"Rain", :precipitation_mm=>2, :temp_high=>55.81, :temp_low=>51.53},
         {:day=>"Tuesday", :description=>"Rain", :precipitation_mm=>1, :temp_high=>68.86, :temp_low=>47.84},
         {:day=>"Wednesday", :description=>"Clouds", :precipitation_mm=>0, :temp_high=>77.92, :temp_low=>46.6},
         {:day=>"Thursday", :description=>"Clear", :precipitation_mm=>0, :temp_high=>82.9, :temp_low=>51.4},
         {:day=>"Friday", :description=>"Clear", :precipitation_mm=>0, :temp_high=>91.44, :temp_low=>55.11},
         {:day=>"Saturday", :description=>"Rain", :precipitation_mm=>0, :temp_high=>93.13, :temp_low=>60.31},
         {:day=>"Sunday", :description=>"Clouds", :precipitation_mm=>0, :temp_high=>90.45, :temp_low=>60.3}]}}}}

```
Register a new user:
```sh
POST api/v1/users?email=<email_address_here>&password=<password_here>&password_confirmation=<confirmation_password_here>
```
Expected response: 
```sh
{:data=>{:id=>"195", :type=>"users", :attributes=>{:email=>"whatever@example.com", :api_key=>"6e5da00f3e4119b1d114c685908916d8"}}}
```
Login a registered user:
```
POST api/v1/sessions?email=<email_address_here>&password=<password_here>
```
Expected response: 
```sh
{:data=>{:id=>"196", :type=>"users", :attributes=>{:email=>"whatever@example.com", :api_key=>"jij342lmk1oj5klj234KNLMn34kmKM436"}}}
```

Returns road trip information for a registered user:
```
POST api/v1/road_trip?origin=<origin_here>&destination=<destination_here>&api_key=<api_key_here>
```
Expected response: 
```sh
{:data=>
  {:id=>"42",
   :type=>"road_trip_info",
   :attributes=>{:origin=>"Denver, CO, USA", :destination=>"Pueblo, CO, USA", :travel_time=>"1 hour 48 mins", :forecast=>{:weather=>{:temp=>65.57, :description=>"clear sky"}}}}}
```
