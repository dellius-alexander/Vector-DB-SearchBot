# Milvus API Service

## Authentication

```bash
curl --request GET \
    --url "${MILVUS_HOST}:${MILVUS_PORT}/v1/vector/collections" \
    --header "Authorization: Bearer ${TOKEN}" \
    --header "accept: application/json" \
    --header "content-type: application/json"
```
