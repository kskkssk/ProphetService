from models.request import Request
from models.user_service import UserService
import joblib


if __name__ == '__main__':
    model = joblib.load('prophet_model.pkl')
    # Пример
    service = UserService()
    service.sign_up('kskkssk', '0880', 'Aleks', 'Kud', 20, 'example@gmail.com')
    service.sign_in('kskkssk', '0880')
    request = Request('2024-02-27', model)
    transaction = service.handle_request(request)
    if transaction:
        print(transaction)
    else:
        print("Ошибка")

    print('История транзакций', service.transaction_history())