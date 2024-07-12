from models.request import Request
from services.crud.user_service import UserService
from services.crud.balance_service import BalanceService
import joblib
from database.database import SessionLocal

if __name__ == '__main__':
    with SessionLocal() as session:
        user_service = UserService(session)
        balance_service = BalanceService(session)

        # Create admin user
        admin = user_service.create_user('admin', '0880', 'Admin', 'User', 'example@gmail.com', 100000000)
        # Create demo user
        demo_user = user_service.create_user('demo', '0880', 'Demo', 'User', 'example@gmail.com', 20)

        # No need to add users to session and commit here, if create_user handles it internally
        # session.add(admin)
        # session.add(demo_user)
        # session.commit()

        # Login as admin
        user_service.login('admin', '0880')
        if user_service.current_user:
            print("Logged in as:", user_service.current_user)

            # Add balance to admin
            balance_service.add_balance(user_service.current_user.id, 20)
            print("Balance:", balance_service.get_balance(user_service.current_user.id))

            # Load machine learning model
            model = joblib.load('prophet_model.pkl')
            request_data = '2024-07-10'
            request = Request(data=request_data, model=model)

            # Handle request
            transaction = user_service.handle_request(request)
            if transaction:
                print("Transaction:", transaction)
            else:
                print("Transaction failed.")

            # Print transaction history
            transaction_history = user_service.transaction_history()
            if transaction_history:
                print("Transaction History:", transaction_history)
            else:
                print("No transaction history available.")
        else:
            print("Login failed.")

    # session.close() is handled automatically by using the `with` statement

