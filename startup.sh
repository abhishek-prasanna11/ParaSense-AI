#!/bin/bash
set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}=== ParaSense AI Local Deployment Script ===${NC}"
echo -e "This script will set up Minikube, build the Docker images, and deploy the Kubernetes manifests."
echo ""

# 1. Start Minikube
echo -e "${GREEN}[1/5] Checking Minikube status...${NC}"
if ! minikube status > /dev/null 2>&1; then
    echo "Starting Minikube (this may take a few minutes)..."
    minikube start --driver=docker
else
    echo "Minikube is already running."
fi

# 2. Enable Ingress
echo -e "${GREEN}[2/5] Enabling Minikube Ingress addon...${NC}"
minikube addons enable ingress > /dev/null

# 3. Update /etc/hosts for semantic-analysis.test
echo -e "${GREEN}[3/5] Checking /etc/hosts for semantic-analysis.test...${NC}"
if ! grep -q "semantic-analysis.test" /etc/hosts; then
    echo -e "${BLUE}We need to map semantic-analysis.test to 127.0.0.1.${NC}"
    echo -e "${RED}You may be prompted for your sudo password to update /etc/hosts.${NC}"
    echo "127.0.0.1 semantic-analysis.test" | sudo tee -a /etc/hosts > /dev/null
    echo "Host file updated."
else
    echo "Host file is already configured."
fi

# 4. Build Docker Images
echo -e "${GREEN}[4/5] Building Docker images inside Minikube...${NC}"
echo "Connecting to Minikube Docker daemon..."
eval $(minikube -p minikube docker-env)

echo "Building Backend (this auto-detects macOS vs Ubuntu architecture)..."
docker build -t dharaniprasads/semantic-backend:latest backend/

echo "Building Frontend..."
docker build -t dharaniprasads/semantic-frontend:latest frontend/

# 5. Apply Kubernetes Manifests
echo -e "${GREEN}[5/6] Deploying application to Kubernetes...${NC}"
kubectl apply -f k8s/

echo "Restarting pods to ensure latest images are used..."
kubectl rollout restart deployment semantic-backend
kubectl rollout restart deployment semantic-frontend

# 6. Deploy ELK Monitoring Stack
echo -e "${GREEN}[6/6] Deploying ELK Monitoring Stack...${NC}"
kubectl apply -f k8s/monitoring/

echo "Waiting for Elasticsearch to become ready (this may take a minute)..."
kubectl rollout status deployment/elasticsearch --timeout=180s || echo -e "${RED}Elasticsearch is still starting up. Check 'kubectl get pods' for status.${NC}"
kubectl rollout status deployment/logstash --timeout=120s || true
kubectl rollout status deployment/kibana --timeout=120s || true

echo ""
echo -e "${BLUE}==============================================${NC}"
echo -e "${GREEN}Deployment Complete!${NC}"
echo -e "${BLUE}==============================================${NC}"
echo "To access the web interface, you must start the Minikube tunnel."
echo ""
echo -e "Please run the following command in your terminal and KEEP IT OPEN:"
echo -e "${GREEN}minikube tunnel${NC}"
echo ""
echo -e "Then, open your web browser and navigate to:"
echo -e "  Application: ${GREEN}http://semantic-analysis.test${NC}"
echo -e "  Kibana:      ${GREEN}http://localhost:30601${NC}  (or via minikube service kibana)"
echo ""
