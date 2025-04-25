from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from dotenv import load_dotenv
import requests
import json
import os

load_dotenv()

url = os.getenv('URL')

def fetch_page(url: str) -> str:
    response = requests.get(url)
    return response.text


def fetch_page_js(url: str) -> str:
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)

    match_results = []

    try:
        driver.get(url)

        dates = driver.find_elements(By.CLASS_NAME, "MatchList__MatchListDate-sc-1pio0qc-0")

        for date in dates:
            match_date = date.text.strip()
            
            next_element = date.find_element(By.XPATH, 'following-sibling::a')

            if next_element:
                match_result = next_element.text.strip()

                match_results.append({
                    'date': match_date,
                    'result': match_result
                })

    
    
    finally:
        driver.quit()

    return json.dumps(match_results, ensure_ascii=False, indent=4)


def extract_nicknames(container, class_prefix) -> list:
    if not container:
        return []
    
    return [
        div.get_text(strip=True)
        for div in container.find_all('div', class_=lambda c: c and c.startswith(class_prefix))
    ]


def get_lineup_info(content: str) -> dict:

    soup = BeautifulSoup(content, 'html.parser')
    
    players_container = soup.select_one('#AppContainer > div > div > div > div.sc-dkPtRN.id__BaseCol-sc-1x9brse-0.TYdVh.edCxBh > div.id__ContentContainer-sc-1x9brse-2.hlMjcl > div:nth-child(2)')
    benched_players_container = soup.select_one('#AppContainer > div > div > div > div.sc-dkPtRN.id__BaseCol-sc-1x9brse-0.TYdVh.edCxBh > div.id__ContentContainer-sc-1x9brse-2.hlMjcl > div:nth-child(4)')
    coach_container = soup.select_one('#AppContainer > div > div > div > div.sc-dkPtRN.id__MenuCol-sc-1x9brse-1.UsnfG.elezoS > div.PlayerCardList__PlayerCardListContainer-sc-cuylet-0.kuAkeK')

    return {
        "players": extract_nicknames(players_container, 'PlayerCard__PlayerNickName-sc-1u0zx4y'),
        "benched": extract_nicknames(benched_players_container, 'PlayerCard__PlayerNickName-sc-1u0zx4y'),
        "coach": extract_nicknames(coach_container, 'PlayerCard__PlayerInfo-sc-1u0zx4y')
    }


def get_latest_news(content: str) -> dict:
    
    soup = BeautifulSoup(content, 'html.parser')
    news_containers = soup.find_all('a', class_=lambda c: c and c.startswith('NewsCardSmall__NewsCardSmallContainer-sc-1q3y6t7'))

    if not news_containers:
        return {'error': 'Latest news not found'}

    news_list = [news.get_text(strip=True) for news in news_containers]
    
    return {'Latest news': news_list}