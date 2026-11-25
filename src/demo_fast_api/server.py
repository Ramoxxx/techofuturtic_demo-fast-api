from typing import Annotated
from fastapi import FastAPI, Query
import uvicorn


app = FastAPI()

@app.get('/api/hello')
def say_hello(name: Annotated[str, Query()] = 'World'):
    return f"hello {name} !!"

@app.get('/api/fibo')
def fibo():
    return 'fibo'

def main():
    uvicorn.run('demo_fast_api.server:app', port=8080, reload=True)