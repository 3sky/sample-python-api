#!flask/bin/python
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app import db
from datetime import datetime


class AppStatus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    app_name = db.Column(db.String(50), unique=True, nullable=False)
    app_version = db.Column(db.String(50), unique=True, nullable=False)
    updated_date = db.Column(db.Integer, unique=True, nullable=False)
    updated_by = db.Column(db.String(10), unique=True, nullable=False)

    def __repr__(self):
        return '<ID: %d, app_name: %s, app_version: %s, updated_date: %s, updated_by: %s>' % (self.id, self.app_name, self.app_version, datetime.fromtimestamp(self.updated_date), self.updated_by)