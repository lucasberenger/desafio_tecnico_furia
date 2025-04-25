from dotenv import load_dotenv
import requests
import json
import os

load_dotenv()

def generate_answer(data: list) -> str:
    prompt = f""" 
A seguir estão alguns dados do time de Counter Strike da Furia.

{json.dumps(data, indent=2)}

Sua missão:

- Use essas informações para responder perguntas sobre a FURIA.
- Se a pergunta for sobre os últimos jogos, liste cada um com data, hora, adversário e campeonato de forma clara.
- Ao final, se fizer sentido, adicione uma análise da performance recente — como um comentarista esportivo falando com um fã (um verdadeiro FURIOSO).
- Se a pergunta não puder ser respondida com base nesses dados, diga de forma simples e honesta que a informação não está disponível.

Seja natural, direto e envolvente. Fale como quem vive o eSports.

"""
    
    mistral_response = requests.post(
        os.getenv('SLM_ENDPOINT'),
        json={
            "model": "mistral",
            "prompt": prompt,
            "stream": False
        }
    )

    print(mistral_response.json()['response'])