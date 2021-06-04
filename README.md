# Guide line #

## Set up env before running the RL Agent##
1. Set up Prometheous server. 
1. Run start-up.sh file to update all the images in each node. 
2. Build the image-server locally in each node.
3. Create servers using docker swarm.
4. Create load balancer using docker swarm.
5. Create node load balancer using docker swarm. 
6. Create the service client containers
7. Start all containers and wait for them to stablize. 

## Reset environment ##
### Init the environment, start all over again. ###
1. Set number user for each client services in each ingress nodes to start point.
2. Run all client services containers.
3. Wait for the container to be stable. (appx = 5 sec)
4. Run the client containers with initial user number.
5. Capture and return the observe bandwidth ingress from each node.

## Apply action (step) ##

1. Get the action space / action array from Agent RL.
2. Apply action: -> Docker swarm update
- Change the number of user of each service according to running time -> Docker Swarm Update 
- Change the weight accordingly -> Docker Swarm Update
3. Capture at same time: -> Prometheous + Netdata ( or other tool to collect container traffic info)
- Capture bandwidth value at each ingress node for each service (after time t2) -> netdata 
- Capture latency for each services. -> Prometheous in each client container
- Capture packet loss (if possible). -> Netdata in each client container
4. Calculate reward.
5. Normalize the observe space: traffic ingress during the time (BW of each service) + node load in each node (BW in each link).
6. Return new observation + reward.

## Container descriptions ##
-------------------------------------------------------------------

container: search_server 
image: search-server
port: 8983
lb port: 8984
input request port: 8001
docker service create --mode global --publish mode=host,target=80,published=8983 --name search_server luongquocdat01091995/network_services:search-server

-------------------------------------------------------------------

container: shop_server 
image: shop-server
port: 8080
lb port: 8081
input request port: 8002
docker service create --mode global --publish mode=host,target=80,published=8080 --name shop_server luongquocdat01091995/network_services:shop-server

-------------------------------------------------------------------

container: web_server 
image: web-server
port: 8096
lb port: 8097
input request port: 8003
docker service create --mode global --publish mode=host,target=80,published=8096 --name web_server luongquocdat01091995/network_services:web-server

-------------------------------------------------------------------

container: media_server 
image: media-server
port: 8088
lb port: 8089
input request port: 8004
docker service create --mode global --publish mode=host,target=80,published=8088 --publish mode=host,target=1935,published=1935 --name media_server media-server

-------------------------------------------------------------------

container: load_balancer
image: load-balancer
port: 8984, 8081, 8097, 8089
env vars:

ENV WEIGHT_SEARCH_2 1
ENV WEIGHT_SEARCH_3 2
ENV WEIGHT_SEARCH_4 3

ENV WEIGHT_SHOP_2 1
ENV WEIGHT_SHOP_3 2
ENV WEIGHT_SHOP_4 3

ENV WEIGHT_WEB_2 1
ENV WEIGHT_WEB_3 2
ENV WEIGHT_WEB_4 3

ENV WEIGHT_WEB_2 1
ENV WEIGHT_WEB_3 2
ENV WEIGHT_WEB_4 3

ENV IP_ADDRESS_NODE_2 192.168.3.74
ENV IP_ADDRESS_NODE_3 192.168.3.84
ENV IP_ADDRESS_NODE_4 192.168.3.94

ENV PORT_ADDRESS_SEARCH_LISTEN 8984
ENV PORT_ADDRESS_SHOP_LISTEN 8097
ENV PORT_ADDRESS_WEB_LISTEN 8081
ENV PORT_ADDRESS_MEDIA_LISTEN 8089

ENV PORT_ADDRESS_SEARCH_FORWARD 8983
ENV PORT_ADDRESS_SHOP_FORWARD 8096
ENV PORT_ADDRESS_WEB_FORWARD 8080
ENV PORT_ADDRESS_MEDIA_FORWARD 8088

Create service for each node:
docker service create --constraint node.labels.node_number==2 \
                                    --publish mode=host,target=8984,published=8984 \
                                    --publish mode=host,target=8081,published=8081 \
                                    --publish mode=host,target=8097,published=8097 \
                                    --publish mode=host,target=8089,published=8089 \
                                    -e WEIGHT_SEARCH_2=1 -e WEIGHT_SEARCH_3=2 -e WEIGHT_SEARCH_4=2 \
                                    -e WEIGHT_SHOP_2=1 -e WEIGHT_SHOP_3=2 -e WEIGHT_SHOP_4=2 \
                                    -e WEIGHT_WEB_2=1 -e WEIGHT_WEB_3=2 -e WEIGHT_WEB_4=2 \
                                    -e WEIGHT_WEB_2=1 -e WEIGHT_WEB_3=2 -e WEIGHT_WEB_4=2 \
                                    -e IP_ADDRESS_NODE_2=192.168.3.74 -e IP_ADDRESS_NODE_3=192.168.3.84 -e IP_ADDRESS_NODE_4=192.168.3.94 \
                                    -e PORT_ADDRESS_SEARCH_LISTEN=8984 -e PORT_ADDRESS_SHOP_LISTEN=8097 -e PORT_ADDRESS_WEB_LISTEN=8081 -e PORT_ADDRESS_MEDIA_LISTEN=8089 \
                                    -e PORT_ADDRESS_SEARCH_FORWARD=8983 -e PORT_ADDRESS_SHOP_FORWARD=8096 -e PORT_ADDRESS_WEB_FORWARD=8080 -e PORT_ADDRESS_MEDIA_FORWARD=8088 \
                                    --name load_balancer_2 luongquocdat01091995/network_services:load-balancer-general

docker service create --constraint node.labels.node_number==3 \
                                    --publish mode=host,target=8984,published=8984 \
                                    --publish mode=host,target=8081,published=8081 \
                                    --publish mode=host,target=8097,published=8097 \
                                    --publish mode=host,target=8089,published=8089 \
                                    -e WEIGHT_SEARCH_2=1 -e WEIGHT_SEARCH_3=2 -e WEIGHT_SEARCH_4=2 \
                                    -e WEIGHT_SHOP_2=1 -e WEIGHT_SHOP_3=2 -e WEIGHT_SHOP_4=2 \
                                    -e WEIGHT_WEB_2=1 -e WEIGHT_WEB_3=2 -e WEIGHT_WEB_4=2 \
                                    -e WEIGHT_WEB_2=1 -e WEIGHT_WEB_3=2 -e WEIGHT_WEB_4=2 \
                                    -e IP_ADDRESS_NODE_2=192.168.3.74 -e IP_ADDRESS_NODE_3=192.168.3.84 -e IP_ADDRESS_NODE_4=192.168.3.94 \
                                    -e PORT_ADDRESS_SEARCH_LISTEN=8984 -e PORT_ADDRESS_SHOP_LISTEN=8097 -e PORT_ADDRESS_WEB_LISTEN=8081 -e PORT_ADDRESS_MEDIA_LISTEN=8089 \
                                    -e PORT_ADDRESS_SEARCH_FORWARD=8983 -e PORT_ADDRESS_SHOP_FORWARD=8096 -e PORT_ADDRESS_WEB_FORWARD=8080 -e PORT_ADDRESS_MEDIA_FORWARD=8088 \
                                    --name load_balancer_3 luongquocdat01091995/network_services:load-balancer-general

docker service create --constraint node.labels.node_number==4 \
                                    --publish mode=host,target=8984,published=8984 \
                                    --publish mode=host,target=8081,published=8081 \
                                    --publish mode=host,target=8097,published=8097 \
                                    --publish mode=host,target=8089,published=8089 \
                                    -e WEIGHT_SEARCH_2=1 -e WEIGHT_SEARCH_3=2 -e WEIGHT_SEARCH_4=2 \
                                    -e WEIGHT_SHOP_2=1 -e WEIGHT_SHOP_3=2 -e WEIGHT_SHOP_4=2 \
                                    -e WEIGHT_WEB_2=1 -e WEIGHT_WEB_3=2 -e WEIGHT_WEB_4=2 \
                                    -e WEIGHT_WEB_2=1 -e WEIGHT_WEB_3=2 -e WEIGHT_WEB_4=2 \
                                    -e IP_ADDRESS_NODE_2=192.168.3.74 -e IP_ADDRESS_NODE_3=192.168.3.84 -e IP_ADDRESS_NODE_4=192.168.3.94 \
                                    -e PORT_ADDRESS_SEARCH_LISTEN=8984 -e PORT_ADDRESS_SHOP_LISTEN=8097 -e PORT_ADDRESS_WEB_LISTEN=8081 -e PORT_ADDRESS_MEDIA_LISTEN=8089 \
                                    -e PORT_ADDRESS_SEARCH_FORWARD=8983 -e PORT_ADDRESS_SHOP_FORWARD=8096 -e PORT_ADDRESS_WEB_FORWARD=8080 -e PORT_ADDRESS_MEDIA_FORWARD=8088 \
                                    --name load_balancer_4 luongquocdat01091995/network_services:load-balancer-general 

Update service at each load balancer:
docker service update --env-add WEIGHT_SEARCH_2=1 --env-add WEIGHT_SEARCH_3=2 --env-add WEIGHT_SEARCH_4=7 \
                      --env-add WEIGHT_SHOP_2=1 --env-add WEIGHT_SHOP_3=2 --env-add WEIGHT_SHOP_4=2 \
                      --env-add WEIGHT_WEB_2=1 --env-add WEIGHT_WEB_3=2 --env-add WEIGHT_WEB_4=2 \
                      --env-add WEIGHT_MEDIA_2=1 --env-add WEIGHT_MEDIA_3=2 --env-add WEIGHT_MEDIA_4=2 \
                      --env-add IP_ADDRESS_NODE_2=192.168.3.74 --env-add IP_ADDRESS_NODE_3=192.168.3.84 --env-add IP_ADDRESS_NODE_4=192.168.3.94 \
                      --env-add PORT_ADDRESS_SEARCH_LISTEN=8984 --env-add PORT_ADDRESS_SHOP_LISTEN=8097 --env-add PORT_ADDRESS_WEB_LISTEN=8081 --env-add PORT_ADDRESS_MEDIA_LISTEN=8089 \
                      --env-add PORT_ADDRESS_SEARCH_FORWARD=8983 --env-add PORT_ADDRESS_SHOP_FORWARD=8096 --env-add PORT_ADDRESS_WEB_FORWARD=8080 --env-add PORT_ADDRESS_MEDIA_FORWARD=8088 \
                      load_balancer_2

docker service update --env-add WEIGHT_SEARCH_2=1 --env-add WEIGHT_SEARCH_3=2 --env-add WEIGHT_SEARCH_4=2 \
                      --env-add WEIGHT_SHOP_2=1 --env-add WEIGHT_SHOP_3=2 --env-add WEIGHT_SHOP_4=2 \
                      --env-add WEIGHT_WEB_2=1 --env-add WEIGHT_WEB_3=2 --env-add WEIGHT_WEB_4=2 \
                      --env-add WEIGHT_MEDIA_2=1 --env-add WEIGHT_MEDIA_3=2 --env-add WEIGHT_MEDIA_4=2 \
                      load_balancer_3

docker service update --env-add WEIGHT_SEARCH_2=1 --env-add WEIGHT_SEARCH_3=2 --env-add WEIGHT_SEARCH_4=2 \
                      --env-add WEIGHT_SHOP_2=1 --env-add WEIGHT_SHOP_3=2 --env-add WEIGHT_SHOP_4=2 \
                      --env-add WEIGHT_WEB_2=1 --env-add WEIGHT_WEB_3=2 --env-add WEIGHT_WEB_4=2 \
                      --env-add WEIGHT_MEDIA_2=1 --env-add WEIGHT_MEDIA_3=2 --env-add WEIGHT_MEDIA_4=2 \
                      load_balancer_4

-------------------------------------------------------------------

container: load_balancer_node
image: load-balancer-node 
port: 8001, 8002, 8003, 8004
env vars:

ENV WEIGHT_SEARCH_2 1
ENV WEIGHT_SEARCH_3 2
ENV WEIGHT_SEARCH_4 3

ENV WEIGHT_SHOP_2 1
ENV WEIGHT_SHOP_3 2
ENV WEIGHT_SHOP_4 3

ENV WEIGHT_WEB_2 1
ENV WEIGHT_WEB_3 2
ENV WEIGHT_WEB_4 3

ENV WEIGHT_MEDIA_2 1
ENV WEIGHT_MEDIA_3 2
ENV WEIGHT_MEDIA_4 3

ENV IP_ADDRESS_NODE_2 192.168.3.74
ENV IP_ADDRESS_NODE_3 192.168.3.84
ENV IP_ADDRESS_NODE_4 192.168.3.94

ENV PORT_ADDRESS_SEARCH_LISTEN 8001
ENV PORT_ADDRESS_SHOP_LISTEN 8002
ENV PORT_ADDRESS_WEB_LISTEN 8003
ENV PORT_ADDRESS_MEDIA_LISTEN 8004

ENV PORT_ADDRESS_SEARCH_FORWARD 8984
ENV PORT_ADDRESS_SHOP_FORWARD 8097
ENV PORT_ADDRESS_WEB_FORWARD 8081
ENV PORT_ADDRESS_MEDIA_FORWARD 8089

Create load balancer at each node:

docker service create --constraint node.labels.node_number==2 \
                                     --publish mode=host,target=8001,published=8001 \
                                    --publish mode=host,target=8002,published=8002 \
                                    --publish mode=host,target=8003,published=8003 \
                                    --publish mode=host,target=8004,published=8004 \
                                    -e WEIGHT_SEARCH_2=1 -e WEIGHT_SEARCH_3=2 -e WEIGHT_SEARCH_4=2 \
                                    -e WEIGHT_SHOP_2=1 -e WEIGHT_SHOP_3=2 -e WEIGHT_SHOP_4=2 \
                                    -e WEIGHT_WEB_2=1 -e WEIGHT_WEB_3=2 -e WEIGHT_WEB_4=2 \
                                    -e WEIGHT_MEDIA_2=1 -e WEIGHT_MEDIA_3=2 -e WEIGHT_MEDIA_4=2 \
                                    -e IP_ADDRESS_NODE_2=192.168.3.74 -e IP_ADDRESS_NODE_3=192.168.3.84 -e IP_ADDRESS_NODE_4=192.168.3.94 \
                                    -e PORT_ADDRESS_SEARCH_LISTEN=8001 -e PORT_ADDRESS_SHOP_LISTEN=8002 -e PORT_ADDRESS_WEB_LISTEN=8003 -e PORT_ADDRESS_MEDIA_LISTEN=8004 \
                                    -e PORT_ADDRESS_SEARCH_FORWARD=8984 -e PORT_ADDRESS_SHOP_FORWARD=8097 -e PORT_ADDRESS_WEB_FORWARD=8081 -e PORT_ADDRESS_MEDIA_FORWARD=8089 \
                                    --name load_balancer_node_2 luongquocdat01091995/network_services:load-balancer-general  

docker service create --constraint node.labels.node_number==3 \
                                     --publish mode=host,target=8001,published=8001 \
                                    --publish mode=host,target=8002,published=8002 \
                                    --publish mode=host,target=8003,published=8003 \
                                    --publish mode=host,target=8004,published=8004 \
                                    -e WEIGHT_SEARCH_2=1 -e WEIGHT_SEARCH_3=2 -e WEIGHT_SEARCH_4=2 \
                                    -e WEIGHT_SHOP_2=1 -e WEIGHT_SHOP_3=2 -e WEIGHT_SHOP_4=2 \
                                    -e WEIGHT_WEB_2=1 -e WEIGHT_WEB_3=2 -e WEIGHT_WEB_4=2 \
                                    -e WEIGHT_MEDIA_2=1 -e WEIGHT_MEDIA_3=2 -e WEIGHT_MEDIA_4=2 \
                                    -e IP_ADDRESS_NODE_2=192.168.3.74 -e IP_ADDRESS_NODE_3=192.168.3.84 -e IP_ADDRESS_NODE_4=192.168.3.94 \
                                    -e PORT_ADDRESS_SEARCH_LISTEN=8001 -e PORT_ADDRESS_SHOP_LISTEN=8002 -e PORT_ADDRESS_WEB_LISTEN=8003 -e PORT_ADDRESS_MEDIA_LISTEN=8004 \
                                    -e PORT_ADDRESS_SEARCH_FORWARD=8984 -e PORT_ADDRESS_SHOP_FORWARD=8097 -e PORT_ADDRESS_WEB_FORWARD=8081 -e PORT_ADDRESS_MEDIA_FORWARD=8089 \
                                    --name load_balancer_node_3 luongquocdat01091995/network_services:load-balancer-general 

docker service create --constraint node.labels.node_number==4 \
                                     --publish mode=host,target=8001,published=8001 \
                                    --publish mode=host,target=8002,published=8002 \
                                    --publish mode=host,target=8003,published=8003 \
                                    --publish mode=host,target=8004,published=8004 \
                                    -e WEIGHT_SEARCH_2=1 -e WEIGHT_SEARCH_3=2 -e WEIGHT_SEARCH_4=2 \
                                    -e WEIGHT_SHOP_2=1 -e WEIGHT_SHOP_3=2 -e WEIGHT_SHOP_4=2 \
                                    -e WEIGHT_WEB_2=1 -e WEIGHT_WEB_3=2 -e WEIGHT_WEB_4=2 \
                                    -e WEIGHT_MEDIA_2=1 -e WEIGHT_MEDIA_3=2 -e WEIGHT_MEDIA_4=2 \
                                    -e IP_ADDRESS_NODE_2=192.168.3.74 -e IP_ADDRESS_NODE_3=192.168.3.84 -e IP_ADDRESS_NODE_4=192.168.3.94 \
                                    -e PORT_ADDRESS_SEARCH_LISTEN=8001 -e PORT_ADDRESS_SHOP_LISTEN=8002 -e PORT_ADDRESS_WEB_LISTEN=8003 -e PORT_ADDRESS_MEDIA_LISTEN=8004 \
                                    -e PORT_ADDRESS_SEARCH_FORWARD=8984 -e PORT_ADDRESS_SHOP_FORWARD=8097 -e PORT_ADDRESS_WEB_FORWARD=8081 -e PORT_ADDRESS_MEDIA_FORWARD=8089 \
                                    --name load_balancer_node_4 luongquocdat01091995/network_services:load-balancer-general 

Update service at each node:

docker service update --env-add WEIGHT_SEARCH_2=1 --env-add WEIGHT_SEARCH_3=2 --env-add WEIGHT_SEARCH_4=4 \
                      --env-add WEIGHT_SHOP_2=1 --env-add WEIGHT_SHOP_3=2 --env-add WEIGHT_SHOP_4=2 \
                      --env-add WEIGHT_WEB_2=1 --env-add WEIGHT_WEB_3=2 --env-add WEIGHT_WEB_4=2 \
                      --env-add WEIGHT_MEDIA_2=1 --env-add WEIGHT_MEDIA_3=2 --env-add WEIGHT_MEDIA_4=2 \
                      load_balancer_node_2

docker service update --env-add WEIGHT_SEARCH_2=1 --env-add WEIGHT_SEARCH_3=2 --env-add WEIGHT_SEARCH_4=2 \
                      --env-add WEIGHT_SHOP_2=1 --env-add WEIGHT_SHOP_3=2 --env-add WEIGHT_SHOP_4=2 \
                      --env-add WEIGHT_WEB_2=1 --env-add WEIGHT_WEB_3=2 --env-add WEIGHT_WEB_4=2 \
                      --env-add WEIGHT_MEDIA_2=1 --env-add WEIGHT_MEDIA_3=2 --env-add WEIGHT_MEDIA_4=2 \
                      load_balancer_node_3

docker service update --env-add WEIGHT_SEARCH_2=1 --env-add WEIGHT_SEARCH_3=2 --env-add WEIGHT_SEARCH_4=2 \
                      --env-add WEIGHT_SHOP_2=1 --env-add WEIGHT_SHOP_3=2 --env-add WEIGHT_SHOP_4=2 \
                      --env-add WEIGHT_WEB_2=1 --env-add WEIGHT_WEB_3=2 --env-add WEIGHT_WEB_4=2 \
                      --env-add WEIGHT_MEDIA_2=1 --env-add WEIGHT_MEDIA_3=2 --env-add WEIGHT_MEDIA_4=2 \
                      load_balancer_node_4               

-------------------------------------------------------------------

container: search_client_2
image: service-client
env vars:

ENV IP_ADDRESS 192.168.3.74
ENV USER_NO 100
ENV MEDIA_SERVICE 0

Create client:

docker service create --constraint node.labels.node_number==2 \
                      -e IP_ADDRESS=192.168.3.74 \
                      -e PORT_NUMBER=8001 \
                      --publish mode=host,target=8101,published=8101 \
                      -e USER_NO=100 -e MEDIA_SERVICE=0 --name search_client_2 luongquocdat01091995/service-client

Update client: 

docker service update --env-add USER_NO=60 search_client_2

-------------------------------------------------------------------

container: shop_client_2
image: service-client
env vars:

ENV IP_ADDRESS 192.168.3.74
ENV USER_NO 100
ENV MEDIA_SERVICE 0

Create client:

docker service create --constraint node.labels.node_number==2 \
                      -e IP_ADDRESS=192.168.3.74 \
                      -e PORT_NUMBER=8002 \
                      --publish mode=host,target=8102,published=8102 \
                      -e USER_NO=100 -e MEDIA_SERVICE=0 --name shop_client_2 luongquocdat01091995/network_services:service-client

Update client: 

docker service update --env-add USER_NO=100 shop_client_2

-------------------------------------------------------------------

container: web_client_2
image: service-client
env vars:

ENV IP_ADDRESS 192.168.3.74
ENV USER_NO 100
ENV MEDIA_SERVICE 0

docker service create --constraint node.labels.node_number==2 \
                      -e IP_ADDRESS=192.168.3.74 \
                      -e PORT_NUMBER=8003 \
                      --publish mode=host,target=8103,published=8103 \
                      -e USER_NO=100 -e MEDIA_SERVICE=0 --name web_client_2 luongquocdat01091995/network_services:service-client

docker service update --env-add USER_NO=100 web_client_2

-------------------------------------------------------------------

container: media_client_2
image: service-client
env vars:

ENV IP_ADDRESS 192.168.3.74
ENV USER_NO 100
ENV MEDIA_SERVICE 0

docker service create --constraint node.labels.node_number==2 \
                      -e IP_ADDRESS=192.168.3.74 \
                      -e PORT_NUMBER=8004 \
                      --publish mode=host,target=8104,published=8104 \
                      -e USER_NO=100 -e MEDIA_SERVICE=1 --name media_client_2 luongquocdat01091995/network_services:service-client

docker service update --env-add USER_NO=100 media_client_2

-------------------------------------------------------------------

container: search_client_3
image: service-client
env vars:

ENV IP_ADDRESS 192.168.3.84
ENV USER_NO 100
ENV MEDIA_SERVICE 0

docker service create --constraint node.labels.node_number==3 \
                      -e IP_ADDRESS=192.168.3.84 \
                      -e PORT_NUMBER=8001 \
                      --publish mode=host,target=8101,published=8101 \
                      -e USER_NO=100 -e MEDIA_SERVICE=0 --name search_client_3 luongquocdat01091995/network_services:service-client

docker service update --env-add USER_NO=100 search_client_3

-------------------------------------------------------------------

container: shop_client_3
image: service-client
env vars:

ENV IP_ADDRESS 192.168.3.84
ENV USER_NO 100
ENV MEDIA_SERVICE 0

docker service create --constraint node.labels.node_number==3 \
                      -e IP_ADDRESS=192.168.3.84 \
                      -e PORT_NUMBER=8002 \
                      --publish mode=host,target=8102,published=8102 \
                      -e USER_NO=100 -e MEDIA_SERVICE=0 --name shop_client_3 luongquocdat01091995/network_services:service-client

docker service update --env-add USER_NO=100 shop_client_3

-------------------------------------------------------------------

container: web_client_3
image: service-client
env vars:

ENV IP_ADDRESS 192.168.3.84
ENV USER_NO 100
ENV MEDIA_SERVICE 0

docker service create --constraint node.labels.node_number==3 \
                      -e IP_ADDRESS=192.168.3.84 \
                      -e PORT_NUMBER=8003 \
                      --publish mode=host,target=8103,published=8103 \
                      -e USER_NO=100 -e MEDIA_SERVICE=0 --name web_client_3 luongquocdat01091995/network_services:service-client

docker service update --env-add USER_NO=100 web_client_3

-------------------------------------------------------------------

container: media_client_3
image: service-client
env vars:

ENV IP_ADDRESS 192.168.3.84
ENV USER_NO 100
ENV MEDIA_SERVICE 0

docker service create --constraint node.labels.node_number==3 \
                      -e IP_ADDRESS=192.168.3.84 \
                      -e PORT_NUMBER=8004 \
                      --publish mode=host,target=8104,published=8104 \
                      -e USER_NO=100 -e MEDIA_SERVICE=1 --name media_client_3 luongquocdat01091995/network_services:service-client

docker service update --env-add USER_NO=100 media_client_3

-------------------------------------------------------------------

container: search_client_4
image: service-client
env vars:

ENV IP_ADDRESS 192.168.3.94
ENV USER_NO 100
ENV MEDIA_SERVICE 0

docker service create --constraint node.labels.node_number==4 \
                      -e IP_ADDRESS=192.168.3.94 \
                      -e PORT_NUMBER=8983 \
                      --publish mode=host,target=9083,published=9083 \
                      -e USER_NO=100 -e MEDIA_SERVICE=0 --name search_client_4 luongquocdat01091995/network_services:service-client

docker service update --env-add USER_NO=100 search_client_4

-------------------------------------------------------------------

container: shop_client_4
image: service-client
env vars:

ENV IP_ADDRESS 192.168.3.94
ENV USER_NO 100
ENV MEDIA_SERVICE 0

docker service create --constraint node.labels.node_number==4 \
                      -e IP_ADDRESS=192.168.3.94 \
                      -e PORT_NUMBER=8096 \
                      --publish mode=host,target=8196,published=8196 \
                      -e USER_NO=100 -e MEDIA_SERVICE=0 --name shop_client_4 luongquocdat01091995/network_services:service-client

docker service update --env-add USER_NO=100 shop_client_4

-------------------------------------------------------------------

container: web_client_4
image: service-client
env vars:

ENV IP_ADDRESS 192.168.3.94
ENV USER_NO 100
ENV MEDIA_SERVICE 0

create service:

docker service create --constraint node.labels.node_number==4 \
                      -e IP_ADDRESS=192.168.3.94 \
                      -e PORT_NUMBER=8003 \
                      --publish mode=host,target=8103,published=8103 \
                      -e USER_NO=100 -e MEDIA_SERVICE=0 --name web_client_4 luongquocdat01091995/network_services:service-client

update service:

docker service update --env-add USER_NO=50 web_client_4

-------------------------------------------------------------------

container: media_client_4
image: service-client
env vars:

ENV IP_ADDRESS 192.168.3.94
ENV USER_NO 100
ENV MEDIA_SERVICE 0

docker service create --constraint node.labels.node_number==4 \
                      -e IP_ADDRESS=192.168.3.94 \
                      -e PORT_NUMBER=8004 \
                      --publish mode=host,target=8104,published=8104 \
                      -e USER_NO=100 -e MEDIA_SERVICE=1 --name media_client_4 luongquocdat01091995/network_services:service-client

docker service update --env-add USER_NO=100 media_client_4
