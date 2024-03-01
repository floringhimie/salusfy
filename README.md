# Home-Assistant Custom Components

[![CI](https://github.com/matthewturner/salusfy/actions/workflows/ci.yml/badge.svg)](https://github.com/matthewturner/salusfy/actions/workflows/ci.yml)

Custom Components for Home-Assistant (http://www.home-assistant.io)

# Salus Thermostat Climate Component
My device is RT301i, it is working with it500 thermostat, the idea is simple if you have a Salus Thermostat and you are able to login to salus-it500.com and control it from this page, this custom component should work.

## Component to interface with the salus-it500.com.
It reads the Current Temperature, Set Temperature, Current HVAC Mode, Current Relay Mode.

Keep in mind this is my first custom component and this is also the first version of this Salusfy so it can have bugs. Sorry for that.

**** This is not an official integration.

### Installation
1. Clone the repo into the `home_assistant` directory
1. Change directory into the `salusfy` directory
1. Run install.sh (you may need to fix the line endings)
1. Configure with config below
1. Restart Home Assistant

### Usage
To use this component in your installation, add the following to your configuration.yaml file:

#### Example configuration.yaml entry

```
climate:
  - platform: salusfy
    username: "EMAIL"
    password: "PASSWORD"
    id: "DEVICE_ID"
```
![image](https://user-images.githubusercontent.com/33951255/140300295-4915a18f-f5d4-4957-b513-59d7736cc52a.png)
![image](https://user-images.githubusercontent.com/33951255/140303472-fd38b9e4-5c33-408f-afef-25547c39551c.png)


### Getting the DEVICE_ID
1. Loggin to https://salus-it500.com with email and password used in the mobile app (in my case RT301i)
2. Click on the device
3. In the next page you will be able to see the device ID in the page URL
4. Copy the device ID from the URL
![image](https://user-images.githubusercontent.com/33951255/140301260-151b6af9-dbc4-4e90-a14e-29018fe2e482.png)


### Separate Temperature Client
Due to how chatty Home Assistant integrations are, the salus-it500.com server may start blocking your public IP address. This will prevent the gateway and mobile client from connecting. To resolve this, you can use the `TemperatureClient` which:

* suppresses requests to Salus for reading the current temperature
* queries another Home Assistant entity for current temperature via the HA API

The effect of this is that the target temperature/mode values may be out of date **if they have been updated outside of HA**, but the main control features (target temperature, set mode etc) will still work.

To enable the `TemperatureClient`, set the following settings in `climate.yaml`:

```
climate:
  - platform: salusfy
    username: "EMAIL"
    password: "PASSWORD"
    id: "DEVICE_ID"
    enable_temperature_client: True
    host: "your-home-assistant-ip-address"
    entity_id: "sensor.your-temperature-sensor"
    access_token: "your-HA-access-token"
```

### Running Locally

You can exercise the integration locally using the `run.py` which calls the code on your local machine as if it was being run within Home Assistant. This can help debug any issues you may be having without waiting for multiple Home Assistant restarts.

To get going:

1. Copy `config.sample.py` to `config.py`
1. Replace the config (below) with the appropriate values for your installation
1. Run `python ./run.py`

Feel free to change the code to exercise different methods and configuration.

#### Example config.py

```
ENABLE_TEMPERATURE_CLIENT = True
HOST = "your-home-assistant-ip-address"
ENTITY_ID = "sensor.your-temperature-sensor"
ACCESS_TOKEN = "your-HA-access-token"
```