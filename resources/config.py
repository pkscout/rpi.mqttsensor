import sys
defaults = {'readingdelta': 2,
            'which_sensor': 'BME280',
            'i2c_port': 1,
            'bme280_address': 0x76,
            'bme280_sampling': 4,
            'bme280_adjust': -1,
            'sensehat_adjust': True,
            'sensehat_factor': 8.199,
            'rest_address': '',
            'rest_port': 8123,
            'rest_state_name': 'rpi',
            'rest_token': '',
            'temp_scale': 'F',
            'logbackups': 1,
            'debug': False,
            'testmode': False}

try:
    import data.settings as overrides
    has_overrides = True
except ImportError:
    has_overrides = False
if sys.version_info < (3, 0):
    _reload = reload
elif sys.version_info >= (3, 4):
    from importlib import reload as _reload
else:
    from imp import reload as _reload


def Reload():
    if has_overrides:
        _reload(overrides)


def Get(name):
    setting = None
    if has_overrides:
        setting = getattr(overrides, name, None)
    if not setting:
        setting = defaults.get(name, None)
    return setting
