FROM nginx
# Copy  nginx config file to container
# COPY ./templates/nginx.conf.template /etc/nginx/conf.d/mysite.template

COPY conf/nginx.conf /etc/nginx/nginx.conf

# CMD ["envsubst",  "<", "/etc/nginx/conf.d/mysite.template", ">","/etc/nginx/nginx.conf", "&&", "nginx", "-g", "daemon off;"]