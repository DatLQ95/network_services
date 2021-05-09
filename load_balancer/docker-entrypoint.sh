#!/bin/bash
echo build starting nginx config


echo replacing ___WEIGHT_SEARCH_2___/$WEIGHT_SEARCH_2
echo replacing ___WEIGHT_SEARCH_3___/$WEIGHT_SEARCH_3
echo replacing ___WEIGHT_SEARCH_4___/$WEIGHT_SEARCH_4

echo replacing ___WEIGHT_WEB_2___/$WEIGHT_WEB_2
echo replacing ___WEIGHT_WEB_3___/$WEIGHT_WEB_3
echo replacing ___WEIGHT_WEB_4___/$WEIGHT_WEB_4

echo replacing ___WEIGHT_SHOP_2___/$WEIGHT_SHOP_2
echo replacing ___WEIGHT_SHOP_3___/$WEIGHT_SHOP_3
echo replacing ___WEIGHT_SHOP_4___/$WEIGHT_SHOP_4

echo replacing ___WEIGHT_MEDIA_2___/$WEIGHT_MEDIA_2
echo replacing ___WEIGHT_MEDIA_3___/$WEIGHT_MEDIA_3
echo replacing ___WEIGHT_MEDIA_4___/$WEIGHT_MEDIA_4

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

cat /etc/nginx/nginx.conf

nginx -g 'daemon off;'