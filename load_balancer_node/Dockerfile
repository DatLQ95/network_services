FROM nginx:1.19
# Copy  nginx config file to container
COPY conf/nginx.conf /etc/nginx/nginx.conf

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

COPY docker-entrypoint.sh /root/service.sh
CMD ["/bin/bash","/root/service.sh"]