# UdaConnect Apis

## Local Development Instructions

### Installing psql

```
# MacOS Install and add folder to path in your bash profile configuration
brew install libpq
echo 'export PATH="/usr/local/opt/libpq/bin:$PATH"' >> /Users/andremagalhaes/.bash_profile
```

### Connecting with psql
```
# Keep port-forward running in a separate terminal to allow for connections on localhost:5432
kubectl port-forward svc/postgres 5432:5432

# Connect with psql
psql -h localhost -p 5432 -U ct_admin geoconnections
```

### Running apis locally

```
# Create virtual environment
python3 -m venv .venv

# Activate virtual environment (always run this when openning a new terminal)
cd .venv
source bin/activate

# Upgrade pip
pip install --upgrade pip

# Geos package required by some of the python packages
brew install geos

# Go to api folder
cd modules/api

# Install required packages - Exporting LDFLAGS required to install psycopg2
env LDFLAGS="-I/usr/local/opt/openssl/include -L/usr/local/opt/openssl/lib" pip install -r requirements.txt

# Make sure database is accessible on localhost by running this command on a separate terminal
kubectl port-forward svc/postgres 5432:5432

# Create .env file with the following settings
DB_USERNAME=ct_admin
DB_NAME=geoconnections
DB_HOST=localhost
DB_PORT=5432
DB_PASSWORD=wowimsosecure

# Using flask command line to start the application
# This can be used to automatically apply source code changes but runs on port 5000
FLASK_ENV=dev flask run

# Go to http://127.0.0.1:5000/api/
```

## Building 

### Build Docker Images

```
# Location api
cd modules/apis/locations-api
docker build -f ./Dockerfile -t udaconnect-locations-api .

# Person api
cd modules/apis/persons-api
docker build -f ./Dockerfile -t udaconnect-persons-api .

# Connections api
cd modules/apis/connections-api
docker build -f ./Dockerfile -t udaconnect-connections-api .

# Web App
cd modules/frontend
docker build -f ./Dockerfile -t udaconnect-app .
```

### Push Docker Images

```
docker tag udaconnect-locations-api andremagalhaes/udaconnect-locations-api
docker push andremagalhaes/udaconnect-locations-api

docker tag udaconnect-persons-api andremagalhaes/udaconnect-persons-api
docker push andremagalhaes/udaconnect-persons-api

docker tag udaconnect-connections-api andremagalhaes/udaconnect-connections-api
docker push andremagalhaes/udaconnect-connections-api

docker tag udaconnect-app andremagalhaes/udaconnect-app
docker push andremagalhaes/udaconnect-app
```

### Deployment to Kubernetes

```
# Configuration
kubectl apply -f deployment/db-configmap.yaml
kubectl apply -f deployment/db-secret.yaml
kubectl apply -f deployment/postgres.yaml

# Apis
kubectl apply -f deployment/udaconnect-locations-api.yaml
kubectl apply -f deployment/udaconnect-persons-api.yaml
kubectl apply -f deployment/udaconnect-connections-api.yaml

# Web Application
kubectl apply -f deployment/udaconnect-app.yaml
```

### Verifying it Works

* `http://localhost:30002/` - Locations API - OpenAPI Documentation
* `http://localhost:30002/api/` - Locations API - Base path for API
* `http://localhost:30003/` - Persons API - OpenAPI Documentation
* `http://localhost:30003/api/` - Persons API - Base path for API
* `http://localhost:30004/` - Connections API - OpenAPI Documentation
* `http://localhost:30004/api/` - Connections API - Base path for API 
* `http://localhost:30000/` - Frontend ReactJS Application

### Kubectl Others

```
# Restarting deployment to apply image changes 
kubectl rollout restart deploy [DEPLOYMENT_NAME]

# Get pod logs in case of errors
kubectl logs [POD_NAME]
```