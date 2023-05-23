FROM minio/minio:RELEASE.2023-01-02T09-40-09Z

CMD ["minio", "server", "--address", "minio:9000", "--console-address", "minio:9001", "/minio_data"]
