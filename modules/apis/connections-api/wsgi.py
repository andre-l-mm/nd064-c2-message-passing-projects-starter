import os
import sys

from app import create_app


def start_consumer(app):
    import threading
    from app.udaconnect.services import ConnectionService

    consumer = threading.Thread(target=ConnectionService.start_locations_consumer, args=[app])
    consumer.daemon = True
    consumer.start()


if os.getenv("FLASK_ENV") == "dev":
    from dotenv import load_dotenv
    load_dotenv()

app = create_app(os.getenv("FLASK_ENV") or "test")
if __name__ == "__main__":
    app.run(debug=True)

# Start kafka locations topic consumer.
start_consumer(app)