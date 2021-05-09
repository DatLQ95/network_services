FROM nginx:1.19
# Copy  nginx config file to container
COPY conf/nginx.conf /etc/nginx/nginx.conf

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

COPY docker-entrypoint.sh /root/service.sh
CMD ["/bin/bash","/root/service.sh"]