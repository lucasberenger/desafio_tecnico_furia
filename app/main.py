from fastapi import FastAPI, HTTPException, Depends, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from .chatbot.scrapping import run_scrapers 
from .chatbot.chatbot import find_similar_question, UserMessage
from .schemas.partner_dto import PartnerCreate
from .services.partner_service import create_partner, delete_partner
from sqlalchemy.orm import Session
from .database.db import get_db
from .database.init_db import init_db
from typing import Annotated
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
        
        answer = find_similar_question(user_question)
        
        return {"response": answer or "Sorry, I don't have an answer for that."}
    
    except Exception as e:
        logger.error(f'Error at /chat: {e}')
        raise HTTPException(status_code=500, detail="Internal error trying to process the question")
    

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
    

@app.get("/register")
async def get_home(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.post('/register')
async def register(
    name: Annotated[str, Form()],
    age: Annotated[int, Form()],
    cpf: Annotated[str, Form()],
    email: Annotated[str, Form()],
    phone: Annotated[str, Form()],
    social_media: Annotated[str, Form()],
    db: Session = Depends(get_db)
):
    try:
        data = PartnerCreate(
            name=name,
            age=age,
            cpf=cpf,
            email=email,
            phone=phone,
            social_media=social_media
    )
        new_partner = create_partner(data, db)

        return RedirectResponse(url='/admin', status_code=303)
    
    except ValueError as e:
        logger.error(f'Error at /test: {e}')
        raise HTTPException(status_code=400, detail=str(e))
    
@app.get('/admin')
async def admin_page(request: Request):
    return templates.TemplateResponse("admin.html", {"request": request})

@app.get('/chat')
async def chatbot_page(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})
