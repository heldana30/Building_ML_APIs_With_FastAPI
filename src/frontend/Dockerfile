FROM python:3.10.9

COPY requirements.txt /temp/requirements.txt

RUN python -m pip install --timeout 300000 -r /temp/requirements.txt

COPY . /app

WORKDIR /app

EXPOSE 3000

CMD [ "streamlit", "run",  "predict.py", "--server.port=8501"]