from ..models.partner import Partner
from sqlalchemy.orm import Session
from collections import Counter
from urllib import parse
import matplotlib.pyplot as plt
import io
import base64


def get_social_media(url: str) -> str:
    if not url:
        return 'Outro'

    try:
        if not url.startswith(('http://', 'https://')):
            url = 'http://' + url

        parsed_url = parse.urlparse(url)
        domain = parsed_url.netloc.lower().replace('www.', '')

        if 'facebook' in domain:
            return 'Facebook'
        elif 'twitter' in domain or 'x.com' in domain:
            return 'X'
        elif 'instagram' in domain:
            return 'Instagram'
        elif 'linkedin' in domain:
            return 'LinkedIn'
        else:
            return 'Outro'
    except Exception as e:
        print(f"Error while processing URL: {url} → {e}")
        return 'Outro'




def get_social_media_count(db: Session):
    partners = db.query(Partner).all()

    social_media_urls = [partner.social_media for partner in partners if partner.social_media]
    social_media_platforms = [get_social_media(url) for url in social_media_urls]
    return Counter(social_media_platforms)


def generate_chart(db: Session):
    social_media_counts = get_social_media_count(db)

    labels = list(social_media_counts.keys())
    values = list(social_media_counts.values())

    if not labels:
        print("No data available.")
        return ""  

    try:

        plt.figure(figsize=(10, 6))
        plt.bar(labels, values, color='lightcoral')
        plt.xlabel("Plataforma de Rede Social")
        plt.ylabel("Número de Cadastros")
        plt.title("Plataformas de Redes Sociais Mais Cadastradas")
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()

        buffer = io.BytesIO()
        plt.savefig(buffer, format="png")
        buffer.seek(0)
        image_png = buffer.getvalue()
        graphic = base64.b64encode(image_png).decode("utf-8")
        plt.close()
        return graphic
    except Exception as e:
        print(f"Error while trying to generate chart: {e}")
        return ""

