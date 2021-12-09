from fastapi.security.api_key import APIKeyHeader
from fastapi import Security

api_key_header = Security(APIKeyHeader(name="Authorization", auto_error=False))
