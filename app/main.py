from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates("app/templates/")

def get_db():
    pass

@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse(name="index.html", request=request)

# Only for admins
@app.get("/admin")
async def admin_page(request: Request):
    return templates.TemplateResponse(name="admin_dashboard.html", request=request)

@app.post("/postdata")
async def postdata(name=Form()):
    pass