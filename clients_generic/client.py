import time
import threading 
import os
import numpy as np
import subprocess
# import aiohttp
import requests
import urllib3
import os

from prometheus_client import Histogram
from prometheus_client import start_http_server, Summary, Counter



IP_ADDRESS = os.getenv('IP_ADDRESS')

SEARCH_PORT_NUMBER = os.getenv('SEARCH_PORT_NUMBER')
SHOP_PORT_NUMBER = os.getenv('SHOP_PORT_NUMBER')
WEB_PORT_NUMBER = os.getenv('WEB_PORT_NUMBER')
MEDIA_PORT_NUMBER = os.getenv('MEDIA_PORT_NUMBER')

SEARCH_USER_NO = os.getenv('SEARCH_USER_NO')
SHOP_USER_NO = os.getenv('SHOP_USER_NO')
WEB_USER_NO = os.getenv('WEB_USER_NO')
MEDIA_USER_NO = os.getenv('MEDIA_USER_NO')

MEDIA_SERVICE = os.getenv('MEDIA_SERVICE')

SEARCH_URL = "http://" + IP_ADDRESS + ":" + SEARCH_PORT_NUMBER
SHOP_URL = "http://" + IP_ADDRESS + ":" + SHOP_PORT_NUMBER
WEB_URL = "http://" + IP_ADDRESS + ":" + WEB_PORT_NUMBER
MEDIA_URL = "http://" + IP_ADDRESS + ":" + MEDIA_PORT_NUMBER


client_node = 0

if IP_ADDRESS == "131.155.35.54":
    client_name = 4

if IP_ADDRESS == "131.155.35.53":
    client_name = 3

if IP_ADDRESS == "131.155.35.52":
    client_name = 2

if IP_ADDRESS == "131.155.35.51":
    client_name = 1

#Global var:
number_user = 0
error = 0
freq_request_per_thread = 0.5

#TODO: this is prometheous code 
bucks = [(i*10) for i in range(20,100)]

search_h = Histogram("request_latency_seconds_search_client_" + f"{client_node}", 'Description of histogram', buckets= bucks)
shop_h = Histogram("request_latency_seconds_shop_client_" + f"{client_node}", 'Description of histogram', buckets= bucks)
web_h = Histogram("request_latency_seconds_web_client_" + f"{client_node}", 'Description of histogram', buckets= bucks)
media_h = Histogram("request_latency_seconds_media_client_" + f"{client_node}", 'Description of histogram', buckets= bucks)

s = Summary('summary_request_latency_seconds', 'Description of summary')
err = Counter('drop_conn', 'Description of counter')
number_req = Counter('success_conn', 'Description of counter')
err_connect = Counter('error_conn', 'Description of counter')

upool = urllib3.PoolManager(num_pools=50)

def run(cmd):
    with subprocess.Popen(cmd, stdout=subprocess.PIPE) as proc:
        print(proc.stdout.readlines())

class SearchUser(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

    def run(self):
        while(True):
            if self.stopped():
                return
            err_connect.inc()
            if int(MEDIA_SERVICE) == 1: 
                text = "rtmp://" + IP_ADDRESS + ":" + SEARCH_PORT_NUMBER + "/vod/aaa.mp4"
                run(['ffmpeg',  '-i',  text, '-c:v', 'copy', '-c:a', 'copy', '-segment_list_flags', '+live', '-y', '-f', 'flv', 'emre.flv', '-y'])  
            else:
                r = upool.request('GET', SEARCH_URL)

                if (r.status == 200):
                    number_req.inc()
                else:
                    err.inc()
                    print(r.status)
            time.sleep(freq_request_per_thread)

class UserTestMeasure(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

    def run(self):
        while(True):
            if self.stopped():
                return
            if int(MEDIA_SERVICE) == 1: 
                # TODO: find the way to measure the reponse latency from media?
                # text = "rtmp://" + IP_ADDRESS + ":" + PORT_NUMBER + "/vod/aaa.mp4"
                # run(['ffmpeg',  '-i',  text, '-c:v', 'copy', '-c:a', 'copy', '-preset:v', 'ultrafast', '-segment_list_flags', '+live', '-y', '-f', 'flv', 'emre.flv', '-y'])  
                # run(['ffmpeg',  '-i',  text, '-c:v', 'copy', '-c:a', 'copy', '-segment_list_flags', '+live', '-y', '-f', 'flv', 'emre.flv', '-y'])
                pass
            else:
                r = requests.get(SEARCH_URL)
                h.observe(r.elapsed.microseconds /10)
                s.observe(r.elapsed.microseconds / 10)
                print(r.elapsed.microseconds / 10)
            time.sleep(1)

if __name__ == '__main__':
    # start_http_server(int(int(str(PORT_NUMBER)) + 100))
    print(URL)
    print(MEDIA_SERVICE)
    start_http_server(9999)
    t = UserTestMeasure()
    t.start()

    UserThreads = []
    while True: 
        USER_NO = os.getenv('USER_NO')
        add_number_user = int(str(USER_NO)) - number_user
        # add or remove users
        if(add_number_user > 0):
            for i in range(add_number_user):
                t = User()
                t.start()
                UserThreads.append(t)
                time_sleep = (freq_request_per_thread / add_number_user)
                time.sleep(time_sleep)
        elif(add_number_user < 0):
            for i,t in enumerate(UserThreads):
                if (i < (add_number_user * (-1))):
                    t.stop()
                    UserThreads.remove(t)
                    time_sleep = (freq_request_per_thread / (add_number_user) * (-1))
                    time.sleep(time_sleep)
        number_user = int(str(USER_NO))
        time.sleep(0.1)
        pass
