from .redis_client import get_data_from_redis
from dotenv import load_dotenv
from rapidfuzz import fuzz, process
from pydantic import BaseModel
import os


load_dotenv()

LINEUP_KEY=os.getenv('LINEUP_KEY')
NEWS_KEY=os.getenv('NEWS_KEY')
RESULTS_KEY=os.getenv('RESULTS_KEY')

class UserMessage(BaseModel):
    """Model to be used on user messages"""
    message: str


def find_similar_question(user_message: str):

    saved_questions = {
    'Qual a lineup da FURIA?': get_data_from_redis(LINEUP_KEY),
    'Quais as últimas notícias da FURIA?': get_data_from_redis(NEWS_KEY),
    'Quais os últimos resultados dos jogos da FURIA?': get_data_from_redis(RESULTS_KEY)
}

    questions = list(saved_questions.keys())
    best = process.extractOne(user_message, questions, scorer=fuzz.token_sort_ratio)

    if best:
        best_one, score, _ = best
        if score >= 50:
            return saved_questions.get(best_one)
    
    return 'Sorry, I did not understand.'
        