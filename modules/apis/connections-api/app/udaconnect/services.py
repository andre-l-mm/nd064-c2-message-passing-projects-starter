import os
import logging
from datetime import datetime, timedelta
from typing import Dict, List
from app import db
from kafka import KafkaConsumer
from app.udaconnect.models import Connection, Location, Person, Contact
from app.udaconnect.schemas import LocationSchema
from geoalchemy2.functions import ST_Point
from sqlalchemy.sql import text, update
from .api_clients import PersonsApi

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("udaconnect-api")


class ConnectionService:
    @staticmethod
    def start_locations_consumer(app):
        with app.app_context():
            LOCATIONS_TOPIC = 'locations'
            KAFKA_SERVER = f'{os.environ["KAFKA_SERVICE_HOST"]}:{os.environ["KAFKA_SERVICE_PORT"]}'
            kafka_consumer = KafkaConsumer(LOCATIONS_TOPIC, bootstrap_servers=KAFKA_SERVER, group_id='connections_api')

            logger.info('Kafka locations topic consumer started')

            query = text(
                """
            SELECT    person_id, id, creation_time, MIN(ST_Distance(ST_Point(:latitude,:longitude), coordinate))
            FROM      location
            WHERE     ST_DWithin(coordinate::geography,ST_SetSRID(ST_MakePoint(:latitude,:longitude),4326)::geography, :meters)
            AND       person_id != :person_id
            AND       TO_DATE(:start_date, 'YYYY-MM-DD') <= creation_time
            AND       TO_DATE(:end_date, 'YYYY-MM-DD') > creation_time
            GROUP BY  person_id, id, creation_time;
            """
            )

            location_schema = LocationSchema()
            for record in kafka_consumer:
                logger.info('New location received from kafka topic')
                location = location_schema.loads(record.value.decode('utf-8'))

                params = {
                    "person_id": location['person_id'],
                    "longitude": location['longitude'],
                    "latitude": location['latitude'],
                    "meters": 100,
                    "start_date": location['creation_time'].strftime("%Y-%m-%d"),
                    "end_date": (location['creation_time'] + timedelta(days=1)).strftime("%Y-%m-%d"),
                }

                for (
                        exposed_person_id,
                        location_id,
                        creation_time,
                        exposed_distance,
                ) in db.engine.execute(query, **params):
                    direct_connection = Connection(
                        person_id=location['person_id'],
                        location_id=location_id,
                        connection_time=creation_time,
                        distance=exposed_distance,
                    )

                    opposite_connection = Connection(
                        person_id=exposed_person_id,
                        location_id=location['id'],
                        connection_time=location['creation_time'],
                        distance=exposed_distance,
                    )

                    # Only add connections if not duplicated and keeps the shortest distance in case it is.
                    ConnectionService.add_or_update(db, direct_connection)
                    ConnectionService.add_or_update(db, opposite_connection)

                # Commit one time after all connections added.
                db.session.commit()

                logger.info('Completed computing and adding connections for new location')

    @staticmethod
    def add_or_update(db, connection):
        existing = (db.session.query(Connection)
                    .filter(Connection.person_id == connection.person_id)
                    .filter(Connection.location_id == connection.location_id)
                    .first())

        if existing is None:
            db.session.add(connection)
        elif existing.distance > connection.distance:
            existing.distance = connection.distance
            existing.update_time = datetime.utcnow()


    @staticmethod
    def find_contacts(person_id: int, start_date: datetime, end_date: datetime, meters=5) -> List[Contact]:
        """
        Finds all Person who have been within a given distance of a given Person within a date range.
        """
        connections: List = (db.session.query(Connection)
            .filter(Connection.person_id == person_id)
            .filter(Connection.connection_time < end_date)
            .filter(Connection.connection_time >= start_date)
            .filter(Connection.distance <= meters)
            .all())

        # Cache all users in memory for quick lookup
        person_map: Dict[str, Person] = {person['id']: person for person in PersonsApi.get_persons()}

        result: List[Contact] = []

        for (connection) in connections:
            result.append(Contact(person=person_map[connection.location.person_id], location=connection.location))

        return result
