FROM python:3-slim
ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt
ENV FLASK_APP input_service
ENV FLASK_ENV development
ENTRYPOINT ["flask","run","--host=0.0.0.0"]
