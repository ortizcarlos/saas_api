from redis import Redis, ConnectionPool
from typing import Dict

# Initialize Redis connection pool
pool = ConnectionPool(host='localhost', port=6379, db=0)  # Use your Redis server details

def get_redis_client():
    return Redis(connection_pool=pool)