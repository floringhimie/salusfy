# Home-Assistant Custom Components
Custom Components for Home-Assistant (http://www.home-assistant.io)

# Salus Thermostat Climate Component
Component to interface with the salus-it500.com.
It reads the Current Temperature, Set Temperature, Current HVAC Mode, Current Relay Mode.

### Installation
* If not exist, in config/custom_components/ create a directory called salusfy 
* Copy all files in salusfy to your config/custom_components/salusfy/ directory.
* Configure with config below.
* Restart Home-Assistant.

### Usage
To use this component in your installation, add the following to your configuration.yaml file:

### Example configuration.yaml entry

```
climate:
  - platform: salusfy
    username: "EMAIL"
    password: "PASSWORD"
    id: "DEVICEID"
```
![image](https://user-images.githubusercontent.com/33951255/140300295-4915a18f-f5d4-4957-b513-59d7736cc52a.png)
