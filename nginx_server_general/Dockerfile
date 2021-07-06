ARG DEBIAN_VERSION=stretch-slim 

##### Building stage #####
FROM debian:${DEBIAN_VERSION} as builder
MAINTAINER Dat Luong <luongquocdat.hust@gmail.com>

# Versions of nginx, rtmp-module and ffmpeg 
ARG  NGINX_VERSION=1.17.5
ARG  NGINX_RTMP_MODULE_VERSION=1.2.1
ARG  FFMPEG_VERSION=4.2.1

# Install dependencies
RUN apt-get update && \
	apt-get install -y \
		wget build-essential ca-certificates \
		openssl libssl-dev yasm \
		libpcre3-dev librtmp-dev libtheora-dev \
		libvorbis-dev libvpx-dev libfreetype6-dev \
		libmp3lame-dev libx264-dev libx265-dev && \
    rm -rf /var/lib/apt/lists/*
	
		
# Download nginx source
RUN mkdir -p /tmp/build && \
	cd /tmp/build && \
	wget https://nginx.org/download/nginx-${NGINX_VERSION}.tar.gz && \
	tar -zxf nginx-${NGINX_VERSION}.tar.gz && \
	rm nginx-${NGINX_VERSION}.tar.gz

# Build nginx with nginx-rtmp module
RUN cd /tmp/build/nginx-${NGINX_VERSION} && \
    ./configure \
        --sbin-path=/usr/local/sbin/nginx \
        --conf-path=/etc/nginx/nginx.conf \
        --error-log-path=/var/log/nginx/error.log \
        --http-log-path=/var/log/nginx/access.log \		
        --pid-path=/var/run/nginx/nginx.pid \
        --lock-path=/var/lock/nginx.lock \
        --http-client-body-temp-path=/tmp/nginx-client-body \
        --with-http_ssl_module \
        --with-threads \
		--with-http_mp4_module \
		--with-http_stub_status_module && \
    make -j $(getconf _NPROCESSORS_ONLN) && \
    make install

##### Building the final image #####
FROM debian:${DEBIAN_VERSION}

# Install dependencies
RUN apt-get update && \
	apt-get install -y \
		ca-certificates openssl libpcre3-dev \
		librtmp1 libtheora0 libvorbis-dev libmp3lame0 \
		libvpx4 libx264-dev libx265-dev && \
    rm -rf /var/lib/apt/lists/*

# Copy files from build stage to final stage	
COPY --from=builder /usr/local /usr/local
COPY --from=builder /etc/nginx /etc/nginx
COPY --from=builder /var/log/nginx /var/log/nginx
COPY --from=builder /var/lock /var/lock
COPY --from=builder /var/run/nginx /var/run/nginx
COPY ./static-html-directory/ /usr/local/nginx/html/

# Forward logs to Docker
RUN ln -sf /dev/stdout /var/log/nginx/access.log && \
    ln -sf /dev/stderr /var/log/nginx/error.log

# Copy  nginx config file to container
COPY conf/nginx.conf /etc/nginx/nginx.conf
EXPOSE 8983
EXPOSE 8080
EXPOSE 8095


CMD ["nginx", "-g", "daemon off;"]
