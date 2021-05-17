#!/bin/bash
echo build starting nginx config

sed -i "s/___WEIGHT_SEARCH_2___/$WEIGHT_SEARCH_2/g" /etc/nginx/nginx.conf
sed -i "s/___WEIGHT_SEARCH_3___/$WEIGHT_SEARCH_3/g" /etc/nginx/nginx.conf
sed -i "s/___WEIGHT_SEARCH_4___/$WEIGHT_SEARCH_4/g" /etc/nginx/nginx.conf

sed -i "s/___WEIGHT_WEB_2___/$WEIGHT_WEB_2/g" /etc/nginx/nginx.conf
sed -i "s/___WEIGHT_WEB_3___/$WEIGHT_WEB_3/g" /etc/nginx/nginx.conf
sed -i "s/___WEIGHT_WEB_4___/$WEIGHT_WEB_4/g" /etc/nginx/nginx.conf

sed -i "s/___WEIGHT_SHOP_2___/$WEIGHT_SHOP_2/g" /etc/nginx/nginx.conf
sed -i "s/___WEIGHT_SHOP_3___/$WEIGHT_SHOP_3/g" /etc/nginx/nginx.conf
sed -i "s/___WEIGHT_SHOP_4___/$WEIGHT_SHOP_4/g" /etc/nginx/nginx.conf

sed -i "s/___WEIGHT_MEDIA_2___/$WEIGHT_MEDIA_2/g" /etc/nginx/nginx.conf
sed -i "s/___WEIGHT_MEDIA_3___/$WEIGHT_MEDIA_3/g" /etc/nginx/nginx.conf
sed -i "s/___WEIGHT_MEDIA_4___/$WEIGHT_MEDIA_4/g" /etc/nginx/nginx.conf

sed -i "s/___IP_ADDRESS_NODE_2___/$IP_ADDRESS_NODE_2/g" /etc/nginx/nginx.conf
sed -i "s/___IP_ADDRESS_NODE_3___/$IP_ADDRESS_NODE_3/g" /etc/nginx/nginx.conf
sed -i "s/___IP_ADDRESS_NODE_4___/$IP_ADDRESS_NODE_4/g" /etc/nginx/nginx.conf

sed -i "s/___PORT_ADDRESS_SEARCH_LISTEN___/$PORT_ADDRESS_SEARCH_LISTEN/g" /etc/nginx/nginx.conf
sed -i "s/___PORT_ADDRESS_SHOP_LISTEN___/$PORT_ADDRESS_SHOP_LISTEN/g" /etc/nginx/nginx.conf
sed -i "s/___PORT_ADDRESS_WEB_LISTEN___/$PORT_ADDRESS_WEB_LISTEN/g" /etc/nginx/nginx.conf
sed -i "s/___PORT_ADDRESS_MEDIA_LISTEN___/$PORT_ADDRESS_MEDIA_LISTEN/g" /etc/nginx/nginx.conf

sed -i "s/___PORT_ADDRESS_SEARCH_FORWARD___/$PORT_ADDRESS_SEARCH_FORWARD/g" /etc/nginx/nginx.conf
sed -i "s/___PORT_ADDRESS_SHOP_FORWARD___/$PORT_ADDRESS_SHOP_FORWARD/g" /etc/nginx/nginx.conf
sed -i "s/___PORT_ADDRESS_WEB_FORWARD___/$PORT_ADDRESS_WEB_FORWARD/g" /etc/nginx/nginx.conf
sed -i "s/___PORT_ADDRESS_MEDIA_FORWARD___/$PORT_ADDRESS_MEDIA_FORWARD/g" /etc/nginx/nginx.conf

cat /etc/nginx/nginx.conf

nginx -g 'daemon off;'