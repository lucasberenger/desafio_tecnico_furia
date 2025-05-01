from pydantic import BaseModel, field_validator, EmailStr
from validate_docbr import CPF

cpf_validator = CPF()

class PartnerCreate(BaseModel):
    
    name: str
    age: int
    cpf: str
    email: EmailStr
    phone: str
    social_media: str

    field_validator('cpf')
    def validate_cpf(cls, cpf: str) -> str:
        """Validates the CPF format."""
        if not cpf_validator.validate(cpf):
            raise ValueError('Invalid CPF')
        
        return cpf

