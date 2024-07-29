import os
import streamlit as st
from streamlit_cookies_manager import EncryptedCookieManager
from dotenv import load_dotenv
import requests
from celery.result import AsyncResult
from worker.tasks import handle_request as celery_handle_request
from worker.celery_config import app

load_dotenv()

api_base_url = os.getenv("API_BASE_URL")


cookie_manager = EncryptedCookieManager(
    prefix=os.getenv("COOKIE_MANAGER_PREFIX"),
    password=os.getenv("COOKIE_MANAGER_PASSWORD")
)


def authenticate(email, password):
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    data = {
        'grant_type': 'password',
        'username': email,
        'password': password,
    }
    response = requests.post(f'{api_base_url}/users/signin', headers=headers, data=data)
    if response.status_code == 200:
        return response.json().get("access_token")
    else:
        return None


def register_user(username, password, first_name, last_name, email):
    response = requests.post(f'{api_base_url}/users/signup',
                             json={"username": username,
                                   "password": password,
                                   "first_name": first_name,
                                   "last_name": last_name,
                                   "email": email})
    return response


def landing():
    st.header("AI Toolbox")
    st.sidebar.header("Navigation")
    mode = st.sidebar.selectbox("Выбрать страницу", ["Баланс", "Сделать предсказание"])

    if mode == "Баланс":
        show_balance()
    elif mode == "Сделать предсказание":
        make_prediction()


def show_balance():
    token = st.session_state.get("access_token")
    if token:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{api_base_url}/balances/balance", headers=headers)
        if response.status_code == 200:
            balance = response.json()
            st.success(f"Your balance is: {balance['amount']}")

            add_amount = st.number_input("Write amount to add", min_value=0.0, step=10.0, format="%.2f")
            if st.button("Add Balance"):
                response = requests.post(
                    f"{api_base_url}/balances/add_balance",
                    headers=headers,
                    data={"amount": float(add_amount)}
                )
            if response.status_code == 200:
                new_balance = response.json()
                st.success(f"New balance is: {new_balance['amount']}")
            else:
                st.error(f"Error: {response.text}")
        else:
            st.error("Unable to fetch balance. Please login again.")
    else:
        st.error("Please login first")


def format_prediction(predictions):
    formatted_output = ""
    for prediction in predictions['prediction']:
        date = prediction['ds']
        yhat = prediction['yhat']
        yhat_lower = prediction['yhat_lower']
        yhat_upper = prediction['yhat_upper']
        formatted_output += f"Дата: {date}\n"
        formatted_output += f"Прогноз: {yhat}\n"
        formatted_output += f"Диапазон: [{yhat_lower}, {yhat_upper}]\n\n"
    return formatted_output


def make_prediction():
    token = st.session_state.get("access_token")
    if token:
        headers = {"Authorization": f"Bearer {token}"}
        data = st.text_input("Write data for prediction in format YYYY-MM-DD")
        model = 'prophet_model'
        response = requests.get(f"{api_base_url}/users/current_user")
        if response.status_code == 200:
            user_data = response.json()
            current_user = user_data.get("username")
        else:
            st.error(f"Error: {response.text}")
        if st.button("Make Prediction"):
            try:
                task_id = celery_handle_request.apply_async(args=[data, model, current_user])
                result = AsyncResult(task_id, app=app)
                st.text(format_prediction(result.get()))
            except ValueError as e:
                st.error(f"Error: {str(e)}")
    else:
        st.error("Please login first")


def login_form():
    login_username = st.text_input("Email", key="login_username")
    login_password = st.text_input("Password", type="password", key="login_password")
    if st.button("Login"):
        st.session_state["login_attempted"] = True
        return authenticate(login_username, login_password)
    return None


def register_form():
    username = st.text_input("Username", key="register_username")
    password = st.text_input("Password", type="password", key="register_password")
    first_name = st.text_input("First Name", key="register_first_name")
    last_name = st.text_input("Last Name", key="register_last_name")
    email = st.text_input("Email", key="register_email")
    if st.button("Register"):
        st.session_state["register_attempted"] = True
        response = register_user(username, password, first_name, last_name, email)
        if response.status_code == 200:
            return authenticate(email, password)
        else:
            st.error(f"Error: {response.text}")
    return None


def main():
    if not cookie_manager.ready():
        st.stop()

    if "login_attempted" not in st.session_state:
        st.session_state["login_attempted"] = False
    if "register_attempted" not in st.session_state:
        st.session_state["register_attempted"] = False

    access_token = cookie_manager.get("access_token")

    st.header("ProfitProphet")

    if access_token:
        st.session_state["access_token"] = access_token
        landing()

        if st.button("Logout"):
            cookie_manager['access_token'] = ''
            st.success("Logged out successfully!")
            st.rerun()
    else:
        login_tab, register_tab = st.tabs(["Login", "Register"])

        with login_tab:
            access_token = login_form()

            if access_token:
                cookie_manager['access_token'] = access_token
                cookie_manager.save()
                st.experimental_rerun()
            elif st.session_state["login_attempted"]:
                st.warning("Invalid credentials. Please try again.")

        with register_tab:
            access_token = register_form()

            if access_token:
                cookie_manager['access_token'] = access_token
                cookie_manager.save()
                st.experimental_rerun()
            elif st.session_state["register_attempted"]:
                st.warning("Unable to authenticate. Please try again.")


if __name__ == "__main__":
    main()
