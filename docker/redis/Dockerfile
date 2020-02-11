FROM redis:5.0.7

RUN apt-get update ;\
    apt-get install dos2unix gettext-base

COPY redis.conf /usr/local/etc/redis/redis.conf.tmp

COPY docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh
RUN dos2unix /usr/local/bin/docker-entrypoint.sh
RUN chmod +x /usr/local/bin/docker-entrypoint.sh
RUN ln -sf /usr/local/bin/docker-entrypoint.sh /