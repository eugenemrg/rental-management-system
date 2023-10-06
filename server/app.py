from flask import Flask, request, jsonify
from models import db, Owner, Property, House, Tenant, Issue, HouseIssue
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rental_management.db'
app.config['SECRET_KEY'] = 'a_secret_key'
migrate = Migrate(app, db)
db.init_app(app)

@app.route('/owners/<int:owner_id>', methods=['GET'])
def get_owner_by_id(owner_id):
    owner = Owner.query.get(owner_id)
    if not owner:
        return jsonify({"error": "Owner not found"}), 404
    return jsonify({
        "id": owner.id,
        "name": owner.name,
        "email": owner.email
    })

@app.route('/owners', methods=['POST'])
def create_owner():
    name = request.json.get('name')
    email = request.json.get('email')
    password = request.json.get('password')
    new_owner = Owner(name=name, email=email)
    new_owner.set_password(password)
    db.session.add(new_owner)
    db.session.commit()
    return jsonify({"message": "Owner added!", "id": new_owner.id}), 201

@app.route('/owners/<int:owner_id>/properties', methods=['GET'])
def get_properties_by_owner(owner_id):
    properties = Property.query.filter_by(owner_id=owner_id).all()
    return jsonify([prop.location for prop in properties])

@app.route('/owners/<int:owner_id>/properties', methods=['POST'])
def add_property_to_owner(owner_id):
    location = request.json.get('location')
    new_property = Property(location=location, owner_id=owner_id)
    property_name = request.json.get('property_name')  # Get the property name from the request
    db.session.add(new_property)
    db.session.commit()
    return jsonify({"message": "Property added!", "id": new_property.id}), 201

@app.route('/properties/<int:property_id>/houses', methods=['POST'])
def add_house_to_property(property_id):
    description = request.json.get('description')
    rent = request.json.get('rent')
    new_house = House(description=description, rent=rent, property_id=property_id)
    db.session.add(new_house)
    db.session.commit()
    return jsonify({"message": "House added!", "id": new_house.id}), 201

@app.route('/tenants', methods=['GET'])
def get_tenants():
    tenants = Tenant.query.all()
    return jsonify([tenant.name for tenant in tenants])

@app.route('/tenants', methods=['POST'])
def add_tenant():
    name = request.json.get('name')
    email = request.json.get('email')
    new_tenant = Tenant(name=name, email=email)
    db.session.add(new_tenant)
    db.session.commit()
    return jsonify({"message": "Tenant added!", "id": new_tenant.id}), 201

@app.route('/issues', methods=['GET'])
def list_issues():
    issues = Issue.query.all()
    return jsonify([issue.description for issue in issues])

@app.route('/houses/<int:house_id>/issues/<int:issue_id>', methods=['POST'])
def assign_issue_to_house(house_id, issue_id):
    status = request.json.get('status', 'pending')
    house_issue = HouseIssue(house_id=house_id, issue_id=issue_id, status=status)
    db.session.add(house_issue)
    db.session.commit()
    return jsonify({"message": "Issue assigned to house!"}), 200


# =================== Properties Routes ===================

@app.route('/', methods=['GET'])
def homepage():
    return 'RENTAL MANAGEMENT SYSTEM'



@app.route('/properties', methods=['GET'])
def get_all_properties():
    properties = Property.query.all()
    return jsonify([{
        "id": prop.id,
        "location": prop.location,
         "property_name": prop.property_name,  # Include the property name in the response
        "owner_id": prop.owner_id
    } for prop in properties])




@app.route('/properties', methods=['POST'])
def add_property():
    location = request.json.get('location')
    property_name = request.json.get('property_name')  # Get the property name from the request
    owner_id = request.json.get('owner_id')
    new_property = Property(location=location, owner_id=owner_id)
    db.session.add(new_property)
    db.session.commit()
    return jsonify({"message": "Property added!", "id": new_property.id}), 201

@app.route('/property/<int:property_id>', methods=['PATCH'])
def update_property(property_id):
    prop = Property.query.get(property_id)
    if not prop:
        return jsonify({"error": "Property not found"}), 404

    prop.location = request.json.get('location', prop.location)
    db.session.commit()
    return jsonify({"message": "Property updated!"})

@app.route('/property/<int:property_id>', methods=['DELETE'])
def delete_property(property_id):
    prop = Property.query.get(property_id)
    if not prop:
        return jsonify({"error": "Property not found"}), 404

    db.session.delete(prop)
    db.session.commit()
    return jsonify({"message": "Property deleted!"})

@app.route('/property/<int:property_id>', methods=['GET'])
def get_property_by_id(property_id):
    prop = Property.query.get(property_id)
    if not prop:
        return jsonify({"error": "Property not found"}), 404
    number_of_houses = len(prop.houses)  # Count the number of houses related to this property
    return jsonify({
        "id": prop.id,
        "location": prop.location,
        "property_name": prop.property_name,  # Include the property name in the response
        "owner_id": prop.owner_id,
        "number_of_houses": number_of_houses
    })




# =================== Houses Routes ===================

@app.route('/houses', methods=['GET'])
def get_all_houses():
    houses = House.query.all()
    return jsonify([{
        "id": house.id,
        "description": house.description,
        "rent": house.rent,
        "property_location": house.property.location
    } for house in houses])

@app.route('/houses', methods=['POST'])
def add_new_house():
    description = request.json.get('description')
    rent = request.json.get('rent')
    property_id = request.json.get('property_id')
    new_house = House(description=description, rent=rent, property_id=property_id)
    db.session.add(new_house)
    db.session.commit()
    return jsonify({"message": "House added!", "id": new_house.id}), 201

@app.route('/houses/<int:house_id>', methods=['PATCH'])
def update_house(house_id):
    house = House.query.get(house_id)
    if not house:
        return jsonify({"error": "House not found"}), 404

    house.description = request.json.get('description', house.description)
    house.rent = request.json.get('rent', house.rent)
    db.session.commit()
    return jsonify({"message": "House updated!"})

# =================== Tenants Routes ===================

@app.route('/tenants/<int:tenant_id>', methods=['PATCH'])
def update_tenant(tenant_id):
    tenant = Tenant.query.get(tenant_id)
    if not tenant:
        return jsonify({"error": "Tenant not found"}), 404

    tenant.name = request.json.get('name', tenant.name)
    tenant.email = request.json.get('email', tenant.email)
    db.session.commit()
    return jsonify({"message": "Tenant updated!"})

@app.route('/tenants/<int:tenant_id>', methods=['DELETE'])
def delete_tenant(tenant_id):
    tenant = Tenant.query.get(tenant_id)
    if not tenant:
        return jsonify({"error": "Tenant not found"}), 404

    # Remove tenant details from linked houses
    linked_houses = House.query.filter_by(tenant_id=tenant_id).all()
    for house in linked_houses:
        house.tenant_id = None

    db.session.delete(tenant)
    db.session.commit()
    return jsonify({"message": "Tenant deleted!"})


# =================== House Issues/Reports Routes ===================



@app.route('/house_issues', methods=['GET'])
def get_houses_with_issues():
    house_issues = HouseIssue.query.all()
    return jsonify([{
        "house_id": issue.house_id,
        "issue_id": issue.issue_id,
        "issue_description": issue.issue.description,
        "status": issue.status
    } for issue in house_issues])


if __name__ == '__main__':
    app.run(debug=True)
