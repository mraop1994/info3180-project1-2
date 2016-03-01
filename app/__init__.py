import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost/project1_2'
# app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://yzicurmnvkqqhp:Kpl-6hLvDaRcPCelsrxdmydSgi@ec2-23-21-219-209.compute-1.amazonaws.com:5432/de7vj5i2j9deb1"
db = SQLAlchemy(app)
db.create_all()

from app import views, models