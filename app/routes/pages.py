from fastapi.responses import HTMLResponse
from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def home():
    with open("static/index.html") as f:
        return HTMLResponse(content=f.read(), status_code=200)
@router.get("/strength-training")
async def strength_training():
    with open("static/strength-training.html") as f:
        return HTMLResponse(content=f.read(), status_code=200)
@router.get("/cardio")
async def cardio():
    with open("static/cardio-training.html") as f:
        return HTMLResponse(content=f.read(), status_code=200)

@router.get("/aquatics")
async def aquatics():
    with open("static/aquatic-exercises.html") as f:
        return HTMLResponse(content=f.read(), status_code=200)
@router.get("/yoga")
async def yoga():
    with open("static/yoga-and-meditation.html") as f:
        return HTMLResponse(content=f.read(), status_code=200)

@router.get("/signup")
async def signup():
    with open("static/signup.html") as f:
        return HTMLResponse(content=f.read(), status_code=200)

@router.get('/dashboard')
async def dashboard():
    with open("static/user-dashboard.html") as f:
        return HTMLResponse(content=f.read(), status_code=200)

@router.get('/admin')
async def admin():
    with open("static/admin-dash-deep.html") as f:
        return HTMLResponse(content=f.read(), status_code=200)