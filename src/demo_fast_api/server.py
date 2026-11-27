from fastapi import FastAPI
import uvicorn


from demo_fast_api.routers import default_routes, math_routes, pokemon_routes, type_routes

app = FastAPI()
# app = FastAPI(root_path="/api")

app.include_router(default_routes.router)
app.include_router(math_routes.router)
app.include_router(pokemon_routes.router)
app.include_router(type_routes.router)

def main():
    uvicorn.run(
        'demo_fast_api.server:app',
        port=8080,
        reload=True
    )