from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from config.settings import templates
from app.models import User
from tortoise.exceptions import IntegrityError
from passlib.hash import bcrypt

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("authentication/login.html", {"request": request, "error": None})

@router.post("/login")
async def login(request: Request, username: str = Form(...), password: str = Form(...)):
    user = await User.get_or_none(username=username)
    if not user or not bcrypt.verify(password, user.password_hash):
        return templates.TemplateResponse(
            "authentication/login.html",
            {"request": request, "error": "Login yoki parol xato!"},
        )
    if not user.is_admin:
        return templates.TemplateResponse(
            "authentication/login.html",
            {"request": request, "error": "Siz admin emassiz!"},
        )
    
    response = RedirectResponse("/auth/dashboard", status_code=303)
    response.set_cookie(key="admin_user", value=username, httponly=True)
    return response


@router.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse("authentication/register.html", {"request": request, "error": None})

@router.post("/register")
async def register(request: Request, username: str = Form(...), password: str = Form(...)):
    user = await User.create_user(username=username, password=password, is_admin=True)

    response = RedirectResponse("/auth/login", status_code=303)
    return response



@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    username = request.cookies.get("admin_user")
    if not username:
        return RedirectResponse("/auth/login", status_code=303)

    user = await User.get_or_none(username=username)
    if not user or not user.is_admin:
        return RedirectResponse("/auth/login", status_code=303)

    return templates.TemplateResponse(
        "base.html",
        {"request": request, "user": user},
    )

@router.get("/logout")
async def logout():
    response = RedirectResponse("/auth/login", status_code=303)
    response.delete_cookie("admin_user")
    return response
