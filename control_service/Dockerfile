FROM tiangolo/uvicorn-gunicorn:python3.7
ENV MODULE_NAME control_service.main
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY ./control_service /app/control_service
