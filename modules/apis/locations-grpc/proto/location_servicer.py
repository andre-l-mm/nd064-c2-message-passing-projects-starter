import location_pb2
import location_pb2_grpc
from app.udaconnect.services import LocationService


class LocationServicer(location_pb2_grpc.LocationServiceServicer):
    def Create(self, request, context):
        location = LocationMapping.to_dictionary(request)

        created = LocationService.create(location)

        location['id'] = created.id

        return location_pb2.LocationMessage(**location)


class LocationMapping():
    @staticmethod
    def to_dictionary(request):
        return {
            "person_id": request.person_id,
            "longitude": request.longitude,
            "latitude": request.latitude,
            "creation_time": request.creation_time,
        }
