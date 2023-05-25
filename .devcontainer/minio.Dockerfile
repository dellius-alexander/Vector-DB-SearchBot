ARG VARIANT=RELEASE.2023-01-02T09-40-09Z
###################################################################################################
FROM minio/minio:${VARIANT}
###################################################################################################
ARG MINIO_ROOT_USER="minioadmin"
ARG MINIO_ROOT_PASSWORD="minioadmin"
###################################################################################################
# The MinIO Client allows you to work with your MinIO server from the commandline.
# Download the mc client and install it to a location on your system PATH such
# as /usr/local/bin. You can alternatively run the binary from the download location.
RUN curl -fsSL https://dl.min.io/client/mc/release/linux-amd64/mc -o /tmp/mc && \
    chmod +x /tmp/mc && \
    mv /tmp/mc /usr/local/bin/mc
#RUN #minio server --address "0.0.0.0:9000" --console-address "0.0.0.0:9001" /minio_data
# Use mc alias set to create a new alias associated to your local deployment. You \
# can run mc commands against this alias:
# - The mc alias set takes four arguments:
#
#   - The name of the alias
#   - The hostname or IP address and port of the MinIO server
#   - The Access Key for a MinIO user
#   - The Secret Key for a MinIO user
#   - For additional details about this command,
#     see [mc alias set](https://min.io/docs/minio/linux/reference/minio-mc/mc-alias-set.html#alias).
#RUN mc alias set local http://127.0.0.1:9000 ${MINIO_ROOT_USER} ${MINIO_ROOT_PASSWORD}
#RUN mc admin info local
#RUN mc admin heal local
#RUN mc admin update ${MINIO_ROOT_USER}
#RUN mc admin user add local ${MINIO_ROOT_USER} ${MINIO_ROOT_PASSWORD}

CMD ["minio", "server", "--address", "minio:9000", "--console-address", "minio:9001", "/minio_data"]
