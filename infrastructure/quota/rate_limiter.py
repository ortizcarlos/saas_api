from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from fastapi import Depends,Request
from typing import Optional,Callable,Any


class DynamicLimiter(Limiter):
    def _check_request_limit(
        self,
        request: Request,
        endpoint_func: Optional[Callable[..., Any]],
        in_middleware: bool = True,
    ) -> None:
        
        tenant = request.state.tenant
        
        def get_rate_limit():
           return tenant["rate_limit"]
        
        @limiter.limit(get_rate_limit)
        def get_expression(request):
            return endpoint_func
 
        print(endpoint_func)
        return super()._check_request_limit(request,get_expression,in_middleware)
    
def get_user_id(request: Request = Depends(Request)):
    return request.state.tenant['name']
# default_limits=["1000 per day", "300 per hour", "5 per minute"]
limiter = DynamicLimiter(key_func=get_user_id, 
                         storage_uri="redis://localhost:6379",
                        )
