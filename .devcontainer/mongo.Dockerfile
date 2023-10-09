FROM mongo:5.0.16
EXPOSE 27017
COPY .devcontainer/config/mongo/mongo-init.js*  /docker-entrypoint-initdb.d/
COPY .devcontainer/config/mongo/mongod.conf*  /etc/
RUN apt-get update -y
RUN mkdir -p /opt/healthcheck
COPY .devcontainer/healthcheck/healthcheck.js /opt/healthcheck/healthcheck.js
HEALTHCHECK --interval=15s --timeout=15s --start-period=30s \
 CMD node /opt/healthcheck/healthcheck.js
