from fastapi import FastAPI
from .scrapping import run_scrapers 
from .slm_client import generate_answer
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

@app.get('/update_data')
def home():
    return run_scrapers()


