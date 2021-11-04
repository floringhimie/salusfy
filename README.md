# Home-Assistant Custom Components
Custom Components for Home-Assistant (http://www.home-assistant.io)

# Salus Thermostat Climate Component
My device is RT301i, it is working with it500 thermostat, the ideea is simple if you have a Salus Thermostat and you are able to login to salus-it500.com and controll it from this page, this custom component should work.
Component to interface with the salus-it500.com.
It reads the Current Temperature, Set Temperature, Current HVAC Mode, Current Relay Mode.

Keep in mind this is my first custom component and this is also the first version of this Salusfy so it can have bugs. Sorry for that.

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
![image](https://user-images.githubusercontent.com/33951255/140303472-fd38b9e4-5c33-408f-afef-25547c39551c.png)


### Getting the DEVICEID
1. Loggin to https://salus-it500.com with email and password used in the mobile app(in my case RT301i)
2. Click on the device
3. In the next page you will be able to see the device ID in the page URL
4. Copy the device ID from the URL
![image](https://user-images.githubusercontent.com/33951255/140301260-151b6af9-dbc4-4e90-a14e-29018fe2e482.png)


