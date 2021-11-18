from app.udaconnect.models import Location, Person, Connection  # noqa
from app.udaconnect.schemas import LocationSchema, PersonSchema, ConnectionSchema  # noqa


def register_routes(api, app, root="api"):
    from app.udaconnect.controllers import api as udaconnect_api

    api.add_namespace(udaconnect_api, path=f"/{root}")


def create_tables(app, db):
    with app.app_context():
        db.create_all()