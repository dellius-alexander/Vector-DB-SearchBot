ARG VERSION=latest
ARG HOSTNAME="localhost"
FROM nginx:${VERSION}
EXPOSE 80
COPY .devcontainer/config/nginx/nginx.conf /etc/nginx/nginx.conf
HEALTHCHECK --interval=30s --timeout=3s --retries=5  CMD curl --fail "http://${HOSTNAME}" || exit 1

