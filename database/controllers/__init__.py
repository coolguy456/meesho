import os
import redis
from database import *

redisHost = os.getenv("redisURL")
conn = redis.StrictRedis(host=redisHost)
