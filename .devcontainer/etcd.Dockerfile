ARG VERSION='v3.5.5'
FROM quay.io/coreos/etcd:${VERSION}
RUN apt-get update -y && \
    apt-get install -y --no-install-recommends \
    openssl
RUN mkdir -p /entrypoint \
    /etc/etcd \
    /etc/ssl/certs/etcd  \
    /etc/systemd/system/etcd-member.service.d
RUN groupadd -r etcd && useradd -r -g etcd etcd && \
    chown -R etcd:etcd /etc/ssl/certs/etcd /etc/etcd && \
    chmod 700 /etc/ssl/certs/etcd /etc/etcd
COPY .devcontainer/certs/certs.sh /tmp/certs.sh
COPY .devcontainer/config/etcd/entrypoint.sh* /entrypoint/entrypoint.sh
#COPY .devcontainer/config/etcd/20-cl-etcd-member.conf /etc/systemd/system/etcd-member.service.d/20-cl-etcd-member.conf
#COPY .devcontainer/config/etcd/etcd.conf.yml /etc/etcd/etcd.conf.yml
RUN /bin/sh /tmp/certs.sh  "-s" "$(hostname)" "/etc/ssl/certs/etcd" && wait $!
RUN chmod +x /entrypoint/entrypoint.sh
EXPOSE 2379 2380 4001 7001
ENTRYPOINT ["/entrypoint/entrypoint.sh"]
