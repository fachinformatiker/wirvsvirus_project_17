FROM python:3-slim
ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt
ENV FLASK_APP control_service
ENV FLASK_ENV development
ADD control_service control_service
WORKDIR control_service
ENTRYPOINT ["flask","run","--host 0.0.0.0"]