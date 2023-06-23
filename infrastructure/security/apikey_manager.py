from infrastructure.redis.redis_support import get_redis_client

rate_limit_key = 'rate_limit'

def create_customer_credentials(tenant:str,apikey:str,client_secret:str,rate_limit:str='10/minute'):
    r = get_redis_client()
    r.hmset(apikey, {'name': tenant, 
                     'client_secret':client_secret,
                     rate_limit_key: rate_limit}) 