from fastapi import FastAPI, HTTPException, Depends, Request
from .chatbot.scrapping import run_scrapers 
from .chatbot.chatbot import find_similar_question, UserMessage
from .schemas.partner_dto import PartnerCreate
from .services.partner_service import create_partner, delete_partner
from sqlalchemy.orm import Session
from .database.db import get_db
from .database.init_db import init_db
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
import logging
import os

load_dotenv()
logger = logging.getLogger(__name__)


LINEUP_KEY=os.getenv('LINEUP_KEY')
NEWS_KEY=os.getenv('NEWS_KEY')
RESULTS_KEY=os.getenv('RESULTS_KEY')

app = FastAPI()

init_db()

templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get('/update_data')
async def update_data():
    """Endpoint to update redis data"""
    update_data = run_scrapers()
    
    if not update_data:
        raise HTTPException(status_code=500, detail='Database update has been failed')
    
    return {'message': 'Database has been updated successfully.'}


@app.post('/chat')
async def ask_furia(question: UserMessage):
    try:
        user_question = question.message.strip()

        if not user_question:
            raise HTTPException(status_code=400, detail="The question can't be empty.")
        
        return {"success": True if find_similar_question(user_question) else False,
                "data" : find_similar_question(user_question)
        }
    
    except Exception as e:
        logger.error(f'Error at /chat: {e}')
        raise HTTPException(status_code=500, detail="Internal error trying to process the question")

@app.post('/register', response_model=dict)  
async def register_partner(partner: PartnerCreate, db: Session = Depends(get_db)):
    try:
        new_partner = create_partner(partner, db)
        return {
            'success': True,
            'message': 'Partner registered successfully.',
            'data': {
                'id': new_partner.id,
                'name': new_partner.name
            }
        }
    except ValueError as e:
        logger.error(f'Error at /register: {e}')
        raise HTTPException(status_code=400, detail=str(e))
    

@app.delete('/delete/{partner_id}', response_model=dict)
async def delete_partner_by_id(partner_id: int, db: Session = Depends(get_db)):
    try:
        deleted_partner = delete_partner(partner_id, db)
        return {
            'success': True,
            'message': deleted_partner['message']
        }
    except ValueError as e:
        logger.error(f'Error at /delete/{partner_id}: {e}')
        raise HTTPException(status_code=400, detail=str(e))
    

@app.get("/test")
async def get_home(request: Request):
    return templates.TemplateResponse("admin.html", {"request": request})
