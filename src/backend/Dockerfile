FROM python:3.10.9

COPY requirements.txt /temp/requirements.txt

RUN python -m pip install --timeout 300000 -r /temp/requirements.txt

COPY . /

WORKDIR /src

EXPOSE 8080

CMD [ "uvicorn" , "api:app",  '--host', "0.0.0.0", "--port", "8000" ]