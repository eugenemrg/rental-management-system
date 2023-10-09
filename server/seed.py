from app import app, db, Owner, Property, House, Tenant, Issue, HouseIssue
from faker import Faker
from random import choice as rc, randint

fake = Faker()

with app.app_context():
    Owner.query.delete()
    Property.query.delete()
    House.query.delete()
    Tenant.query.delete()
    Issue.query.delete()
    HouseIssue.query.delete()
    
    owners = []
    for _ in range(10):
        password = fake.password(length=8)
        owner = Owner(
            first_name = fake.first_name(),
            last_name = fake.last_name(),
            email = fake.ascii_safe_email(),
            password_hash = password
        )
        print(f'Owner: {owner.email}, password: {password}')
        owners.append(owner)
    
    db.session.add_all(owners)
    db.session.commit()
    
    tenants = []
    for _ in range(200):
        tenant = Tenant(
            first_name = fake.first_name(),
            last_name = fake.last_name(),
            email = fake.ascii_safe_email()
        )
        tenants.append(tenant)
    
    db.session.add_all(tenants)
    db.session.commit()
    
    properties = []
    for owner in owners:
        for _ in range(randint(4, 12)):
            property = Property(
                name = f"{fake.city()} {rc(['Apartment', 'Villa', 'Place', 'Residence', 'Estate'])}",
                location = fake.address(),
                owner = owner
            )
            properties.append(property)
    
    db.session.add_all(properties)
    db.session.commit()
    
    houses = []
    for property in properties:
        for i in range(randint(20, 80)):
            house = House(
                unit = f"{rc('ABCDE')}{i+1}",
                tenant = rc(tenants),
                property = property
            )
            houses.append(house)
    
    db.session.add_all(houses)
    db.session.commit()
    
    issues_list = [
        {
            'name': 'Leaky Faucet',
            'description': 'The faucet in the apartment is dripping water constantly.'
        },
        {
            'name': 'Clogged Drain',
            'description': 'The drain in the apartment is not draining water properly and is causing backups.'
        },
        {
            'name': 'No Heat',
            'description': 'The heater in the apartment is not working and the apartment is cold.'
        },
        {
            'name': 'Broken Window',
            'description': 'There is a broken window in the apartment that needs to be repaired or replaced.'
        },
        {
            'name': 'Pest Infestation',
            'description': 'The apartment is infested with pests such as mice, rats, or insects.'
        },
        {
            'name': 'Noise Complaints',
            'description': 'The tenant is experiencing excessive noise from neighboring apartments or outside the building.'
        },
        {
            'name': 'Appliance Malfunction',
            'description': 'One or more of the appliances in the apartment are not functioning properly.'
        },
        {
            'name': 'Mold or Water Damage',
            'description': 'There is mold or water damage in the apartment that needs to be remediated.'
        },
        {
            'name': 'Electricity Outage',
            'description': 'The apartment is experiencing a power outage, which may be a building-wide problem or due to faulty wiring in the apartment.'
        },
        {
            'name': 'Bathroom Leak',
            'description': 'There is a leak in the bathroom that is causing water damage or mold growth.'
        },
        {
            'name': 'Security Concerns',
            'description': 'There are security concerns in the apartment complex, such as a lack of working locks on doors or windows.'
        },
        {
            'name': 'Air Conditioning Problem',
            'description': 'The air conditioning in the apartment is not working properly or not at all.'
        },
        {
            'name': 'Paint or Wallpaper Peeling',
            'description': 'The paint or wallpaper in the apartment is peeling, which can be unsightly and may indicate underlying problems like water damage.'
        },
        {
            'name': 'Roof Leak',
            'description': 'There is a leak in the roof of the building or in the apartment, which can cause water damage to belongings and mildew growth.'
        },
        {
            'name': 'Access Issues',
            'description': 'The tenant is experiencing difficulty accessing the apartment, such as due to a broken elevator or a lack of accessible entrances.'
        },
        {
            'name': 'Parking Problems',
            'description': 'There are problems with parking at the apartment complex, such as a lack of available spots or safety concerns.'
        },
        {
            'name': 'Inadequate Heating or Cooling',
            'description': 'The temperature in the apartment is consistently uncomfortable, either too hot or too cold.'
        },
        {
            'name': 'Structural Problems',
            'description': 'There are structural problems with the apartment or building, such as cracks in the walls or foundation issues.'
        },
        {
            'name': 'Garbage Disposal Problems',
            'description': 'The garbage disposal in the apartment is not working or is causing a foul smell.'
        },
        {
            'name': 'Unresponsive Landlord or Management',
            'description': 'The tenant is unable to get in touch with the landlord or management team to report issues or get necessary repairs done.'
        }
    ]
    
    issues = []
    for issue_type in issues_list:
        issue = Issue(
            name = issue_type['name'],
            description = issue_type['description']
        )
        issues.append(issue)
    
    db.session.add_all(issues)
    db.session.commit()
    
    house_issues = []
    for _ in range(30):
        hi = HouseIssue(
            house = rc(houses),
            issue = rc(issues),
            detail = fake.paragraph(nb_sentences=3),
            status = 'not fixed' if (randint(1, 4)) % 2 == 0 else 'fixed'
        )
        house_issues.append(hi)
    
    db.session.add_all(house_issues)
    db.session.commit()
    
# sample email, password with current commit

# Owner: robertsroger@example.com, password: i(t2H)tr
# Owner: pmosley@example.com, password: 9%1*T6As
# Owner: brandonwallace@example.net, password: ^35viTmLjU
# Owner: norrisrobin@example.net, password: bmm+4BtK
# Owner: mandycollins@example.com, password: 1$Y3U4gO
# Owner: emily37@example.com, password: tFk!O1Al7If
# Owner: heather21@example.com, password: *VI8R+ps
# Owner: margaret18@example.org, password: YL+7Kolf
# Owner: nathaniel99@example.net, password: _6L7StwM
# Owner: ashleyhunt@example.net, password: @7aaJ&Kl

# ------------END OF NEW SEED-------------
# from models import db, Owner, Property, House, Tenant, Issue, HouseIssue
# from app import app
# from faker import Faker
# from random import choice as rc, randint
# # import random

# fake = Faker()

# # Number of fake entries
# NUM_OWNERS = 30
# NUM_PROPERTIES_PER_OWNER = 2
# NUM_HOUSES_PER_PROPERTY = 5
# NUM_TENANTS = 30
# NUM_ISSUES = 10
# NUM_HOUSE_ISSUES = 20

# def seed_owners():
#     for _ in range(NUM_OWNERS):
#         owner = Owner(name=fake.name(), email=fake.email())
#         owner.set_password(fake.password())
#         db.session.add(owner)
#     db.session.commit()

# def seed_properties():
#     owners = Owner.query.all()
#     for owner in owners:
#         for _ in range(random.randint(1, NUM_PROPERTIES_PER_OWNER)):
#             prop = Property(
#                 location=fake.address(), 
#                 owner_id=owner.id, 
#                 property_name=fake.company(),  
#                 owner_name=owner.name  
#             )
#             db.session.add(prop)
#     db.session.commit()

# def seed_houses():
#     properties = Property.query.all()
#     for prop in properties:
#         for _ in range(random.randint(1, NUM_HOUSES_PER_PROPERTY)):
#             house = House(
#                 description=fake.sentence(), 
#                 rent=fake.random_int(500, 5000), 
#                 property_id=prop.id, 
#                 balance=random.uniform(0, 1000),  
#                 property_name=prop.property_name  
#             )
#             db.session.add(house)
#     db.session.commit()


# def seed_tenants():
#     for _ in range(NUM_TENANTS):
#         tenant = Tenant(name=fake.name(), email=fake.email())
#         db.session.add(tenant)
#     db.session.commit()

# def seed_issues():
#     for _ in range(NUM_ISSUES):
#         issue = Issue(description=fake.sentence())
#         db.session.add(issue)
#     db.session.commit()

# def seed_house_issues():
#     houses = House.query.all()
#     issues = Issue.query.all()

#     for _ in range(NUM_HOUSE_ISSUES):
#         selected_issue = random.choice(issues)
#         selected_house = random.choice(houses)
        
#         house_issue = HouseIssue(
#             house_id=selected_house.id,
#             issue_id=selected_issue.id,
#             status=random.choice(['pending', 'in-progress', 'resolved']),
#             house_name=selected_house.description,  
#             issue_name=selected_issue.description  
#         )
#         db.session.add(house_issue)
#     db.session.commit()


# def assign_tenants_to_houses():
#     houses = House.query.all()
#     tenants = Tenant.query.all()

#     for house in houses:
#         if random.choice([True, False]):  
#             tenant = random.choice(tenants)
#             house.tenant_id = tenant.id
#             house.tenant_name = tenant.name  # Set the tenant_name for the house

#     db.session.commit()







# if __name__ == '__main__':
#     with app.app_context():
#         db.drop_all()
#         db.create_all()
        
#         seed_owners()
#         seed_properties()
#         seed_houses()
#         seed_tenants()
#         seed_issues()
#         seed_house_issues()
#         assign_tenants_to_houses()

#         print("Database seeded successfully!")
