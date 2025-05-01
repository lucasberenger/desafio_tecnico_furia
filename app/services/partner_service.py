from ..models.partner import Partner
from ..schemas.partner_dto import PartnerCreate
from ..database.db import get_db
from sqlalchemy.orm import Session

def create_partner(partner_data: PartnerCreate, db: Session):
    """Create a new partner in the database."""

    db_partner = db.query(Partner).filter(Partner.cpf == partner_data.cpf).first()
    if db_partner:
        raise ValueError("Partner with this CPF already exists.")
    
    new_partner = Partner(
        name=partner_data.name,
        age=partner_data.age,
        cpf=partner_data.cpf,
        email=partner_data.email,
        phone=partner_data.phone,
        social_media=partner_data.social_media
    )

    db.add(new_partner)
    db.commit()
    db.refresh(new_partner)

    return new_partner    

def delete_partner(partner_id: int, db: Session):
    """Delete a partner from the database."""

    db_partner = db.query(Partner).filter(Partner.id == partner_id).first()
    if not db_partner:
        raise ValueError("Partner not found.")

    db.delete(db_partner)
    db.commit()

    return {"message": "Partner deleted successfully."}