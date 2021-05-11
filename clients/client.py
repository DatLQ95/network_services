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

IP_ADDRESS = os.getenv('IP_ADDRESS')
PORT_NUMBER = os.getenv('PORT_NUMBER')
USER_NO = os.getenv('USER_NO')
MEDIA_SERVICE = os.getenv('MEDIA_SERVICE')
URL = "http://" + IP_ADDRESS + ":" + PORT_NUMBER
# IP_ADDRESS = "192.168.3.84"
# PORT_NUMBER = "1935"
# URL ="http://192.168.3.84:8088/aaa.mp4"
# URL ="http://131.155.35.53:8088/aaa.mp4"
# MEDIA_SERVICE = 1
#Global var:
number_user = 0
error = 0

#TODO: this is prometheous code 
bucks = [(i*50) for i in range(20,100)]

h = Histogram('request_latency_seconds', 'Description of histogram', buckets= bucks)

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
            if MEDIA_SERVICE == 1: 
                text = "rtmp://" + IP_ADDRESS + ":" + PORT_NUMBER + "/vod/aaa.mp4"
                run(['ffmpeg',  '-i',  text, '-c:v', 'copy', '-c:a', 'copy', '-preset:v', 'ultrafast', '-segment_list_flags', '-y', '-t', '50', '-f', 'flv', 'emre.flv', '-y'])  
                time.sleep(0.5)
            else:
                try:
                    upool.request('GET',URL)
                    time.sleep(np.random.uniform(low=0.1, high=0.5))
                except:
                    print("err: ", sys.exc_info()[0])
                    error = error + 1
                    print("error: " + str(error))

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
                r = requests.get(URL)
                h.observe(r.elapsed.microseconds)
                time.sleep(1)

start_http_server(8000)
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
            time.sleep(0.01)
    elif(add_number_user < 0):
        for i,t in enumerate(UserThreads):
            if (i < (add_number_user * (-1))):
                t.stop()
                UserThreads.remove(t)
                time.sleep(0.01)
    number_user = int(str(USER_NO))
    print(number_user)

    # # sleep for 1 min
    # time.sleep(20)
    # if number_user < USER_NO:
    #     t = User()
    #     t.start()
    #     UserThreads.append(t)
    #     time.sleep(0.01)
    # elif number_user > USER_NO:
    #     for i,t in enumerate(searchingUserThreads):
    #         if (i < (add_number_user * (-1))):
    #         # print("therehere")
    #         t.stop()
    #         searchingUserThreads.remove(t)
    #         time.sleep(0.001)

# for i in range(USER_NO):
#     t = User()
#     t.start()
#     searchingUserThreads.append(t)
#     time.sleep(0.01)

# time.sleep(1)


# while True:
#     for days in range(7):
#         scale = np.random.uniform(low=0.9, high=1.1)
#         for index,rate in enumerate(webSearchingUsers):
#             for run_time in range(granuality):

#                 if(index == (len(webSearchingUsers) - 1)):
#                     a = webSearchingUsers[index] + (webSearchingUsers[0] - webSearchingUsers[index])*(run_time + 1)/granuality
#                 else :
#                     a = webSearchingUsers[index] + (webSearchingUsers[index + 1] - webSearchingUsers[index])*(run_time + 1)/granuality

#                 number_user = int(a * scale)
#                 add_number_user = number_user - len(searchingUserThreads)
#                 # add or remove users
#                 if(add_number_user > 0):
#                     for i in range(add_number_user):
#                         t = UserSearch()
#                         t.start()
#                         searchingUserThreads.append(t)
#                         time.sleep(0.001)
#                 elif(add_number_user < 0):
#                     # print("here")
#                     for i,t in enumerate(searchingUserThreads):
#                         if (i < (add_number_user * (-1))):
#                             # print("therehere")
#                             t.stop()
#                             searchingUserThreads.remove(t)
#                             time.sleep(0.001)
#                 print(len(searchingUserThreads))
#                 # sleep for 1 min
#                 time.sleep(20)
