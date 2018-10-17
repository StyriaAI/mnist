FROM python:3.6

RUN apt-get update \
    && apt-get install -y locales \
    && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# set timezone
RUN echo Europe/Zagreb > /etc/timezone && \
    rm -f /etc/localtime && \
    dpkg-reconfigure -f noninteractive tzdata

# set locale
RUN echo LC_ALL=en_US.UTF-8 >> /etc/environment && \
    echo en_US.UTF-8 UTF-8 >> /etc/locale.gen && \
    echo LANG=en_US.UTF-8 > /etc/locale.conf && \
    locale-gen en_US.UTF-8

# copy code
COPY . /app

# install dependencies
RUN pip3 install -r /app/requirements.txt

# basic configuration
ENV UWSGI_HTTP_SOCKET=0.0.0.0:8080 \
    UWSGI_MODULE=runner \
    UWSGI_CALLABLE=app \
    UWSGI_THREADS=5 \
    UWSGI_ENABLE_THREADS=true \
    PYTHONPATH=/app

# expose uwsgi port
EXPOSE 8080

# run uwsgi
CMD uwsgi
