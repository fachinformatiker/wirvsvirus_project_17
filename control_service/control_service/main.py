from fastapi import FastAPI

#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app = FastAPI()

import control_service.models
import control_service.views
import control_service.viewsdynamic