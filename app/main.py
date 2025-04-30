from fastapi import FastAPI, HTTPException
from .scrapping import run_scrapers 
from .chatbot import find_similar_question, UserMessage
from .redis_client import save_data_on_redis, get_data_from_redis
from dotenv import load_dotenv
import logging
import os

load_dotenv()
logger = logging.getLogger(__name__)


LINEUP_KEY=os.getenv('LINEUP_KEY')
NEWS_KEY=os.getenv('NEWS_KEY')
RESULTS_KEY=os.getenv('RESULTS_KEY')

app = FastAPI()

@app.get('/update_data')
async def update_data():
    """Endpoint to update redis data"""
    update_data = run_scrapers()
    
    if not update_data:
        raise HTTPException(status_code=500, detail='Database update has been failed')
    
    return {'message': 'Database has been updated successfully.'}
        


@app.get('/test')
def test():
    """ Endpoint to test Redis """

    test_data = {'message': 'test data'}
    save_data_on_redis(test_data, 'test_key')

    retrieved_data = get_data_from_redis('test_key')

    if retrieved_data:
        return {'status': 'success', 'key': 'test_key', 'data': retrieved_data}
    
    else:
        return {'status': 'error', 'key': 'test_key', 'message': False}


@app.post('/chat')
async def ask_furia(question: UserMessage):
    try:
        user_question = question.message.strip()

        if not user_question:
            raise HTTPException(status_code=400, detail="The question can't be empty.")
        
        return {"success": True,
                "data" : find_similar_question(user_question)
        }
    
    except Exception as e:
        logger.error(f'Error at /chat: {e}')
        raise HTTPException(status_code=500, detail="Internal error trying to process the question")

        