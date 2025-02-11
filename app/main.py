from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from database.database import create_database, get_db
from database.models import populate_sample_data
from routes import auth, pages, admin, users, trainers, dashboard

app = FastAPI()
create_database()

# Serve static files (HTML/CSS/JS)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Include routes
app.include_router(pages.router)
app.include_router(auth.router, prefix="/api")
app.include_router(users.router, prefix="/api/admin")
app.include_router(trainers.router, prefix="/api/admin")
# app.include_router(programs.router, prefix="/api/admin")
app.include_router(dashboard.router, prefix="/api")
app.include_router(admin.router, prefix="/api/admin")
# app.include_router(chatbot.router, prefix="/api/chatbot")
# app.include_router(workout.router, prefix="/api/workouts")
# app.include_router(nutrition.router, prefix="/api/nutrition")