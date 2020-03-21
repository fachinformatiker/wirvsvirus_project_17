FROM python:3-slim
ENV FLASK_APP control_service
ENV FLASK_ENV development
ADD control_service control_service
WORKDIR control_service
RUN pip install -r requirements.txt
ENTRYPOINT ["flask","run","--host=0.0.0.0"]