import os
from concurrent import futures
from sqlalchemy import create_engine
from kafka import KafkaProducer

# Creates sql alchemy database instance.
from app.config import config_by_name
config = config_by_name[os.getenv("ENV") or "test"]
db = create_engine(config.SQLALCHEMY_DATABASE_URI)

# Define base model
from sqlalchemy.orm import declarative_base
model = declarative_base()

# Define session
from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=db)

# Creates kafka producer
KAFKA_SERVER = f'{os.environ["KAFKA_SERVICE_HOST"]}:{os.environ["KAFKA_SERVICE_PORT"]}'
kafka_producer = KafkaProducer(bootstrap_servers=KAFKA_SERVER)


def create_server(location_pb2, location_pb2_grpc,location_servicer):
    import grpc

    # Initialize gRPC server
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
    location_pb2_grpc.add_LocationServiceServicer_to_server(location_servicer.LocationServicer(), server)
    server.add_insecure_port("[::]:5000")

    return server
