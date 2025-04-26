import redis
import os
import json
from dotenv import load_dotenv

load_dotenv()

r = redis.Redis(host=os.getenv('REDIS_HOST'), port=os.getenv('REDIS_PORT'), decode_responses=True)


def get_data_from_redis(key: str) -> dict:
    data = r.get(key)

    if data:
        return json.loads(data)
    
    return None

def save_data_on_redis(data: dict, key: str) -> bool:
    try:
        return r.set(key, json.dumps(data, ensure_ascii=False, indent=4), ex=60)
    except ConnectionError as e:
        print(f'Error trying to connect with Redis: {e}')
        return False
    except Exception as e:
        print(f'An error occured trying to save on Redis: ({key}: {e})')
        return False