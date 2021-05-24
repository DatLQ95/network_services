import asyncio
import urllib.request, json 
import time
import threading 
import os
import numpy as np
import subprocess
# import aiohttp
import requests
import urllib3
import sys

from prometheus_client import Histogram
from prometheus_client import start_http_server, Summary, Counter

import os

# IP_ADDRESS = os.getenv('IP_ADDRESS')
# PORT_NUMBER = os.getenv('PORT_NUMBER')
# USER_NO = os.getenv('USER_NO')
# MEDIA_SERVICE = os.getenv('MEDIA_SERVICE')
# URL = "http://" + IP_ADDRESS + ":" + PORT_NUMBER

IP_ADDRESS = "131.155.35.52"
PORT_NUMBER = "8983"
# URL ="http://192.168.3.84:8088/aaa.mp4"
# URL ="http://131.155.35.53:8096"
URL = "http://" + IP_ADDRESS + ":" + PORT_NUMBER
MEDIA_SERVICE = 0
USER_NO = "10"


#Global var:
number_user = 0
error = 0

#TODO: this is prometheous code 
bucks = [(i*50) for i in range(20,100)]

h = Histogram('request_latency_seconds', 'Description of histogram', buckets= bucks)
s = Summary('summary_request_latency_seconds', 'Description of summary')
err = Counter('my_failures', 'Description of counter')
number_req = Counter('request_number', 'Description of counter')

upool = urllib3.PoolManager(num_pools=50,  block=False)

def run(cmd):
    with subprocess.Popen(cmd, stdout=subprocess.PIPE) as proc:
        print(proc.stdout.readlines())

class User(threading.Thread):
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
            number_req.inc()
            if MEDIA_SERVICE == 1: 
                text = "rtmp://" + IP_ADDRESS + ":" + PORT_NUMBER + "/vod/aaa.mp4"
                run(['ffmpeg',  '-i',  text, '-c:v', 'copy', '-c:a', 'copy', '-preset:v', 'ultrafast', '-segment_list_flags', '-y', '-t', '50', '-f', 'flv', 'emre.flv', '-y'])  
                time.sleep(0.5)
            else:
                r = upool.request('GET',URL)
                if (r.status != 200):
                    error = error + 1
                    err.inc()
                    print(r.status)
                
                time.sleep(0.5)
                # time.sleep(np.random.uniform(low=0.1, high=0.5))
                # time.sleep(np.random.exponential(30))

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
            if MEDIA_SERVICE == 1: 
                # TODO: find the way to measure the reponse latency from media?
                text = "rtmp://" + IP_ADDRESS + ":" + PORT_NUMBER + "/vod/aaa.mp4"
                # run(['ffmpeg',  '-i',  text, '-c:v', 'copy', '-c:a', 'copy', '-preset:v', 'ultrafast', '-segment_list_flags', '+live', '-y', '-f', 'flv', 'emre.flv', '-y'])  
                run(['ffmpeg',  '-i',  text, '-c:v', 'copy', '-c:a', 'copy', '-segment_list_flags', '+live', '-y', '-f', 'flv', 'emre.flv', '-y'])
                time.sleep(np.random.uniform(low=0.1, high=0.5))
            else:
                print("run")
                r = requests.get(URL)
                print(r.content)
                h.observe(r.elapsed.microseconds /10)
                s.observe(r.elapsed.microseconds / 10)
                print(r.elapsed.microseconds / 10)
                time.sleep(1)

if __name__ == '__main__':
    # start_http_server(int(int(str(PORT_NUMBER)) + 100))
    start_http_server(int(int(str(PORT_NUMBER)) + 100))
    t = UserTestMeasure()
    t.start()

    UserThreads = []
    while True: 
        # USER_NO = os.getenv('USER_NO')
        add_number_user = int(str(USER_NO)) - number_user
        # add or remove users
        if(add_number_user > 0):
            print("deploying")
            for i in range(add_number_user):
                t = User()
                t.start()
                UserThreads.append(t)
                time.sleep(0.01)
        elif(add_number_user < 0):
            for i,t in enumerate(UserThreads):
                if (i < (add_number_user * (-1))):
                    t.stop()
                    UserThreads.remove(t)
                    time.sleep(0.01)
        number_user = int(str(USER_NO))
        time.sleep(0.1)
        pass
