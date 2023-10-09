#!/bin/bash
#/**
# *    Licensed under the Apache License, Version 2.0 (the "License");
# *    you may not use this file except in compliance with the License.
# *    You may obtain a copy of the License at
# *
# *        http://www.apache.org/licenses/LICENSE-2.0
# *
# *    Unless required by applicable law or agreed to in writing, software
# *    distributed under the License is distributed on an "AS IS" BASIS,
# *    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# *    See the License for the specific language governing permissions and
# *    limitations under the License.
# */
#/bin/bash -c etcd --data-dir='/etcd' --name "${ETCD_NAME}" \
#      --initial-cluster "${ETCD_NAME}"='http://127.0.0.1:2380' \
#      --initial-advertise-peer-urls 'http://127.0.0.1:2380' \
#      --advertise-peer-urls 'http://0.0.0.0:2380' \
#      --cert-file="/etc/ssl/certs/etcd/server.crt" --key-file="/etc/ssl/certs/etcd/server.key" \
#      --trusted-ca-file "/etc/ssl/certs/etcd/server.pem" \
#      --cipher-suites TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256,TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384 \
#      --advertise-client-urls "${ETCD_ADVERTISE_CLIENT_URLS:-http://127.0.0.1:2379}" \
#      --listen-client-urls "${ETCD_LISTEN_CLIENT_URLS:-http://0.0.0.0:2379}" \
#      --discovery http://etcd-discovery:8087 && wait $!
########################################################################
# create a dot directory certs in root of project for key generation
#rm -rf "/etc/ssl/certs/*" && wait $!
while [[ ! -f "/etc/ssl/certs/etcd/$(hostname).crt" ]]; do
  sleep 1
  /bin/bash /tmp/certs.sh  "-s" "$(hostname)" "/etc/ssl/certs/etcd" && wait $!
#  cp -r run/secrets/* /etc/ssl/certs/etcd/ && wait $!
done
# Init etcd cluster with discovery
#/bin/bash -c etcd --name="${ETCD_NAME}" \
#      --data-dir="${ETCD_DATA_DIR}" \
#      --wal-dir="${ETCD_WAL_DIR}" \
#      --initial-cluster="${ETCD_INITIAL_CLUSTER}" \
#      --advertise-client-urls="${ETCD_ADVERTISE_CLIENT_URLS}" \
#      --listen-client-urls="${ETCD_LISTEN_CLIENT_URLS}" \
#      --discovery "${DISCOVERY_URL}" && wait $!
# Init etcd cluster with environment variables
etcd && wait $!
#      --listen-client-urls=http://0.0.0.0:2379 \
#      --advertise-client-urls="http://etcd-00:2379,http://etcd-01:2379,http://etcd-02:2379" \
#      --initial-advertise-peer-urls="http://${ETCD_NAME}:2380" \
#      --listen-peer-urls=http://0.0.0.0:2380 \
#      --initial-cluster-token etcd-cluster-1
# Config file init for etcd cluster
#/bin/bash -c etcd --config-file="/etc/etcd/etcd.conf.yml" && wait $!
# Etcdctl member list for etcd cluster
etcdctl --endpoints=${ETCD_ENDPOINTS} member list && wait $!
