FROM python:3-slim
ENV FLASK_APP input_service
ENV FLASK_ENV development
ADD input_service input_service
WORKDIR input_service
RUN pip install -r requirements.txt
ENTRYPOINT ["flask","run","--host=0.0.0.0"]