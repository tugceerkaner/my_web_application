# Application Details
This project is a web application with a Python backend and an HTML/JavaScript frontend.

## Project structure

```text
.
├── backend/
│ ├── app.py
│ ├── requirements.txt
│ ├── Dockerfile
│ └── .env
├── frontend/
│ ├── index.html
│ ├── styles.css
│ └── Dockerfile
├── deployment/
│ ├── backend-deployment.yaml
│ ├── backend-service.yaml
│ ├── frontend-deployment.yaml
│ ├── frontend-service.yaml
├── .gitignore
├── README.md
```

## Getting Started

### Prerequisites

- Docker
- Kubernetes (kubectl)
- Google Cloud SDK (gcloud)
- PostgreSQL


### Setting Up Environment Variables

Create a `.env` file in the `backend` directory with the following content:

```
DB_HOST=YOUR_DB_HOSTNAME
DB_PORT=YOUR_DB_PORT
DB_NAME=YOUR_DB_NAME
DB_USER=YOUR_DB_USER_NAME
DB_PASSWORD=YOUR_DB_PASSWORD
```


### Running Locally

#### Docker Compose File
To check web application locally docker-compose file can be used with the following configurations.

```
version: '3'
services:
  backend:
    image: backend
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: backend
    networks:
      - mynetwork
    environment:
      - DB_HOST=YOUR_DB_HOSTNAME
      - DB_NAME=YOUR_DB_NAME
      - DB_USER=YOUR_DB_USER_NAME
      - DB_PASSWORD=YOUR_DB_PASSWORD
    ports:
      - "5000:5000"
    depends_on:
      - postgres

  frontend:
    image: frontend
    build:
      context: ./frontend
      dockerfile: Dockerfile
    container_name: frontend
    networks:
      - mynetwork
    ports:
      - "80:80"

  postgres:
    image: postgres
    container_name: postgres
    networks:
      - mynetwork
    environment:
      POSTGRES_USER: YOUR_DB_USER_NAME
      POSTGRES_PASSWORD: YOUR_DB_PASSWORD
      POSTGRES_DB: YOUR_DB_HOSTNAME
    ports:
      - "5432:5432"

networks:
  mynetwork:
    driver: bridge
```

Run the docker compose file:
```sh
docker compose -f docker-compose.yml up -d
```

### Docker

#### Building Docker Images

1. Build the frontend Docker image:
```sh
docker build -t frontend ./frontend
```

2. Build the backend Docker image:
```sh
docker build -t backend ./backend
```

#### Running Docker Containers
Those steps are not necessary for local, it is added just to keep commands
1. Run the frontend container:
```sh
docker run -d -p 8080:80 frontend
```

2. Run the backend container:
```sh
docker run -d -p 5000:5000 backend
```

### Kubernetes Deployment

#### Prerequisites

1. Google Cloud CLI Setup
```sh
gcloud auth login
gcloud config set project [YOUR_PROJECT_ID]
```

2. GKE Cluster Creation
```sh
gcloud container clusters create [CLUSTER_NAME] --zone [ZONE] --num-nodes 3
```

3. Getting Authentication Credentials
```sh
gcloud container clusters get-credentials [CLUSTER_NAME] --zone [ZONE]
```

4. Configuring Docker to Authenticate with GCR
```sh
gcloud auth configure-docker
```

5. Tagging and Pushing Docker Image to GCR

Both frontend and backend
```sh
docker tag [IMAGE_NAME]:latest gcr.io/[YOUR_PROJECT_ID]/[IMAGE_NAME]:latest
docker push gcr.io/[YOUR_PROJECT_ID]/[IMAGE_NAME]:latest
```

6. Creating a Kubernetes Secret to Pull Images from GCR

Both frontend and backend
```sh
kubectl create namespace [NAMESPACE]
kubectl create secret docker-registry [your-gcr-json-key] --docker-server=gcr.io --docker-username=_json_key --docker-password="$(cat [PATH_TO_SERVICE_ACCOUNT_JSON])" --docker-email=[YOUR_EMAIL] --namespace=[NAMESPACE]
```

7. Creating a Kubernetes Secret to Store Database Credentials

```sh
kubectl create secret generic db-credentials --from-literal=DB_HOST=[YOUR_DB_HOSTNAME] --from-literal=DB_NAME=[YOUR_DB_NAME] --from-literal=DB_USER=[YOUR_DB_USER_NAME] --from-literal=DB_PASSWORD=[YOUR_DB_PASSWORD] -n [NAMESPACE_FOR_BACKEND]
```

#### Deploying to GKE

1. Deploy the backend:
```sh
kubectl apply -f deployment/backend-deployment.yaml
kubectl apply -f deployment/backend-service.yaml
kubectl get service backend-service --namespace <backend>
```

2. Deploy the frontend:
```sh
kubectl apply -f deployment/frontend-deployment.yaml
kubectl apply -f deployment/frontend-service.yaml
kubectl get service frontend-service --namespace <frontend>
```
