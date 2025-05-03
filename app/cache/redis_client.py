from dotenv import load_dotenv
import redis
import os
import json
import logging

load_dotenv()
logger = logging.getLogger(__name__)

EXPIRE_TIME=int(os.getenv('EXPIRE_TIME'))

r = redis.Redis(host=os.getenv('REDIS_HOST'), port=os.getenv('REDIS_PORT'), db=0, decode_responses=True)


def get_data_from_redis(key: str):
    data = r.get(key)
    if data:
        try:
            return json.loads(data)  
        except json.JSONDecodeError:
            logger.error(f"Erro ao decodificar JSON para a chave {key}")
            return None
    return None

def save_data_on_redis(data: dict, key: str) -> bool:
    try:
        return r.set(key, json.dumps(data, ensure_ascii=False, indent=4), ex=EXPIRE_TIME)
    except ConnectionError as e:
        print(f'Error trying to connect with Redis: {e}')
        return False
    except Exception as e:
        print(f'An error occurred trying to save on Redis: ({key}: {e})')
        return False