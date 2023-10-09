from flask import Flask, make_response, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Resource, Api
from flask_marshmallow import Marshmallow
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, SQLAlchemySchema, auto_field
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, get_jwt, JWTManager
from flask_bcrypt import Bcrypt
from sqlalchemy.ext.hybrid import hybrid_property
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rental_management.db'
app.config["JWT_SECRET_KEY"] = "test@1234"
jwt = JWTManager(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
ma = Marshmallow(app)
api = Api(app)
bcrypt = Bcrypt(app)
CORS(app)

class Owner(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    email = db.Column(db.String)
    _password_hash = db.Column(db.String)
    properties = db.relationship('Property', backref='owner', lazy=True)
    
    @hybrid_property
    def password_hash(self):
        return self._password_hash

    @password_hash.setter
    def password_hash(self, password):
        password_hash = bcrypt.generate_password_hash(
            password.encode('utf-8'))
        self._password_hash = password_hash.decode('utf-8')

    def authenticate(self, password):
        return bcrypt.check_password_hash(
            self._password_hash, password.encode('utf-8'))
    
class Property(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    location = db.Column(db.String)
    owner_id = db.Column(db.Integer, db.ForeignKey('owner.id'))
    
    houses = db.relationship('House', backref='property', lazy=True)
    
class House(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    unit = db.Column(db.String)
    tenant_id = db.Column(db.Integer, db.ForeignKey('tenant.id'))
    property_id = db.Column(db.Integer, db.ForeignKey('property.id'))

class Tenant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    email = db.Column(db.String)
    
    houses_list = db.relationship('House', backref='tenant', lazy=True)

class Issue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)

class HouseIssue(db.Model):
    id = db.Column(db.Integer, primary_key=id)
    house_id = db.Column(db.Integer, db.ForeignKey('house.id'))
    issue_id = db.Column(db.Integer, db.ForeignKey('issue.id'))
    detail = db.Column(db.String)
    status = db.Column(db.String)
    
    house = db.relationship('House', backref=db.backref('house_issue', cascade='all, delete-orphan'))
    issue = db.relationship('Issue', backref=db.backref('house_issue', cascade='all, delete-orphan'))

# Adding schema
class IssueSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Issue

class TenantSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Tenant

class SinglePropertySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Property

class HouseSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = House
    
    tenant = ma.Nested(TenantSchema, many=False)
    property = ma.Nested(SinglePropertySchema, many=False)

class PropertySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Property
    
    houses = ma.Nested(HouseSchema, many=True)

class OwnerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Owner
    
    properties = ma.Nested(PropertySchema, many=True)
    
class HouseIssueSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = HouseIssue
    
    house = ma.Nested(HouseSchema, many=False)
    issue = ma.Nested(IssueSchema, many=False)

# Adding routes

class Index(Resource):
    def get(self):
        return {'message': 'RMT API'}

api.add_resource(Index, '/')

class LoginResource(Resource):
    def post(self):
        email = request.json.get("email", None)
        password = request.json.get("password", None)
        
        owner = Owner.query.filter_by(email=email).first()
        
        if not owner or not owner.authenticate(password):
            return make_response(
                jsonify({"msg": "Bad username or password"}),
                401
            )
        
        additional_claims = {"id": owner.id, "email": owner.email}
        access_token = create_access_token(identity=owner.id, additional_claims=additional_claims)
        return jsonify(access_token=access_token)

api.add_resource(LoginResource, '/login')

class OwnerResource(Resource):
    @jwt_required()
    def get(self):
        return make_response(
            jsonify(OwnerSchema().dump(Owner.query.first())),
            200
        )
    
    @jwt_required()
    def post(self):
        owner = Owner(
            first_name = request.json.get("fname"),
            last_name = request.json.get("lname"),
            email = request.json.get("email"),
            password_hash = request.json.get("password")
        )
        db.session.add(owner)
        db.session.commit()
        
        return make_response(
            jsonify({'msg': 'success'}),
            201
        )
        
api.add_resource(OwnerResource, '/owners')

class OwnerIdResource(Resource):
    @jwt_required()
    def get(self):
        return make_response(
            jsonify(OwnerSchema().dump(Owner.query.first())),
            200
        )
api.add_resource(OwnerIdResource, '/owners/<int:id>')

class PropertyResource(Resource):
    @jwt_required()
    def get(self):
        claims = get_jwt()
        owner_id = claims['id']
        owner = Owner.query.filter_by(id = int(owner_id)).first()
        
        return make_response(
            jsonify({'properties': [PropertySchema().dump(property) for property in owner.properties]}),
            200
        )
    
    @jwt_required()    
    def post(self):
        claims = get_jwt()
        owner_id = claims['id']
        owner = Owner.query.filter_by(id = int(owner_id)).first()
        
        property = Property(
            name = request.json.get("name", None),
            location = request.json.get("location", None),
            owner = owner
        )
        
        db.session.add(property)
        db.session.commit()
        
        return make_response(
            jsonify(PropertySchema().dump(Property.query.filter_by(id = property.id).first())),
            200
        )
        
api.add_resource(PropertyResource, '/properties')

class PropertyIdResource(Resource):
    @jwt_required()
    def get(self, id):
        return make_response(
            jsonify(PropertySchema().dump(Property.query.filter_by(id = id).first())),
            200
        )
    
    @jwt_required()
    def patch(self, id):
        property = Property.query.filter_by(id = id).first()
        changes = request.json

        for key in changes:
            setattr(property, key, changes[key])

        db.session.add(property)
        db.session.commit()

        return make_response(
            jsonify(PropertySchema().dump(property)),
            200
        )
        
api.add_resource(PropertyIdResource, '/properties/<int:id>')

class HousesResource(Resource):
    @jwt_required()
    def get(self):
        claims = get_jwt()
        owner_id = claims['id']
        return make_response(
            jsonify([HouseSchema().dump(house) for house in House.query.all() if house.property.owner.id == owner_id]),
            200
        )
api.add_resource(HousesResource, '/houses')

# get all houses for a property, add a house by a property
class HousesByPropertyIdResource(Resource):
    @jwt_required()
    def get(self, property_id):
        return make_response(
            jsonify({'houses': [HouseSchema().dump(house) for house in House.query.filter_by(property_id = property_id)]}),
            200
        )
    
    @jwt_required()    
    def post(self, property_id):
        house = House(
                unit = request.json.get("unit", None),
                tenant_id = request.json.get("tenant", None),
                property = Property.query.filter_by(id = property_id).first()
            )
        db.session.add(house)
        db.session.commit()
        
        return make_response(
            jsonify(HouseSchema().dump(house)),
            200
        )
api.add_resource(HousesByPropertyIdResource, '/houses/<int:property_id>')

# get, patch and delete house instance
class HouseResource(Resource):
    @jwt_required()
    def get(self, house_id):
        return make_response(
            jsonify(HouseSchema().dump(House.query.filter_by(id = house_id).first())),
            200
        )
    
    @jwt_required()
    def patch(self, house_id):
        house = House.query.filter_by(id = house_id).first()
        
        changes = request.json

        for key in changes:
            setattr(house, key, changes[key])

        db.session.add(house)
        db.session.commit()

        return make_response(
            jsonify(HouseSchema().dump(house)),
            200
        )
        
    @jwt_required()
    def delete(self, house_id):
        for house in House.query.filter_by(id = house_id).all():
            
            house.tenant_id = None
            db.session.commit()
            
            db.session.delete(house)
            db.session.commit()
            
        return make_response(
            jsonify(HouseSchema().dump(House.query.filter_by(id = house_id).first())),
            200
        )
        
        
api.add_resource(HouseResource, '/house/<int:house_id>')

class TenantResource(Resource):
    @jwt_required()
    def get(self):
        return make_response(
            jsonify([TenantSchema().dump(tenant) for tenant in Tenant.query.all()]),
            200
        )
    
    @jwt_required()
    def post(self):
        tenant = Tenant(
            first_name = request.json.get("fname", None),
            last_name = request.json.get("lname", None),
            email = request.json.get("email", None)
        )
        db.session.add(tenant)
        db.session.commit()
        
        return make_response(
            jsonify(TenantSchema().dump(tenant))
        )
        
api.add_resource(TenantResource, '/tenants')

class TenantByIdResource(Resource):
    @jwt_required()
    def get(self, tenant_id):
        return make_response(
            jsonify(TenantSchema().dump(Tenant.query.filter_by(id = tenant_id).first())),
            200
        )
    
    @jwt_required()
    def patch(self, tenant_id):
        tenant = House.query.filter_by(id = tenant_id).first()
        
        changes = request.json

        for key in changes:
            setattr(tenant, key, changes[key])

        db.session.add(tenant)
        db.session.commit()

        return make_response(
            jsonify(TenantSchema().dump(tenant)),
            200
        )
    
    @jwt_required()
    def delete(self, tenant_id):
        for tenant in Tenant.query.filter_by(id=tenant_id).all():
            db.session.delete(tenant)
            db.session.commit()
        
        return make_response(
            jsonify(TenantSchema().dump(Tenant.query.filter_by(id = tenant_id).first())),
            200
        )
        
api.add_resource(TenantByIdResource, '/tenant/<int:tenant_id>')

class HouseIssueResource(Resource):
    @jwt_required()
    def get(self):
        claims = get_jwt()
        owner_id = claims['id']
        return make_response(
            jsonify([HouseIssueSchema().dump(h_i) for h_i in HouseIssue.query.all() if h_i.house.property.owner.id == owner_id]),
            200
        )
    
    @jwt_required()
    def post(self):
        h_i = HouseIssue(
            house_id = request.json.get("house_id", None),
            issue_id = request.json.get("issue_id", None),
            detail = request.json.get("detail", None),
            status = 'not fixed'
        )
        db.session.add(h_i)
        db.session.commit()
        
        return make_response(
            jsonify(HouseIssueSchema().dump(h_i)),
            200
        )
        
api.add_resource(HouseIssueResource, '/issues')

class HouseIssueIdResource(Resource):
    @jwt_required()
    def get(self, id):
        return make_response(
            jsonify(HouseIssueSchema().dump(HouseIssue.query.filter_by(id = id).first())),
            200
        )
    
    @jwt_required()
    def delete(self, id):
        h_i = HouseIssue.query.filter_by(id = id).first()
        
        db.session.delete(h_i)
        db.session.commit()
        
        return make_response(
            jsonify(HouseIssueSchema().dump(HouseIssue.query.filter_by(id = id).first())),
            200
        )
    
    @jwt_required
    def patch(self, id):
        h_i = HouseIssue.query.filter_by(id = id).first()
        
        changes = request.json

        for key in changes:
            setattr(h_i, key, changes[key])

        db.session.add(h_i)
        db.session.commit()

        return make_response(
            jsonify(HouseIssueSchema().dump(h_i)),
            200
        )
        
api.add_resource(HouseIssueIdResource, '/issues/<int:id>')

if __name__ == '__main__':
    app.run(port=5559, debug=True)