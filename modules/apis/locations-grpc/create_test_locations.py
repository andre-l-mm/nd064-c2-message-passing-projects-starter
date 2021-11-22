import sys
import grpc
sys.path.append("../locations-grpc/proto")
from proto import location_pb2, location_pb2_grpc

"""
Sample implementation of a writer that creates new locations using grpc.
"""

print("Sending sample locations using grpc")

channel = grpc.insecure_channel("localhost:5000")
stub = location_pb2_grpc.LocationServiceStub(channel)

# Update this with desired payload
location = location_pb2.LocationMessage(
    person_id=9,
    longitude="37.55363",
    latitude="-122.290883",
    creation_time="2020-07-07T12:40:06"
)

response = stub.Create(location)

print(response)
