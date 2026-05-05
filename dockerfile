FROM bde2020/hadoop-namenode:2.0.0-hadoop3.2.1-java8
# Installe Python 2.7
RUN apt-get update && \
    apt-get install -y --allow-unauthenticated python2.7 && \
    ln -s /usr/bin/python2.7 /usr/bin/python