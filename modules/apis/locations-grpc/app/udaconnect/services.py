import logging
from typing import Dict
from app import db, Session, kafka_producer
from app.udaconnect.models import Location
from app.udaconnect.schemas import LocationSchema
from geoalchemy2.functions import ST_Point

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("udaconnect-api")

TOPIC_NAME = 'locations'

session = Session()

class LocationService:
    @staticmethod
    def create(location: Dict) -> Location:
        validation_results: Dict = LocationSchema().validate(location)
        if validation_results:
            logger.warning(f"Unexpected data format in payload: {validation_results}")
            raise Exception(f"Invalid payload: {validation_results}")

        # Add location to the database.
        new_location = Location()
        new_location.person_id = location["person_id"]
        new_location.creation_time = location["creation_time"]
        new_location.coordinate = ST_Point(location["latitude"], location["longitude"])
        session.add(new_location)
        session.commit()

        # Send location to Kafka topic for consumption by connections api.
        location_schema = LocationSchema()
        kafka_producer.send(TOPIC_NAME, location_schema.dumps(new_location).encode('utf-8'))
        kafka_producer.flush()

        return new_location
