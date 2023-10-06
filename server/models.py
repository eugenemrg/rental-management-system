from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class Owner(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    properties = db.relationship('Property', backref='owner', lazy=True)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

class Property(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(200), nullable=False)
    owner_name = db.Column(db.String(200), nullable=True)  
    property_name = db.Column(db.String(200), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('owner.id'), nullable=False)
    houses = db.relationship('House', backref='property', lazy=True)
    

class House(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=False)
    rent = db.Column(db.Float, nullable=False)
    balance = db.Column(db.Float, default=0.0) 
    tenant_name = db.Column(db.String(200), nullable=True)  
    property_id = db.Column(db.Integer, db.ForeignKey('property.id'), nullable=False)
    property_name = db.Column(db.String(200), nullable=True)  
    tenant_id = db.Column(db.Integer, db.ForeignKey('tenant.id'), nullable=True)
    issues = db.relationship('HouseIssue', backref='house', lazy=True)

class Tenant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    houses = db.relationship('House', backref='tenant', lazy=True)

class Issue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(500), nullable=False)
    house_issues = db.relationship('HouseIssue', backref='issue', lazy=True)

class HouseIssue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    house_id = db.Column(db.Integer, db.ForeignKey('house.id'), nullable=False)
    house_name = db.Column(db.String(200), nullable=True)
    issue_id = db.Column(db.Integer, db.ForeignKey('issue.id'), nullable=False)
    issue_name = db.Column(db.String(200), nullable=True)
    status = db.Column(db.String(50), nullable=False) 
