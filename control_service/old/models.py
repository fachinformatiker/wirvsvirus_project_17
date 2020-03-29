import databases
import sqlalchemy
from pydantic import BaseModel
from datetime import datetime
from control_service import SQLALCHEMY_DATABASE_URI, app

"""
Die Models entsprechend der API Beschreibung mit einer One-to-One Relation
"""

database = databases.Database(SQLALCHEMY_DATABASE_URI)

metadata = sqlalchemy.MetaData()

sql_stammdaten = sqlalchemy.Table(
    "Stammdaten",
    sqlalchemy.Column(sqlalchemy.Integer, name='MarketID', primary_key=True),
    sqlalchemy.Column(sqlalchemy.String(100), name='Name', unique=False, nullable=False),
    sqlalchemy.Column(sqlalchemy.String(100), name='Firma', unique=False, nullable=False),
    sqlalchemy.Column(sqlalchemy.Float, name='lat', unique=False, nullable=False),
    sqlalchemy.Column(sqlalchemy.Float, name='long', unique=False, nullable=False),
    sqlalchemy.Column(sqlalchemy.String(50), name='Adresse', unique=False, nullable=False),
    sqlalchemy.Column(sqlalchemy.Boolean, name='Enabled'),
    sqlalchemy.relationship('UserData', uselist=False, backref='market'),
    sqlalchemy.Column(sqlalchemy.Integer, name='Status'),
    sqlalchemy.Column(
        sqlalchemy.DateTime,
        name='TimeStamp',
        server_default=sqlalchemy.func.current_timestamp(),
        server_onupdate=sqlalchemy.func.current_timestamp())
 )


class Stammdaten(BaseModel):
    MarketID: int
    Name: str
    Firma: str
    lat: float
    long: float
    Adresse: str
    Enabled: bool
    Status: int
    TimeStamp: datetime


sql_userdata = sqlalchemy.Table(
    "UserData",
    sqlalchemy.Column(sqlalchemy.Integer, name='UserID', primary_key=True),
    sqlalchemy.Column(sqlalchemy.String(20), name='UserName', unique=False, nullable=False),
    sqlalchemy.Column(sqlalchemy.String(100), name="password", nullable=False),
    sqlalchemy.Column(sqlalchemy.Integer, name='Rolle'),
    sqlalchemy.Column(sqlalchemy.String(50), name='Email'),
    sqlalchemy.Column(sqlalchemy.String(20), name='Telefon'),
    sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('stammdaten.MarketID')),
    sqlalchemy.Column(sqlalchemy.String(43), name='BearerToken', unique=True)
  )

class UserData(BaseModel):
    UserID: int
    UserName: str
    Rolle: int
    Email: str
    Telefon: str
    BearerToken: str




engine = sqlalchemy.create_engine(
    SQLALCHEMY_DATABASE_URI, connect_args={"check_same_thread": False}
)
metadata.create_all(engine)

@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
