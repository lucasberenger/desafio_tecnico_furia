from ..cache.redis_client import get_data_from_redis
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
        'Qual a lineup da FURIA?': ('lineup', get_data_from_redis(LINEUP_KEY)),
        'Quais as últimas notícias da FURIA?': ('news', get_data_from_redis(NEWS_KEY)),
        'Quais os últimos resultados dos jogos da FURIA?': ('results', get_data_from_redis(RESULTS_KEY))
    }

    questions = list(saved_questions.keys())
    best = process.extractOne(user_message, questions, scorer=fuzz.token_sort_ratio)

    if best:
        best_one, score, _ = best
        if score >= 50:
            type_, data = saved_questions.get(best_one)
            if type_ == 'lineup':
                return {
                    "players": data.get("players", []),
                    "benched": data.get("benched", []),
                    "coach": data.get("coach", [])
                }
            elif type_ == 'news':
                return {"news": data}
            elif type_ == 'results':
                return {"results": data}
    
    return 'Sorry, I did not understand.'

        