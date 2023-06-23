from fastapi import Depends, FastAPI, HTTPException, status,Request
from fastapi.security import APIKeyHeader
from typing import Dict

from infrastructure.redis.redis_support import get_redis_client

api_key_header = APIKeyHeader(name="X-API-KEY", auto_error=False)

async def validate_api_key(request:Request,api_key: str = Depends(api_key_header)) -> Dict[str,str]:
    print(f'api_key {api_key}')
    r = get_redis_client()
    tenant = r.hgetall(api_key)
    if not tenant:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key",
        )
    tenant = {k.decode(): v.decode() for k, v in tenant.items()}
    request.state.tenant = tenant
    return tenant
