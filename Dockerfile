FROM python:3.10.10

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt --use-feature=fast-deps --no-warn-script-location

RUN pip install Werkzeug==2.3.0

COPY . .

CMD ["python3", "-m", "flask", "--app", "app.py", "run", "--host", "0.0.0.0"]
