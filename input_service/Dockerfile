FROM python:3-slim
ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt
ENV FLASK_APP input_service
ENV FLASK_ENV development
ADD inputservice/inputservice inputservice
WORKDIR input_service
ENTRYPOINT ["flask","run"]