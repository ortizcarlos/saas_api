import logging

from fastapi import APIRouter, Request, Form
from typing import Optional

from infrastructure.quota.rate_limiter import limiter

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/v1/search",
    tags=["resume"],
    responses={404: {"description": "Resume Not found"}}
)



@router.post("/nlp")
@limiter.limit('')
async def sem_search(request:Request, 
                     query: str = Form(), 
                     top_k: Optional[int] = Form(5)):

  tenant = request.state.tenant
  print(f"search request from tenant {tenant} , query {query}")
  return "ok"
