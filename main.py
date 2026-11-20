from machine import Pin
from time import sleep 
import network
import socket
import requests
import rp2
import sys
from secrets import WLAN_SSID, WLAN_PASSWORD, API_TOKEN



def connect():
    led = Pin("LED", Pin.OUT) 
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(WLAN_SSID, WLAN_PASSWORD)
    while wlan.isconnected() == False:
        if rp2.bootsel_button() == 1:
            sys.exit()
        print('Waiting for connection...')
        led.on()
        sleep(0.5)
        led.off()
        sleep(0.5)
    ip = wlan.ifconfig()[0]
    print(f'Connected on {ip}')
    return ip
def write_to_database(dataToSend):
    url="https://eu-central-1-1.aws.cloud2.influxdata.com/api/v2/write?org=University%20of%20Oulu&bucket=get-started&precision=s" 
    headers = {
        'Authorization' : 'Token ' + API_TOKEN,
        'Content-Type' : 'text/plain; charset=utf-8'
        }
    r = requests.post(url, data=dataToSend, headers=headers)
    print("request status: ", r.status_code)
    if r.status_code != 204:
        print(r.text)
    r.close()

ip = connect()
write_to_database("doorbell,location=front_door pressed=1.0")