from fastapi import FastAPI, Request
from .settings import templates
from .database import engine
from .models.products_model import *
from .routers import admin, user, cart

app = FastAPI()
app.include_router(admin.router)
app.include_router(user.router)
app.include_router(cart.router)
Base.metadata.create_all(bind=engine)

@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse(name="index.html", request=request)
