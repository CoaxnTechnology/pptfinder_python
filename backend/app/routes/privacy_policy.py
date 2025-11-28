from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="app/templates")

router = APIRouter(
    prefix="",
    tags=["Privacy Policy"]
)

@router.get("/privacy-policy", response_class=HTMLResponse)
def privacy_policy(request: Request):
    return templates.TemplateResponse("privacy_policy.html", {"request": request})
