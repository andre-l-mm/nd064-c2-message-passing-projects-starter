import os
import requests
from .models import Person
from typing import List

class PersonsApi:
    url = f'http://{os.environ["UDACONNECT_PERSONS_API_SERVICE_HOST"]}:{os.environ["UDACONNECT_PERSONS_API_SERVICE_PORT"]}/api/persons'

    @staticmethod
    def get_persons() -> List[Person]:
        response = requests.get(PersonsApi.url)
        return response.json()
