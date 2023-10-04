from app import db
from datetime import datetime


class Owner(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(25))
    last_name = db.Column(db.String(25))
    phone_no = db.Column(db.Integer)
    email = db.Column(db.String(225))
    created_at = db.Column(db.DateTime, default=datetime.now())
    properties = db.relationship('Property', backref='owner', lazy=True)


class Property(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String, nullable=False)
    rooms = db.Column(db.String)
    owner_id = db.Column(db.Integer, db.ForeignKey('owner.id'), nullable=False)
    occupied = db.Column(db.String, nullable=False)
    houses = db.relationship('House', backref='property', lazy=True)


class Tenants(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    phone_no = db.Column(db.Integer)
    email = db.Column(db.String(225), nullable=False)
    due_date = db.Column(db.DateTime)
    payment = db.Column(db.Integer)
    property_id = db.Column(db.Integer, db.ForeignKey('property.id'))


class Issues(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    description = db.Column(db.String, nullable=False)


class HouseIssue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    house_id = db.Column(db.Integer, db.ForeignKey('house.id'), nullable=False)
    issues_id = db.Column(db.Integer, db.ForeignKey('issues.id'), nullable=False)
    complaint = db.Column(db.String(225))

# Define the House model with one-to-many relationship and many-to-many relationship


class House(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    unit_id = db.Column(db.Integer)
    rent = db.Column(db.Integer)
    rooms = db.Column(db.String)
    property_id = db.Column(db.Integer, db.ForeignKey('property.id'))

    # Define the one-to-many relationship with HouseIssue
    issues = db.relationship('HouseIssue', backref='house', lazy=True)

    # Define the many-to-many relationship with Issues through HouseIssue
    issues_many_to_many = db.relationship('Issues',secondary='house_issue', backref=db.backref('houses',lazy='dynamic'))

