from fastapi import FastAPI, HTTPException, Depends, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from .chatbot.scrapping import run_scrapers 
from .chatbot.chatbot import find_similar_question, UserMessage
from .schemas.partner_dto import PartnerCreate
from .services.partner_service import create_partner, delete_partner
from .services import chart_service
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


@app.post('/update_data')
async def update_data():
    """Endpoint to update redis data"""
    update_data = run_scrapers()

    if not update_data:
        raise HTTPException(status_code=500, detail='Database update has been failed')

    return RedirectResponse(url="/admin", status_code=303)


@app.get('/chat')
async def chatbot_page(request: Request, user_message: str = None):
    answer = None
    if user_message:
        answer = find_similar_question(user_message)
    return templates.TemplateResponse("chat.html", {
        "request": request,
        "user_message": user_message,
        "answer": answer
    }
    )

@app.post('/chat')
async def ask_furia(question: UserMessage):
    try:
        user_question = question.message.strip()

        if not user_question:
            raise HTTPException(status_code=400, detail="The question can't be empty.")
        
        answer = find_similar_question(user_question)

        if isinstance(answer, dict):
            return {"success": True, "response": answer}
        else:
            return {"success": False, "response": "Sorry, I don't have an answer for that."}
    
    except Exception as e:
        logger.error(f'Error at /chat: {e}')
        raise HTTPException(status_code=500, detail="Internal error trying to process the question")
    

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


@app.get("/admin/dashboard")
async def admin_dashboard(request: Request, db: Session = Depends(get_db)):
    graphic = chart_service.generate_chart(db)
    return templates.TemplateResponse("admin_dashboard.html", {"request": request, "graphic": graphic})


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """
    Custom exception handler for HTTP exceptions.
    """
    if exc.status_code == 404:
        return templates.TemplateResponse("error.html", {"request": request}, status_code=404)

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    """
    Generic exception handler for all unhandled exceptions.
    """
    return templates.TemplateResponse("error.html", {"request": request}, status_code=500)
