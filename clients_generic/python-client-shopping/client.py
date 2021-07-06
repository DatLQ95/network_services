import asyncio
import urllib.request, json 
import time
import threading 
import os
import numpy as np
import subprocess
import aiohttp
import requests
import urllib3

from paho.mqtt import client as mqtt_client

broker = '192.168.2.93'
port = 1883
topic = "/python/mqtt"

mediaStreamingUsersRaw = [555, 445, 335, 255, 235, 225, 210, 280, 365, 445, 535, 600, 645, 665, 690, 710, 690, 680, 665, 800, 970, 1000, 920, 865]
mediaStreamingUsers = [int(i*1.25) for i in mediaStreamingUsersRaw]

OnlineShoppingUsersRaw = [5900, 4700, 4500, 2700, 2800, 4000, 5200, 6800, 7700, 7700, 7700, 8400, 8800, 9000, 10000, 9700, 7800, 7200, 6800, 6300, 5600, 5500, 5400]
OnlineShoppingUsers = [int(i*0.9) for i in OnlineShoppingUsersRaw]

webServingUsersRaw = [4000, 4000, 4000, 5000, 3300, 2800, 3000, 4800, 10000, 6000, 6500, 6800, 7500, 8000, 9000, 8500, 6000, 5500, 5500, 5200, 3000, 2700, 2400, 1500]
webServingUsers = [int(i*0.9) for i in webServingUsersRaw]

webSearchingUsersRaw = [80, 50, 40, 30, 20, 10, 10, 20, 170, 370, 580, 780, 870, 970, 1000, 1050, 1040, 870, 700, 570, 400, 280, 180, 100]
webSearchingUsers = [int(i*8.5) for i in webSearchingUsersRaw]

# IoTUsers = [555, 445, 335, 255, 235, 225, 210, 280, 365, 445, 535, 600, 645, 665, 690, 710, 690, 680, 665, 800, 970, 1000, 920, 865]

granuality= 36 
URL_online_shopping = 'http://192.168.2.93:8080'
#Online Shopping 8000 user! exp 30
URL_web_serving = 'http://192.168.2.93:8096'
#Web browsing 200 user for uniform sleep 1.1-1.9
URL_web_searching = 'http://192.168.2.93:8983'
#Web browsing 200 user for uniform sleep 1.1-1.9
upool = urllib3.PoolManager(num_pools=50,  block=False)

def run(cmd):
    with subprocess.Popen(cmd, stdout=subprocess.PIPE) as proc:
        print(proc.stdout.readlines())

class UserServing(threading.Thread):
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
            upool.request('GET',URL_web_serving)
            time.sleep(np.random.exponential(30))

class UserShopping(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self._stop_event = threading.Event()
        # self.delay = delay

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

    def run(self):
        while(True):
            if self.stopped():
                return
            upool.request('GET',URL_online_shopping)
            time.sleep(np.random.exponential(30))

class UserMedia(threading.Thread):
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
            run(['ffmpeg',  '-i',  'rtmp://192.168.2.93/vod/aaa.mp4', '-c:v', 'copy', '-c:a', 'copy', '-preset:v', 'ultrafast', '-segment_list_flags', '-y', '-t', '50', '-f', 'flv', 'emre.flv', '-y'])  
            time.sleep(np.random.uniform(low=0.1, high=0.5))

class UserSearch(threading.Thread):
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
            upool.request('GET',URL_web_searching)
            time.sleep(np.random.exponential(30))

class UserIoT(threading.Thread):
    def __init__(self, client_id):
        threading.Thread.__init__(self)
        self._stop_event = threading.Event()
        self.client_id=client_id
        # self.delay = delay

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

    def connect_mqtt(self):
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print("Connected to MQTT Broker!")
            else:
                print("Failed to connect, return code %d\n", rc)

        client = mqtt_client.Client(self.client_id)
        # client.username_pw_set(username, password)
        client.on_connect = on_connect
        client.connect(broker, port)
        return client


    def publish(self, client):
        msg_count = 0
        while True:
            if self.stopped():
                return
            time.sleep(1)
            msg = f"messages: {msg_count}"
            result = client.publish(topic, msg)
            # result: [0, 1]
            status = result[0]
            if status == 0:
                print(f"Send `{msg}` to topic `{topic}`")
            else:
                print(f"Failed to send message to topic {topic}")
            msg_count += 1


    def run(self):
        client = self.connect_mqtt()
        # client.loop_start()
        self.publish(client)

shoppingUserThreads = []
for i in range(OnlineShoppingUsers[0]):
    t1 = UserShopping()
    t1.start()
    shoppingUserThreads.append(t1)
    time.sleep(0.01)

time.sleep(150)

while True:
    for days in range(7):
        scale = np.random.uniform(low=0.9, high=1.1)
        for index,rate in enumerate(OnlineShoppingUsers):
            for run_time in range(granuality):

                if(index == (len(OnlineShoppingUsers) - 1)):
                    a = OnlineShoppingUsers[index] + (OnlineShoppingUsers[0] - OnlineShoppingUsers[index])*(run_time + 1)/granuality
                else :
                    a = OnlineShoppingUsers[index] + (OnlineShoppingUsers[index + 1] - OnlineShoppingUsers[index])*(run_time + 1)/granuality

                number_user = int(a * scale)
                add_number_user = number_user - len(shoppingUserThreads)
                # add or remove users
                if(add_number_user > 0):
                    for i in range(add_number_user):
                        t = UserShopping()
                        t.start()
                        shoppingUserThreads.append(t)
                        time.sleep(0.001)
                elif(add_number_user < 0):
                    # print("here")
                    for i,t in enumerate(shoppingUserThreads):
                        if (i < (add_number_user * (-1))):
                            # print("therehere")
                            t.stop()
                            shoppingUserThreads.remove(t)
                            time.sleep(0.001)
                print(len(shoppingUserThreads))
                # sleep for 1 min
                time.sleep(20)

                # start = time.perf_counter()
                # count = 0
                # for i in range(number_request):
                #     count = count + 1
                #     end = time.perf_counter()
                #     if (end - start > 1):
                #         break
                #     # with urllib.request.urlopen("http://" + os.environ['SERVER_IP']  + ":" + os.environ['SERVER_PORT']) as url:
                #     with urllib.request.urlopen("http://192.168.2.83:8080") as url:
                #         data = url.read().decode()
                #     end2 = time.perf_counter()
                #     if((end2 - end) > 1/number_request):
                #         sleep_time = (end2 - end)
                #     else :
                #         sleep_time = 1/number_request - (end2 - end)
                #     time.sleep(sleep_time)
                #     print(data)



# URL = 'rtmp://131.155.35.53/vod/bbb.mp4'
# cmd = ['ffmpeg', '-i', 'rtmp://131.155.35.53/vod/bbb.mp4', '-y', '-t', '10', '-f', 'flv', 'emre.flv']

# async def fetch(proc):
    
#     async with subprocess.Popen(cmd, stdout=subprocess.PIPE) as proc:
#         response = await proc.stdout.readlines().decode("utf8")
#         print(response)


# async def main():
#     async with subprocess.Popen(cmd, stdout=subprocess.PIPE) as proc:
#         tasks = [fetch(proc) for _ in range(100)]
#         await asyncio.gather(*tasks)


# @timer(1, 5)
# def func():
#     asyncio.run(main())




# @timer(1, 5)
# def func():
#     asyncio.run(main())



# threads = []
# url = 'http://192.168.2.93:8080'

# t0 = time()
# for i in range(10000):
#     threads.append(spawn(upool.request,'GET',url))

# x = joinall(threads)

# print(len(x))
# print(time() - t0)