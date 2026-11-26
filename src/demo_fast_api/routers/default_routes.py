from typing import Annotated

from fastapi import APIRouter, Body, Depends, Query

from demo_fast_api.dto.request import ContactRequest
from demo_fast_api.infrastructure.mailer import Mailer


router = APIRouter(tags=['Default'])

@router.get('/hello', response_model=str)
def say_hello(name: Annotated[str, Query()] = 'World'):
    return f"hello {name} !!"

@router.post("/contact", response_model=str)
async def contact(dto: Annotated[ContactRequest, Body()], mailer: Annotated[Mailer, Depends(Mailer)]):
    name = dto.name
    email = dto.email
    content = dto.content
    return "mail sending disabled"
    # try:
    #     await mailer.send_email([email], f"{name} sent a message from fast api.", content)
    #     return f"Mail sent to {email}"
    # except Exception as error:
    #     return str(error)