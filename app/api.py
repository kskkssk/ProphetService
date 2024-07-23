from fastapi import FastAPI
from routes.home import home_route
from routes.user import user_route
from routes.balance import balance_route
import json
import pika
from database.database import init_db
import uvicorn

app = FastAPI()

app.include_router(home_route)
app.include_router(user_route, prefix='/users') #префикс чтобы не было коллизий
app.include_router(balance_route, prefix='/balances')
app.on_event('startup')


def startup():
    init_db()


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8083)
