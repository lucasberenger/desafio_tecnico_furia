from dotenv import load_dotenv
from pydantic import BaseModel
import requests
import json
import os

load_dotenv()

SLM_ENDPOINT=os.getenv('SLM_ENDPOINT')
SLM_MODEL=os.getenv('SLM_MODEL')

class UserMessage(BaseModel):
    """Model to be used on user messages"""
    message: str

def generate_answer(data: list, message: UserMessage) -> str:
    prompt = f""" 
A seguir estão alguns dados do time de Counter-Strike da FURIA.

{json.dumps(data, indent=2)}

Sua missão:
- Use essas informações para responder a pergunta sobre a FURIA. Pergunta: {message.message}
- Se a pergunta for sobre os últimos jogos, liste cada um com data, hora, adversário e campeonato de forma clara.
- Ao final, se fizer sentido, adicione uma análise da performance recente — como um comentarista esportivo falando com um fã (um verdadeiro FURIOSO).
- Se a pergunta não puder ser respondida com base nesses dados, diga de forma simples e direta que a informação não está disponível.

Seja natural, direto e envolvente. Fale como quem vive o eSports.

"""
    try:
        mistral_response = requests.post(
            SLM_ENDPOINT,
            json={
                "model": SLM_MODEL,
                "prompt": prompt,
                "stream": False
            },
            # timeout=30
        )
        mistral_response.raise_for_status()
        response_data = mistral_response.json()

        if 'response' in response_data:
            return response_data['response']
        else:
            print(f'Error: SLM API response did not have the response field. Full response: {response_data}')
            return None
    except requests.exceptions.RequestException as e:
        print(f'An error ocurred while trying to connect with SLM API: {e}')
        return None
    except json.JSONDecodeError as e:
        print(f'An error ocurred while tryinh to decode JSON API response: {e}')
        return None
    except Exception as e:
        print(f'Unexpected error: {e}')
