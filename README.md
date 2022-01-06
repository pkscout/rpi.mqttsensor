# rpi.rest
This python script is designed to run as a service on a Raspberry Pi that has either a SenseHat or BME280 for temperature and humidity information.  The script uses a RestAPI call to HomeAssistant to sent an entity state.


## PREREQUISITES:
1. You should be running Raspian Buster or later, although right now I wouldn't recommend Bullseye unless you like beta testing software.
1. Python3 is required.
1. For rpi.rest to function properly, there are two modules you need to install. From a terminal window type `sudo pip3 install RPi.bme280 requests` or `sudo pip install RPi.bme280 requests` (if you're system only has Python3).

## PI CONFIGURATION:
To use the BME280 sensor, you need to enable i2c in raspi-config. The i2c options are under INTERFACING OPTIONS in raspi-config.  

Then reboot.

## INSTALLATION:
It is recommended you install this in `/home/pi`.  The service file you'll install later assumes this, so if you install it somewhere else, you'll need to edit rpisc.service.


## CONFIGURATION:
You must create a settings.py file in the data folder of the script (create that folder if it doesn't exist) with at least the address of your Home Assistant server and the secret authentication token

```
rest_address = <ip address or name>
rest_token = <thetoken>
```

## USAGE:
To run from the terminal (for testing): `python3 /home/pi/rpi.rest/execute.py`  
To exit: CNTL-C

Running from the terminal is useful during initial testing, but once you know it's working the way you want, you should set it to autostart.  To do that you need to copy rpirest.service.txt to the systemd directory, change the permissions, and configure systemd. From a terminal window:
```
sudo cp -R /home/pi/rpi.rest/rpirest.service.txt /lib/systemd/system/rpirest.service
sudo chmod 644 /lib/systemd/system/rpirest.service
sudo systemctl daemon-reload
sudo systemctl enable rpirest.service
```

From now on the script will start automatically after a reboot.  If you want to manually stop or start the service you can do that as well. From a terminal window:
```
sudo systemctl stop rpirest.service 
sudo systemctl start rpirest.service 
```

You can change settings by editing the settings.py file any time you'd like.  You must stop and start the service/script for the changes to take affect.
