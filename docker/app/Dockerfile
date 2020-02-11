FROM node:13.8.0-stretch-slim

RUN apt-get update ;\
    apt-get install -y dos2unix python3 python3-pip

COPY docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh
RUN dos2unix /usr/local/bin/docker-entrypoint.sh
RUN chmod +x /usr/local/bin/docker-entrypoint.sh
RUN ln -sf /usr/local/bin/docker-entrypoint.sh /