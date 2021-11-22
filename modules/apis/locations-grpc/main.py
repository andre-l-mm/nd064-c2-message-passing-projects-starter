import os
import sys
import time

if os.getenv("ENV") == "dev":
    from dotenv import load_dotenv
    load_dotenv()

sys.path.append("./proto")
from proto import location_pb2, location_pb2_grpc, location_servicer
from app import create_server

server = create_server(location_pb2, location_pb2_grpc, location_servicer)
if __name__ == "__main__":
    server.start()
    print('GRPC server started')

# Keep server alive.
try:
    while True:
        time.sleep(86400)
except KeyboardInterrupt:
    server.stop(0)