from pydantic import BaseModel, Field, EmailStr, field_validator

class EquationRequest(BaseModel):
    a: float = Field(lt=1000)
    b: float = Field()
    c: float = Field()

class ContactRequest(BaseModel):
    name: str = Field(max_length=50, default="Ramox")
    email: EmailStr = Field(default="pochetraphael@gmail.com")
    content: str = Field(default="Coucou")

class TypeRequest(BaseModel):
    nom: str = Field(max_length=50)
    couleur_hex: str = Field(pattern=r'^[A-F0-9]{6}$')
    description: str = Field(max_len=1000)

    @field_validator('nom')
    @classmethod
    def format_nom(cls, value:str):
        return value.title()
