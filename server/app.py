

from flask import Flask,request,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import db, Owner, Property, Tenants, Issues, HouseIssue, House


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rentals.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)
migrate = Migrate(app, db)
db.init_app(app)


# from models import db, Owner, Property, Tenants, Issues, HouseIssue, House

@app.route('/', methods=['GET'])
def homepage():
    return 'RENTAL MANAGEMENT SYSTEM'

#gets list of properties
@app.route('/properties', methods=['GET'])
def get_properties():
    properties = Property.query.all()
    property_list = []
    for prop in properties:
        property_data = {
            'id': prop.id,
            'type': prop.type,
            'rooms': prop.rooms,
            'owner_id': prop.owner_id,
            'occupied' : prop.occupied,
            'owner_name': f'{prop.owner.first_name} {prop.owner.last_name}'
        }
        property_list.append(property_data)
    return jsonify(property_list)    


#adds new property
@app.route('/properties', methods=['POST'])
def add_property():
  data = request.json
  new_property = Property(
      type=data['type'],
      rooms=data['rooms'],
      owner_id=data['owner_id'],
      occupied=data['occupied']
      
  )
  db.session.add(new_property)
  db.session.commit()
  return jsonify({'message':'Property added successfully'}), 201

#updates properties using ID
@app.route('/property/<int:id>', methods=['PATCH'])
def update_property(id):
    property = Property.query.get(id)
    if not property:
        return jsonify({'error': 'Property not found'}), 404

    data = request.json
    property.type = data.get('type', property.type)
    property.rooms = data.get('rooms', property.rooms)
    property.owner_id = data.get('owner_id', property.owner_id)
    property.occupied = data.get('occupied', property.occupied)

    db.session.commit()
    return jsonify({'message': 'Property updated successfully'})
 

#deletes a property and its linked houses
@app.route('/property/<int:id>', methods=['DELETE'])
def delete_property(id):
    property = Property.query.get(id)
    if not property:
        return jsonify({'error': 'Property not found'}), 404

    # Delete linked houses
    for house in property.houses:
        db.session.delete(house)

    db.session.delete(property)
    db.session.commit()
    return jsonify({'message': 'Property deleted successfully'})

#gets a list of all houses showing details
@app.route('/houses', methods=['GET'])
def get_houses():
    houses = House.query.all()
    house_list = []
    for house in houses:
        house_data = {
            'id': house.id,
            'unit_id': house.unit_id,
            'rent': house.rent,
            'rooms': house.rooms,
            'property_id': house.property_id,
            'property_details': {
                'type': house.property.type,
                'owner_name': f'{house.property.owner.first_name} {house.property.owner.last_name}'
            }
        }
        house_list.append(house_data)
    return jsonify(house_list)

#adds a new house for a property
@app.route('/houses', methods=['POST'])
def add_house():
    data = request.json
    new_house = House(
        unit_id=data['unit_id'],
        rent=data['rent'],
        rooms=data['rooms'],
        property_id=data['property_id']
    )
    db.session.add(new_house)
    db.session.commit()
    return jsonify({'message': 'House added successfully'}), 201

#update house details using ID
@app.route('/houses/<int:id>', methods=['PATCH'])
def update_house(id):
    house = House.query.get(id)
    if not house:
        return jsonify({'error': 'House not found'}), 404

    data = request.json
    house.unit_id = data.get('unit_id', house.unit_id)
    house.rent = data.get('rent', house.rent)
    house.rooms = data.get('rooms', house.rooms)
    house.property_id = data.get('property_id', house.property_id)

    db.session.commit()
    return jsonify({'message': 'House updated successfully'})

#gets all possible issues
@app.route('/issues', methods=['GET'])
def get_issues():
    issues = Issues.query.all()
    issue_list = [{'id': issue.id, 'name': issue.name, 'description': issue.description} for issue in issues]
    return jsonify(issue_list)

#gets a list of all tenants
@app.route('/tenants', methods=['GET'])
def get_tenants():
    tenants = Tenants.query.all()
    tenant_list = []
    for tenant in tenants:
        tenant_data = {
            'id': tenant.id,
            'name': tenant.name,
            'phone_no': tenant.phone_no,
            'email': tenant.email,
            'due_date': tenant.due_date,
            'payment': tenant.payment,
            'property_id': tenant.property_id
        }
        tenant_list.append(tenant_data)
    return jsonify(tenant_list)

#add a new tenant
@app.route('/tenants', methods=['POST'])
def add_tenant():
    data = request.json
    new_tenant = Tenants(
        name=data['name'],
        phone_no=data['phone_no'],
        email=data['email'],
        due_date=data['due_date'],
        payment=data['payment'],
        property_id=data['property_id']
    )
    db.session.add(new_tenant)
    db.session.commit()
    return jsonify({'message': 'Tenant added successfully'}), 201

#update details of a tenant using ID
@app.route('/tenants/<int:id>', methods=['PATCH'])
def update_tenant(id):
    tenant = Tenants.query.get(id)
    if not tenant:
        return jsonify({'error': 'Tenant not found'}), 404

    data = request.json
    tenant.name = data.get('name', tenant.name)
    tenant.phone_no = data.get('phone_no', tenant.phone_no)
    tenant.email = data.get('email', tenant.email)
    tenant.due_date = data.get('due_date', tenant.due_date)
    tenant.payment = data.get('payment', tenant.payment)
    tenant.property_id = data.get('property_id', tenant.property_id)

    db.session.commit()
    return jsonify({'message': 'Tenant updated successfully'})

# delete a tenant and remove id details from the house
@app.route('/tenants/<int:id>', methods=['DELETE'])
def delete_tenant(id):
    tenant = Tenants.query.get(id)
    if not tenant:
        return jsonify({'error': 'Tenant not found'}), 404
    
    houses_with_tenant = House.query.filter_by(property_id=tenant.property_id)
    for house in houses_with_tenant:
        if house.tenant_id == id:
            house.tenant_id = None

    db.session.delete(tenant)
    db.session.commit()
    return jsonify({'message': 'Tenant deleted successfully'})

#gets list of house with issues
@app.route('/house_issues', methods=['GET'])
def get_houses_with_issues():
    houses_with_issues = House.query.filter(House.issues.any()).all()
    house_list = []
    for house in houses_with_issues:
        house_data = {
            'id': house.id,
            'unit_id': house.unit_id,
            'rent': house.rent,
            'rooms': house.rooms,
            'property_id': house.property_id,
            'property_details': {
                'type': house.property.type,
                'owner_name': f'{house.property.owner.first_name} {house.property.owner.last_name}'
            },
            'issues': [issue.name for issue in house.issues]  
        }
        house_list.append(house_data)
    return jsonify(house_list)

if __name__ == '__main__':
    app.run(debug=True)