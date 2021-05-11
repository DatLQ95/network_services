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

//TODO: in the image in dockerhub the video is in gitlfs, therefore we need to build locally in each node and then run docker swarm!

-------------------------------------------------------------------

container: load_balancer
image: load-balancer
port: 8984, 8081, 8097, 8089
env vars:

ENV WEIGHT_SEARCH_LB_2 1
ENV WEIGHT_SEARCH_LB_3 2
ENV WEIGHT_SEARCH_LB_4 3

ENV WEIGHT_SHOP_LB_2 1
ENV WEIGHT_SHOP_LB_3 2
ENV WEIGHT_SHOP_LB_4 3

ENV WEIGHT_WEB_LB_2 1
ENV WEIGHT_WEB_LB_3 2
ENV WEIGHT_WEB_LB_4 3

ENV WEIGHT_MEDIA_LB_2 1
ENV WEIGHT_MEDIA_LB_3 2
ENV WEIGHT_MEDIA_LB_4 3

ENV IP_ADDRESS_NODE_2 131.155.35.52
ENV IP_ADDRESS_NODE_3 131.155.35.53
ENV IP_ADDRESS_NODE_4 131.155.35.54

ENV PORT_ADDRESS_SEARCH_LB 8984
ENV PORT_ADDRESS_SHOP_LB 8097
ENV PORT_ADDRESS_WEB_LB 8081
ENV PORT_ADDRESS_MEDIA_LB 8089

ENV PORT_ADDRESS_SEARCH_SERVER 8983
ENV PORT_ADDRESS_SHOP_SERVER 8096
ENV PORT_ADDRESS_WEB_SERVER 8080
ENV PORT_ADDRESS_MEDIA_SERVER 8088

Create service
docker service create --mode global --publish mode=host,target=8984,published=8984 \
                                    --publish mode=host,target=8081,published=8081 \
                                    --publish mode=host,target=8097,published=8097 \
                                    --publish mode=host,target=8089,published=8089 \
                                    -e WEIGHT_SEARCH_LB_2=1 -e WEIGHT_SEARCH_LB_3=2 -e WEIGHT_SEARCH_LB_4=2 \
                                    -e WEIGHT_SHOP_LB_2=1 -e WEIGHT_SHOP_LB_3=2 -e WEIGHT_SHOP_LB_4=2 \
                                    -e WEIGHT_WEB_LB_2=1 -e WEIGHT_WEB_LB_3=2 -e WEIGHT_WEB_LB_4=2 \
                                    -e WEIGHT_MEDIA_LB_2=1 -e WEIGHT_MEDIA_LB_3=2 -e WEIGHT_MEDIA_LB_4=2 \
                                    -e IP_ADDRESS_NODE_2=131.155.35.52 -e IP_ADDRESS_NODE_3=131.155.35.53 -e IP_ADDRESS_NODE_4=131.155.35.54 \
                                    -e PORT_ADDRESS_SEARCH_LB=8984 -e PORT_ADDRESS_WEB_LB=8081 -e PORT_ADDRESS_SHOP_LB=8097 -e PORT_ADDRESS_MEDIA_LB=8089 \
                                    -e PORT_ADDRESS_SEARCH_SERVER=8983 -e PORT_ADDRESS_SHOP_SERVER=8096 -e PORT_ADDRESS_WEB_SERVER=8080 -e PORT_ADDRESS_MEDIA_SERVER=8088 \
                                    --name load_balancer luongquocdat01091995/network_services:load-balancer 

Update service at each load balancer:
docker service update --env-add WEIGHT_SEARCH_2=1 --env-add WEIGHT_SEARCH_3=2 --env-add WEIGHT_SEARCH_4=2 \
                      --env-add WEIGHT_SHOP_2=1 --env-add WEIGHT_SHOP_3=2 --env-add WEIGHT_SHOP_4=2 \
                      --env-add WEIGHT_WEB_2=1 --env-add WEIGHT_WEB_3=2 --env-add WEIGHT_WEB_4=2 \
                      --env-add WEIGHT_MEDIA_2=1 --env-add WEIGHT_MEDIA_3=2 --env-add WEIGHT_MEDIA_4=2 \
                      load_balancer

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

ENV IP_ADDRESS_NODE_2 131.155.35.52
ENV IP_ADDRESS_NODE_3 131.155.35.53
ENV IP_ADDRESS_NODE_4 131.155.35.54

ENV PORT_ADDRESS_SEARCH 8001
ENV PORT_ADDRESS_SHOP 8002
ENV PORT_ADDRESS_WEB 8003
ENV PORT_ADDRESS_MEDIA 8004

ENV PORT_ADDRESS_SEARCH_LB 8984
ENV PORT_ADDRESS_SHOP_LB 8097
ENV PORT_ADDRESS_WEB_LB 8081
ENV PORT_ADDRESS_MEDIA_LB 8089

Create load balancer at each node:

docker service create --mode global --publish mode=host,target=8001,published=8001 \
                                    --publish mode=host,target=8002,published=8002 \
                                    --publish mode=host,target=8003,published=8003 \
                                    --publish mode=host,target=8004,published=8004 \
                                    -e WEIGHT_SEARCH_2=1 -e WEIGHT_SEARCH_3=2 -e WEIGHT_SEARCH_4=2 \
                                    -e WEIGHT_SHOP_2=1 -e WEIGHT_SHOP_3=2 -e WEIGHT_SHOP_4=2 \
                                    -e WEIGHT_WEB_2=1 -e WEIGHT_WEB_3=2 -e WEIGHT_WEB_4=2 \
                                    -e WEIGHT_MEDIA_2=1 -e WEIGHT_MEDIA_3=2 -e WEIGHT_MEDIA_4=2 \
                                    -e IP_ADDRESS_NODE_2=131.155.35.52 -e IP_ADDRESS_NODE_3=131.155.35.53 -e IP_ADDRESS_NODE_4=131.155.35.54 \
                                    -e PORT_ADDRESS_SEARCH=8001 -e PORT_ADDRESS_SHOP=8002 -e PORT_ADDRESS_WEB=8003 -e PORT_ADDRESS_MEDIA=8004 \
                                    -e PORT_ADDRESS_SEARCH_LB=8984 -e PORT_ADDRESS_SHOP_LB=8097 -e PORT_ADDRESS_WEB_LB=8081 -e PORT_ADDRESS_MEDIA_LB=8089 \
                                    --name load_balancer_node luongquocdat01091995/network_services:load-balancer-node 

Update service at each node:

docker service update --env-add WEIGHT_SEARCH_2=1 --env-add WEIGHT_SEARCH_3=2 --env-add WEIGHT_SEARCH_4=2 \
                      --env-add WEIGHT_SHOP_2=1 --env-add WEIGHT_SHOP_3=2 --env-add WEIGHT_SHOP_4=2 \
                      --env-add WEIGHT_WEB_2=1 --env-add WEIGHT_WEB_3=2 --env-add WEIGHT_WEB_4=2 \
                      --env-add WEIGHT_MEDIA_2=1 --env-add WEIGHT_MEDIA_3=2 --env-add WEIGHT_MEDIA_4=2 \
                      load_balancer_node 

-------------------------------------------------------------------

container: search_client_2
image: service-client
env vars:

ENV IP_ADDRESS 131.155.35.52
ENV USER_NO 100
ENV MEDIA_SERVICE 0

Create client:

docker service create --constraint node.labels.node_number==2 \
                      -e IP_ADDRESS=192.168.3.84 \
                      -e PORT_NUMBER=8001 \
                      -e USER_NO=100 -e MEDIA_SERVICE=0 --name search_client_2 luongquocdat01091995/network_services:service-client

Update client: 

docker service update --constraint node.labels.node_number==2 \
                      --env-add IP_ADDRESS=131.155.35.52 \
                      --env-add PORT_NUMBER=8001 \
                      --env-add USER_NO=100 --env-add MEDIA_SERVICE=0 --name search_client_2

-------------------------------------------------------------------

container: shop_client_2
image: service-client
env vars:

ENV IP_ADDRESS 131.155.35.52
ENV USER_NO 100
ENV MEDIA_SERVICE 0

docker service create --constraint node.labels.node_number==2 \
                      -e IP_ADDRESS=131.155.35.52 \
                      -e PORT_NUMBER=8002 \
                      -e USER_NO=100 -e MEDIA_SERVICE=0 --name shop_client_2 luongquocdat01091995/network_services:service-client

-------------------------------------------------------------------

container: web_client_2
image: service-client
env vars:

ENV IP_ADDRESS 131.155.35.52
ENV USER_NO 100
ENV MEDIA_SERVICE 0

docker service create --constraint node.labels.node_number=2 \
                      -e IP_ADDRESS=131.155.35.52 \
                      -e PORT_NUMBER=8003 \
                      -e USER_NO=100 -e MEDIA_SERVICE=0 --name web_client_2 luongquocdat01091995/network_services:service-client

-------------------------------------------------------------------

container: media_client_2
image: service-client
env vars:

ENV IP_ADDRESS 131.155.35.52
ENV USER_NO 100
ENV MEDIA_SERVICE 0

docker service create --constraint node.labels.node_number=2 \
                      -e IP_ADDRESS=131.155.35.52 \
                      -e PORT_NUMBER=8004 \
                      -e USER_NO=100 -e MEDIA_SERVICE=0 --name media_client_2 luongquocdat01091995/network_services:service-client

-------------------------------------------------------------------

container: search_client_3
image: service-client
env vars:

ENV IP_ADDRESS 131.155.35.53
ENV USER_NO 100
ENV MEDIA_SERVICE 0

docker service create --constraint node.labels.node_number=3 \
                      -e IP_ADDRESS=131.155.35.53 \
                      -e PORT_NUMBER=8001 \
                      -e USER_NO=100 -e MEDIA_SERVICE=0 --name search_client_3 luongquocdat01091995/network_services:service-client

-------------------------------------------------------------------

container: shop_client_3
image: service-client
env vars:

ENV IP_ADDRESS 131.155.35.53
ENV USER_NO 100
ENV MEDIA_SERVICE 0

docker service create --constraint node.labels.node_number=3 \
                      -e IP_ADDRESS=131.155.35.53 \
                      -e PORT_NUMBER=8002 \
                      -e USER_NO=100 -e MEDIA_SERVICE=0 --name shop_client_3 luongquocdat01091995/network_services:service-client

-------------------------------------------------------------------

container: web_client_3
image: service-client
env vars:

ENV IP_ADDRESS 131.155.35.53
ENV USER_NO 100
ENV MEDIA_SERVICE 0

docker service create --constraint node.labels.node_number=3 \
                      -e IP_ADDRESS=131.155.35.53 \
                      -e PORT_NUMBER=8003 \
                      -e USER_NO=100 -e MEDIA_SERVICE=0 --name web_client_3 luongquocdat01091995/network_services:service-client

-------------------------------------------------------------------

container: media_client_3
image: service-client
env vars:

ENV IP_ADDRESS 131.155.35.53
ENV USER_NO 100
ENV MEDIA_SERVICE 0

docker service create --constraint node.labels.node_number=3 \
                      -e IP_ADDRESS=131.155.35.53 \
                      -e PORT_NUMBER=8004 \
                      -e USER_NO=100 -e MEDIA_SERVICE=0 --name media_client_3 luongquocdat01091995/network_services:service-client

-------------------------------------------------------------------

container: search_client_4
image: service-client
env vars:

ENV IP_ADDRESS 131.155.35.54
ENV USER_NO 100
ENV MEDIA_SERVICE 0

docker service create --constraint node.labels.node_number=4 \
                      -e IP_ADDRESS=131.155.35.53 \
                      -e PORT_NUMBER=8001 \
                      -e USER_NO=100 -e MEDIA_SERVICE=0 --name search_client_4 luongquocdat01091995/network_services:service-client

-------------------------------------------------------------------

container: shop_client_4
image: service-client
env vars:

ENV IP_ADDRESS 131.155.35.54
ENV USER_NO 100
ENV MEDIA_SERVICE 0

docker service create --constraint node.labels.node_number=4 \
                      -e IP_ADDRESS=131.155.35.53 \
                      -e PORT_NUMBER=8002 \
                      -e USER_NO=100 -e MEDIA_SERVICE=0 --name shop_client_4 luongquocdat01091995/network_services:service-client

-------------------------------------------------------------------

container: web_client_4
image: service-client
env vars:

ENV IP_ADDRESS 131.155.35.54
ENV USER_NO 100
ENV MEDIA_SERVICE 0

docker service create --constraint node.labels.node_number=4 \
                      -e IP_ADDRESS=131.155.35.53 \
                      -e PORT_NUMBER=8003 \
                      -e USER_NO=100 -e MEDIA_SERVICE=0 --name web_client_4 luongquocdat01091995/network_services:service-client

-------------------------------------------------------------------

container: media_client_4
image: service-client
env vars:

ENV IP_ADDRESS 131.155.35.54
ENV USER_NO 100
ENV MEDIA_SERVICE 0

docker service create --constraint node.labels.node_number=4 \
                      -e IP_ADDRESS=131.155.35.53 \
                      -e PORT_NUMBER=8004 \
                      -e USER_NO=100 -e MEDIA_SERVICE=0 --name media_client_4 luongquocdat01091995/network_services:service-client
