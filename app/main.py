from models.request import Request
from services.crud.user_service import UserService
from services.crud.balance_service import BalanceService
import joblib
from database.database import SessionLocal, engine

if __name__ == '__main__':
    with SessionLocal(engine) as session:
        user_service = UserService(session)
        balance_service = BalanceService(session)

        admin = user_service.create_user('admin', '0880', 'Admin', 'User', 'example@gmail.com', 100000000)
        session.add(admin)
        demo_user = user_service.create_user('demo', '0880', 'Demo', 'User', 'example@gmail.com', 20)
        session.add(demo_user)
        session.commit()
        print("создали пользователя!")
        user_service.login('admin', '0880')
        print("залогинились!")
        print(user_service.current_user)

        balance_service.add_balance(user_service.current_user.id, 20)
        print("Баланс", balance_service.get_balance(user_service.current_user.id))
        print(user_service.get_all_users())
        model = joblib.load('prophet_model.pkl')
        request_data = '2024-07-10'
        request = Request(data=request_data, model=model)
        transaction = user_service.handle_request(request)
        if transaction:
            print(transaction)
        else:
            print("Ошибка")

        session.close()

    print('История транзакций', user_service.transaction_history())
