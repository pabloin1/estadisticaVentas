import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'mysql+pymysql://admin:dine1234@database-2.cuef01lbhtnj.us-east-1.rds.amazonaws.com:3306/integrador')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
