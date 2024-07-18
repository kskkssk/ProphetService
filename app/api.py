from fastapi import FastAPI
from mlservice.routes.home import home_route
from mlservice.routes.user import user_route
from mlservice.routes.balance import balance_route

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
