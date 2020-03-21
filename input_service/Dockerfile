FROM python:3-slim
ENV FLASK_APP input_service
ENV FLASK_ENV development
COPY ./requirements.txt /input_service/requirements.txt
WORKDIR input_service
RUN pip install -r requirements.txt
ENTRYPOINT ["flask","run","--host=0.0.0.0"]