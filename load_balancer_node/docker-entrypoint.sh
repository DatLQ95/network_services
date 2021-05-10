#!/bin/bash
echo build starting nginx config


echo replacing ___WEIGHT_SEARCH_LB_2___/$WEIGHT_SEARCH_LB_2
echo replacing ___WEIGHT_SEARCH_LB_3___/$WEIGHT_SEARCH_LB_3
echo replacing ___WEIGHT_SEARCH_LB_4___/$WEIGHT_SEARCH_LB_4

echo replacing ___WEIGHT_WEB_LB_2___/$WEIGHT_WEB_LB_2
echo replacing ___WEIGHT_WEB_LB_3___/$WEIGHT_WEB_LB_3
echo replacing ___WEIGHT_WEB_LB_4___/$WEIGHT_WEB_LB_4

echo replacing ___WEIGHT_SHOP_LB_2___/$WEIGHT_SHOP_LB_2
echo replacing ___WEIGHT_SHOP_LB_3___/$WEIGHT_SHOP_LB_3
echo replacing ___WEIGHT_SHOP_LB_4___/$WEIGHT_SHOP_LB_4

echo replacing ___WEIGHT_MEDIA_LB_2___/$WEIGHT_MEDIA_LB_2
echo replacing ___WEIGHT_MEDIA_LB_3___/$WEIGHT_MEDIA_LB_3
echo replacing ___WEIGHT_MEDIA_LB_4___/$WEIGHT_MEDIA_LB_4

sed -i "s/___WEIGHT_SEARCH_LB_2___/$WEIGHT_SEARCH_LB_2/g" /etc/nginx/nginx.conf
sed -i "s/___WEIGHT_SEARCH_LB_3___/$WEIGHT_SEARCH_LB_3/g" /etc/nginx/nginx.conf
sed -i "s/___WEIGHT_SEARCH_LB_4___/$WEIGHT_SEARCH_LB_4/g" /etc/nginx/nginx.conf

sed -i "s/___WEIGHT_WEB_LB_2___/$WEIGHT_WEB_LB_2/g" /etc/nginx/nginx.conf
sed -i "s/___WEIGHT_WEB_LB_3___/$WEIGHT_WEB_LB_3/g" /etc/nginx/nginx.conf
sed -i "s/___WEIGHT_WEB_LB_4___/$WEIGHT_WEB_LB_4/g" /etc/nginx/nginx.conf

sed -i "s/___WEIGHT_SHOP_LB_2___/$WEIGHT_SHOP_LB_2/g" /etc/nginx/nginx.conf
sed -i "s/___WEIGHT_SHOP_LB_3___/$WEIGHT_SHOP_LB_3/g" /etc/nginx/nginx.conf
sed -i "s/___WEIGHT_SHOP_LB_4___/$WEIGHT_SHOP_LB_4/g" /etc/nginx/nginx.conf

sed -i "s/___WEIGHT_MEDIA_LB_2___/$WEIGHT_MEDIA_LB_2/g" /etc/nginx/nginx.conf
sed -i "s/___WEIGHT_MEDIA_LB_3___/$WEIGHT_MEDIA_LB_3/g" /etc/nginx/nginx.conf
sed -i "s/___WEIGHT_MEDIA_LB_4___/$WEIGHT_MEDIA_LB_4/g" /etc/nginx/nginx.conf

sed -i "s/___IP_ADDRESS_NODE_2___/$IP_ADDRESS_NODE_2/g" /etc/nginx/nginx.conf
sed -i "s/___IP_ADDRESS_NODE_3___/$IP_ADDRESS_NODE_3/g" /etc/nginx/nginx.conf
sed -i "s/___IP_ADDRESS_NODE_4___/$IP_ADDRESS_NODE_4/g" /etc/nginx/nginx.conf

sed -i "s/___PORT_ADDRESS_SEARCH___/$PORT_ADDRESS_SEARCH/g" /etc/nginx/nginx.conf
sed -i "s/___PORT_ADDRESS_SHOP___/$PORT_ADDRESS_SHOP/g" /etc/nginx/nginx.conf
sed -i "s/___PORT_ADDRESS_WEB___/$PORT_ADDRESS_WEB/g" /etc/nginx/nginx.conf
sed -i "s/___PORT_ADDRESS_MEDIA___/$PORT_ADDRESS_MEDIA/g" /etc/nginx/nginx.conf

sed -i "s/___PORT_ADDRESS_SEARCH_LB___/$PORT_ADDRESS_SEARCH_LB/g" /etc/nginx/nginx.conf
sed -i "s/___PORT_ADDRESS_SHOP_LB___/$PORT_ADDRESS_SHOP_LB/g" /etc/nginx/nginx.conf
sed -i "s/___PORT_ADDRESS_WEB_LB___/$PORT_ADDRESS_WEB_LB/g" /etc/nginx/nginx.conf
sed -i "s/___PORT_ADDRESS_MEDIA_LB___/$PORT_ADDRESS_MEDIA_LB/g" /etc/nginx/nginx.conf


cat /etc/nginx/nginx.conf

nginx -g 'daemon off;'