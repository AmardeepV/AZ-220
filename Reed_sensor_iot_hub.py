from base64 import b64encode, b64decode  # encoding library
from hashlib import sha256  #Cryptographic Hash Algorithm
from urllib import quote_plus, urlencode  # URl library. Make sure to run this code on python 2 because in python3 this method is little bit different
from hmac import HMAC  # Message Authentication library
import RPi.GPIO as GPIO   # GPIO pin of Raspberry library
import time    # time library for delay
import requests     # Request library
import json   #  Json string library

MAGNET_GPIO = 17  # gpio pin of raspberry pi

# Azure IoT Hub
URI = 'zzzzzzzzz.azure-devices.net'  # Insert you IOT HUB URI Name
KEY = 'zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz'  # Replace with your device primary key
IOT_DEVICE_ID = 'XXXXXX'  #  Enter your IOT Device name
POLICY = 'iothubowner'

#  Generating SAS token for azure
def generate_sas_token():
    expiry=3600
    ttl = time.time() + expiry
    sign_key = "%s\n%d" % ((quote_plus(URI)), int(ttl))
    signature = b64encode(HMAC(b64decode(KEY), sign_key, sha256).digest())

    rawtoken = {
        'sr' :  URI,
        'sig': signature,
        'se' : str(int(ttl))
    }

    rawtoken['skn'] = POLICY

    return 'SharedAccessSignature ' + urlencode(rawtoken)

# Reading sensor data
def sensor_data():
      GPIO.setwarnings(False)
      GPIO.setmode(GPIO.BCM) # GPIO Numbers instead of board numbers
      GPIO.setup(MAGNET_GPIO, GPIO.IN) # GPIO Assign mode
      token = generate_sas_token()
      while True:
          
            value = GPIO.input(MAGNET_GPIO)
           # time.sleep(1)
            message = { "door": str(value) }
            data = json.dumps(message)
            print(data)
            send_message(token, message)
            time.sleep(1)

# Send sensor data method
def send_message(token, message):
    url = 'https://{0}/devices/{1}/messages/events?api-version=2016-11-14'.format(URI, IOT_DEVICE_ID)
    headers = {
        "Content-Type": "application/json",
        "Authorization": token
    }
    data = json.dumps(message)
    #print (data)
    response = requests.post(url, data=data, headers=headers)
# Main method
if __name__ == '__main__':

       try:
           sensor_data()
       except KeyboardInterrupt:
           pass
       finally:

            GPIO.cleanup()
