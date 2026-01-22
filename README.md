Сервис, предсказывающий временные ряды на следующие 5 дней. Собран в докер-образ, для него написан телеграм бот и фронт на streamlit. Есть функционал регистрации и авторизации пользователя, функционал проверки, пополнения баланса, а также списания со счета денежных средств при выполнении запроса модели. Для предсказаания временных рядов использована модель Prophet: https://facebook.github.io/prophet/

Сервис написан на FastAPI, в докер образе собран Nginx, RabbitMQ для реализации многопоточности, написаны unit тесты

**EN:**
A service for forecasting time series for the next 5 days. The system is containerized using Docker and includes a Telegram bot and a Streamlit-based web interface. User registration and authentication are implemented, along with balance management features such as balance checks, top-ups, and automated billing per model request.

Time series forecasting is performed using the Prophet model.

The backend is implemented with FastAPI. The Dockerized setup includes Nginx and RabbitMQ for asynchronous task processing and concurrency. Unit tests are implemented to ensure system reliability.
