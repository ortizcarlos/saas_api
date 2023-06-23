import asyncio
import logging
import uvicorn

from fastapi import Depends,HTTPException
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware import Middleware

from sentry_sdk import add_breadcrumb
from sentry_sdk import init as initialize_sentry, capture_exception
from sentry_sdk.integrations.logging import LoggingIntegration

from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from infrastructure.security.apikey_support import validate_api_key
from infrastructure.quota.rate_limiter import limiter

from interface.endpoints import search

middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
]

sentry_logging = LoggingIntegration(
    level=logging.INFO,        
    event_level=logging.ERROR  
)


initialize_sentry(
    dsn="your dsn",
    integrations=[sentry_logging]
)

logger = logging.getLogger(__name__)

app = FastAPI(middleware=middleware,
              dependencies = [Depends(validate_api_key)])

app.state.limiter = limiter

@app.middleware("http")
async def add_sentry_breadcrumbs(request: Request, call_next):
    # Add a breadcrumb for Sentry with the request details
    add_breadcrumb(
        category="request",
        data={
            "path": request.url.path,
            "method": request.method,
        },
    )
    # Continue processing the request
    return await call_next(request)

app.include_router(search.router)
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    # Capture the exception for Sentry
    capture_exception(exc)
    # Return the default FastAPI handler response
    return await request.app.default_exception_handler(request, exc)



# Run the FastAPI app
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)