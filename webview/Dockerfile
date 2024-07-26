FROM python:3.11-slim

WORKDIR /app

COPY ./app/requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY app /app
COPY webview /app/webview
COPY worker /app/worker

EXPOSE 8501

ENV PYTHONPATH="${PYTHONPATH}:/app"

CMD ["streamlit", "run", "webview/webui.py", "--server.port", "8501", "--server.address", "0.0.0.0"]

