from models.request import Request
from services.crud.user_service import UserService
from services.crud.balance_service import BalanceService
import joblib
from database.database import SessionLocal

if __name__ == '__main__':
    with SessionLocal() as session:
        user_service = UserService(session)
        balance_service = BalanceService(session)

        admin = user_service.create_user('admin', '0880', 'Admin', 'User', 'example@gmail.com', 100000000)
        demo_user = user_service.create_user('demo', '0880', 'Demo', 'User', 'example@gmail.com', 20)

        user_service.login('admin', '0880')
        if user_service.current_user:
            print("Logged in as:", user_service.current_user)

            balance_service.add_balance(user_service.current_user.id, 20)
            print("Balance:", balance_service.get_balance(user_service.current_user.id))

            model = joblib.load('prophet_model.pkl')
            request_data = '2024-10-10'
            request = Request(data=request_data, model=model)

            transaction = user_service.handle_request(request)
            if transaction:
                print("Transaction:", transaction)
            else:
                print("Transaction failed.")

            transaction_history = user_service.transaction_history()
            if transaction_history:
                print("Transaction History:", transaction_history)
            else:
                print("No transaction history available.")
        else:
            print("Login failed.")


