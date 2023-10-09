ARG VERSION='v2.2.8'
FROM milvusdb/milvus:${VERSION}
RUN apt-get update -y && \
    apt-get install -y --no-install-recommends \
    openssl nodejs
RUN mkdir -p /entrypoint \
    /etc/ssl/certs
COPY .devcontainer/certs/certs.sh /tmp/certs.sh
COPY .devcontainer/healthcheck/healthcheck.js /opt/healthcheck/healthcheck.js
RUN /bin/bash /tmp/certs.sh  "-s" "$(hostname)" "/etc/ssl/certs"
