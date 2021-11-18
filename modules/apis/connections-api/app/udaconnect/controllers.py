from datetime import datetime
from app.udaconnect.models import Contact
from app.udaconnect.schemas import ContactSchema
from app.udaconnect.services import ConnectionService
from flask import request
from flask_accepts import accepts, responds
from flask_restx import Namespace, Resource
from typing import Optional, List

DATE_FORMAT = "%Y-%m-%d"

api = Namespace("UdaConnect", description="Connections via geolocation.")  # noqa


@api.route("/connections")
@api.param("person_id", "Person ID", _in="query", required=True)
@api.param("start_date", "Lower bound of date range", _in="query", required=True)
@api.param("end_date", "Upper bound of date range", _in="query", required=True)
@api.param("distance", "Proximity to a given user in meters", _in="query")
class ConnectionDataResource(Resource):
    @responds(schema=ContactSchema, many=True)
    def get(self) -> List[Contact]:
        person_id: int = request.args.get("person_id")
        start_date: datetime = datetime.strptime(
            request.args["start_date"], DATE_FORMAT
        )
        end_date: datetime = datetime.strptime(request.args["end_date"], DATE_FORMAT)
        distance: Optional[int] = request.args.get("distance", 5)

        results = ConnectionService.find_contacts(
            person_id=person_id,
            start_date=start_date,
            end_date=end_date,
            meters=distance,
        )

        return results
