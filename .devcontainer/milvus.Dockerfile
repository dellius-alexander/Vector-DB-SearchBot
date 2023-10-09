ARG VERSION='v2.2.14'
FROM milvusdb/milvus:${VERSION}
RUN apt-get update -y && \
    apt-get install -y --no-install-recommends \
    openssl
RUN mkdir -p /entrypoint \
    /etc/ssl/certs
COPY .devcontainer/certs/certs.sh /tmp/certs.sh
RUN /bin/bash /tmp/certs.sh  "-s" "$(hostname)" "/etc/ssl/certs"
EXPOSE 19530 9091
CMD ["milvus", "run", "standalone"]