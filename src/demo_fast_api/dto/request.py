from pydantic import BaseModel, Field, EmailStr

class EquationRequest(BaseModel):
    a: float = Field(lt=1000)
    b: float = Field()
    c: float = Field()

class ContactRequest(BaseModel):
    name: str = Field(max_length=50, default="Ramox")
    email: EmailStr = Field(default="pochetraphael@gmail.com")
    content: str = Field(default="Coucou")