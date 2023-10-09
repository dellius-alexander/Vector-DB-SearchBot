ARG VERSION='latest'
FROM quay.io/coreos/discovery.etcd.io:${VERSION}
EXPOSE 8087
#CMD ["devweb", "--addr=discovery.example.com:8087", "--host=discovery.example.com", "--etcd=proxy.example.com:2379"]
