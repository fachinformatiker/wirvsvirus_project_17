#import uvicorn
from fastapi import FastAPI
from .routers import items, users
from .models import database
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app = FastAPI()


app.include_router(users.router)
app.include_router(items.router)

@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
