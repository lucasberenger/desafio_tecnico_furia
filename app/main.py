from fastapi import FastAPI, HTTPException
from .scrapping import run_scrapers 
from .slm_client import UserMessage, generate_answer
from .redis_client import save_data_on_redis, get_data_from_redis
from dotenv import load_dotenv
import os

load_dotenv()

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
async def chat(user_message: UserMessage):
    """Endpoint to chat with FURIA Chatbot"""

    message = user_message.message

    # Get data from database
    lineup = get_data_from_redis(LINEUP_KEY)
    last_results = get_data_from_redis(RESULTS_KEY)
    latest_news = get_data_from_redis(NEWS_KEY)

    data = {
        "lineup": lineup if lineup else {},
        "last_results": last_results if last_results else [],
        "latest_news": latest_news.get('Latest news') if latest_news else []
    }

    user_message = UserMessage(message=message)

    slm_response = generate_answer(data, user_message)

    if slm_response:
        return {'answer': slm_response}
    else:
        raise HTTPException(status_code=500, detail='Failed trying to get SLM response')
   