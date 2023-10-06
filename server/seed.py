from models import db, Owner, Property, House, Tenant, Issue, HouseIssue
from app import app
from faker import Faker
import random

fake = Faker()

# Number of fake entries
NUM_OWNERS = 30
NUM_PROPERTIES_PER_OWNER = 2
NUM_HOUSES_PER_PROPERTY = 5
NUM_TENANTS = 30
NUM_ISSUES = 10
NUM_HOUSE_ISSUES = 20

def seed_owners():
    for _ in range(NUM_OWNERS):
        owner = Owner(name=fake.name(), email=fake.email())
        owner.set_password(fake.password())
        db.session.add(owner)
    db.session.commit()

def seed_properties():
    owners = Owner.query.all()
    for owner in owners:
        for _ in range(random.randint(1, NUM_PROPERTIES_PER_OWNER)):
            prop = Property(
                location=fake.address(), 
                owner_id=owner.id, 
                property_name=fake.company(),  
                owner_name=owner.name  
            )
            db.session.add(prop)
    db.session.commit()

def seed_houses():
    properties = Property.query.all()
    for prop in properties:
        for _ in range(random.randint(1, NUM_HOUSES_PER_PROPERTY)):
            house = House(
                description=fake.sentence(), 
                rent=fake.random_int(500, 5000), 
                property_id=prop.id, 
                balance=random.uniform(0, 1000),  
                property_name=prop.property_name  
            )
            db.session.add(house)
    db.session.commit()


def seed_tenants():
    for _ in range(NUM_TENANTS):
        tenant = Tenant(name=fake.name(), email=fake.email())
        db.session.add(tenant)
    db.session.commit()

def seed_issues():
    for _ in range(NUM_ISSUES):
        issue = Issue(description=fake.sentence())
        db.session.add(issue)
    db.session.commit()

def seed_house_issues():
    houses = House.query.all()
    issues = Issue.query.all()

    for _ in range(NUM_HOUSE_ISSUES):
        selected_issue = random.choice(issues)
        selected_house = random.choice(houses)
        
        house_issue = HouseIssue(
            house_id=selected_house.id,
            issue_id=selected_issue.id,
            status=random.choice(['pending', 'in-progress', 'resolved']),
            house_name=selected_house.description,  
            issue_name=selected_issue.description  
        )
        db.session.add(house_issue)
    db.session.commit()


def assign_tenants_to_houses():
    houses = House.query.all()
    tenants = Tenant.query.all()

    for house in houses:
        if random.choice([True, False]):  
            tenant = random.choice(tenants)
            house.tenant_id = tenant.id
            house.tenant_name = tenant.name  # Set the tenant_name for the house

    db.session.commit()







if __name__ == '__main__':
    with app.app_context():
        db.drop_all()
        db.create_all()
        
        seed_owners()
        seed_properties()
        seed_houses()
        seed_tenants()
        seed_issues()
        seed_house_issues()
        assign_tenants_to_houses()

        print("Database seeded successfully!")
