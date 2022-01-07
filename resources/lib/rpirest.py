
import resources.config as config
import json
import os
import sys
import time
import traceback
from datetime import datetime
from resources.lib.sensors import BME280Sensors, SenseHatSensors
from resources.lib.xlogger import Logger
from resources.lib import url


class PassSensorData:

    def __init__(self, lw):
        self.KEEPRUNNING = True
        self.LW = lw
        self.READINGDELTA = config.Get('readingdelta') * 60
        self.WHICHSENSOR = config.Get('which_sensor')
        self.SENSOR = self._pick_sensor()
        self.TEMPSCALE = '°C'
        headers = {}
        headers['Content-Type'] = 'application/json'
        headers['Accept'] = 'application/json'
        headers['Authorization'] = 'Bearer %s' % config.Get('rest_token')
        self.JSONURL = url.URL('json', headers=headers)
        self.RESTURL = 'http://%s:%s/api/states/sensor.%s' % (config.Get(
            'rest_address'), config.Get('rest_port'), config.Get('rest_state_name'))

    def Start(self):
        self.LW.log(['starting up PassSensorData'], 'info')
        stored_temp = None
        stored_humidity = None
        try:
            while self.KEEPRUNNING:
                temperature = self._convert_temp(self.SENSOR.Temperature())
                humidity = self.SENSOR.Humidity()
                if int(temperature) != stored_temp:
                    stored_temp = int(temperature)
                    payload = {'state': temperature, "attributes": {
                        "unit_of_measurement": self.TEMPSCALE, "friendly_name": "RPI Sensor Temperature"}}
                    status, loglines, results = self.JSONURL.Post(
                        self.RESTURL + 'temp', data=json.dumps(payload))
                    self.LW.log(loglines)
                else:
                    self.LW.log(['no change to temperature'])
                if int(humidity) != stored_humidity:
                    stored_humidity = int(humidity)
                    payload = {'state': humidity, "attributes": {
                        "unit_of_measurement": "%", "friendly_name": "RPI Sensor Humidity"}}
                    status, loglines, results = self.JSONURL.Post(
                        self.RESTURL + 'humidity', data=json.dumps(payload))
                    self.LW.log(loglines)
                else:
                    self.LW.log(['no change to humidity'])

                time.sleep(self.READINGDELTA)
        except KeyboardInterrupt:
            self.KEEPRUNNING = False
        except Exception as e:
            self.KEEPRUNNING = False
            self.LW.log([traceback.format_exc()], 'error')
            print(traceback.format_exc())

    def _convert_temp(self, temperature):
        if config.Get('temp_scale').lower() == 'f':
            self.TEMPSCALE = '°F'
            return (temperature * 1.8) + 32
        return temperature

    def _pick_sensor(self):
        self.LW.log(['setting up %s weather sensor' % self.WHICHSENSOR])
        if self.WHICHSENSOR.lower() == 'sensehat':
            return SenseHatSensors(adjust=config.Get('sensehat_adjust'), factor=config.Get('sensehat_factor'),
                                   testmode=config.Get('testmode'))
        else:
            return BME280Sensors(port=config.Get('i2c_port'), address=config.Get('bme280_address'),
                                 sampling=config.Get('bme280_sampling'), adjust=config.Get('bme280_adjust'),
                                 testmode=config.Get('testmode'))


class Main:

    def __init__(self, thepath):
        self.LW = Logger(logfile=os.path.join(os.path.dirname(thepath), 'data', 'logs', 'logfile.log'),
                         numbackups=config.Get('logbackups'), logdebug=config.Get('debug'))
        self.LW.log(['script started, debug set to %s' %
                    str(config.Get('debug'))], 'info')
        self.PASSSENSORDATA = PassSensorData(self.LW)
        self.PASSSENSORDATA.Start()
        self.LW.log(['closing down PassSensorData'], 'info')
