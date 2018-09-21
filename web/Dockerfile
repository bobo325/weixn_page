FROM registry.registry:5000/nginx3:latest

RUN mkdir -p /data \
    && mkdir -p /data/log \
    && mkdir -p /data/www/static_file \
    && mkdir -p /data/certs

WORKDIR /data

ADD config /data/config
ADD const /data/const
ADD flask_app /data/flask_app
ADD intercept /data/intercept
ADD logs /data/logs
ADD migrations /data/migrations
ADD model /data/model
ADD proj /data/proj
ADD route /data/route
ADD schema /data/schema
ADD service /data/service
ADD sql /data/sql
ADD www /data/www
ADD static_file /data/static_file
ADD test /data/test
ADD util /data/util
ADD run.py /data
ADD manage.py /data/manage.py
ADD requirements.txt /data

# 使用本地的配置文件，替换
ADD nginx_web.conf /etc/nginx/nginx.conf
ADD supervisord_web.conf /etc/supervisor/supervisord.conf
ADD 01_init_static_file.sh /docker-entrypoint.d
RUN chmod 755 /docker-entrypoint.d/*

RUN pip install -i https://mirrors.ustc.edu.cn/pypi/web/simple/ -r /data/requirements.txt

VOLUME /data/www/static_file
VOLUME /data/log
VOLUME /data/certs

EXPOSE 80 8000

CMD /usr/bin/supervisord -n