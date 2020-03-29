import databases
import sqlalchemy
from pydantic import BaseModel
from datetime import datetime
import os
SQLALCHEMY_DATABASE_URI=os.environ.get("CONNECTION_STRING","sqlite:///test.db")
"""
Die Models entsprechend der API Beschreibung mit einer One-to-One Relation
"""

database = databases.Database(SQLALCHEMY_DATABASE_URI)

metadata = sqlalchemy.MetaData()
#sqlalchemy.relationship('UserData', uselist=False, backref='market'),
sql_stammdaten = sqlalchemy.Table(
    "Stammdaten",
    metadata,
    sqlalchemy.Column('MarketID',sqlalchemy.BIGINT,  primary_key=True),
    sqlalchemy.Column( 'Name',sqlalchemy.String(100), unique=False, nullable=False),
    sqlalchemy.Column( 'Firma',sqlalchemy.String(100), unique=False, nullable=False),
    sqlalchemy.Column( 'lat',sqlalchemy.Float, unique=False, nullable=False),
    sqlalchemy.Column( 'long',sqlalchemy.Float, unique=False, nullable=False),
    sqlalchemy.Column( 'Adresse',sqlalchemy.String(50), unique=False, nullable=False),
    sqlalchemy.Column( 'Enabled',sqlalchemy.Boolean),
    sqlalchemy.Column('Status', sqlalchemy.Integer),
    sqlalchemy.Column(
        'TimeStamp',
        sqlalchemy.DateTime,
        server_default=sqlalchemy.func.current_timestamp(),
        server_onupdate=sqlalchemy.func.current_timestamp()
        )
 )


class Stammdaten(BaseModel):
    MarketID: int
    Name: str
    Firma: str
    lat: float
    long: float
    Adresse: str
    Enabled: bool = False
    Status: int = None
    TimeStamp: datetime = None

class Market_status(BaseModel):
    MarketID: int
    Status: int

#sqlalchemy.Column('MarketID', sqlalchemy.Integer,sqlalchemy.ForeignKey('stammdaten.MarketID')),
sql_userdata = sqlalchemy.Table(
    "UserData",
    metadata,
    sqlalchemy.Column( 'UserID',sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column( 'UserName',sqlalchemy.String(20), unique=False, nullable=False),
    sqlalchemy.Column( "password",sqlalchemy.String(94), nullable=False),
    sqlalchemy.Column( 'Rolle',sqlalchemy.Integer),
    sqlalchemy.Column( 'Email',sqlalchemy.String(50)),
    sqlalchemy.Column( 'Telefon',sqlalchemy.String(20)),
    sqlalchemy.Column( 'BearerToken',sqlalchemy.String(43), unique=True),
    sqlalchemy.Column( 'Enabled',sqlalchemy.Boolean,default=False,nullable=False)
  )

class UserData(BaseModel):
    UserID: int
    UserName: str
    Rolle: int
    Email: str
    Telefon: str
    BearerToken: str
    Enabled: bool=False

class RegisterUser(BaseModel):
    UserName: str
    password: str
    Email: str
    Telefon: str

class UserInDB(UserData):
    hashed_password: str

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str = None





engine = sqlalchemy.create_engine(
    SQLALCHEMY_DATABASE_URI, connect_args={"check_same_thread": False}
)
metadata.create_all(engine)
