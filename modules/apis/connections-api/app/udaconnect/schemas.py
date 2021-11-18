from app.udaconnect.models import Connection, Location, Person
from marshmallow import Schema, fields


class LocationSchema(Schema):
    id = fields.Integer()
    person_id = fields.Integer()
    longitude = fields.String(attribute="longitude")
    latitude = fields.String(attribute="latitude")
    creation_time = fields.DateTime()

    class Meta:
        model = Location


class PersonSchema(Schema):
    id = fields.Integer()
    first_name = fields.String()
    last_name = fields.String()
    company_name = fields.String()

    class Meta:
        model = Person


class ConnectionSchema(Schema):
    person_id = fields.Integer()
    location_id = fields.Integer()
    connection_time = fields.DateTime()
    distance = fields.Float()
    creation_time = fields.DateTime()
    update_time = fields.DateTime()

    class Meta:
        model = Connection

class ContactSchema(Schema):
    location = fields.Nested(LocationSchema)
    person = fields.Nested(PersonSchema)