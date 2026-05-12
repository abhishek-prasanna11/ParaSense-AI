# ParaSense AI: Semantic Paraphrase Analysis Platform

ParaSense AI is a state-of-the-art semantic analysis platform that detects paraphrasing with high precision. This repository showcases a complete DevOps lifecycle, from automated CI/CD pipelines to container orchestration and production-grade monitoring.

---

## 🛠️ Project Architecture

The application is built using a microservices architecture designed for scalability and reliability.

- **Frontend**: A modern React application (Vite-based) providing a sleek, interactive user interface.
- **Backend**: A robust FastAPI (Python) service that handles semantic analysis and inference logic.
- **Ingress Gateway**: Uses the NGINX Ingress Controller to manage traffic routing:
  - `http://semantic-analysis.test/` → Serves the React Frontend.
  - `http://semantic-analysis.test/api/` → Routes to the FastAPI Backend.
- **Kubernetes (K8s)**: Manages the lifecycle of all containers, ensuring high availability and self-healing.

---

## 🚀 CI/CD Pipeline (Jenkins)

The project features a sophisticated Jenkins-based automation pipeline that ensures code quality and automated deployment.

### Pipeline Stages:
1.  **Clone Repo**: Pulls the latest code from the GitHub repository.
2.  **Health Check (Smoke Test)**:
    - Builds a temporary backend container.
    - Runs a `test50.py` suite (validating 50 core semantic scenarios).
    - **Threshold Gate**: The pipeline **automatically stops** if the pass rate is below 60%.
3.  **Build & Tag**: Once tests pass, production-ready Docker images are built for both Frontend and Backend.
4.  **Docker Push**: Securely pushes the images to DockerHub (`dharaniprasads/semantic-*`).
5.  **Kubernetes Deploy**: 
    - Applies all K8s manifests (`kubectl apply -f k8s/`).
    - Performs a `rollout restart` to ensure the cluster is running the absolute latest version of the images.
6.  **Monitoring Deploy**: Automatically spins up the ELK stack alongside the application.

---

## 📊 Observability & Monitoring (ELK Stack)

We have implemented a production-grade **ELK (Elasticsearch, Logstash, Kibana)** stack to monitor the cluster's health and application performance in real-time.

### 🔍 Monitoring Deep Dive
The system is designed to handle heterogeneous logs by isolating application-specific logic:

1.  **Structured Backend Logging**:
    - The FastAPI backend uses a custom JSON logger (`logging_config.py`) to output machine-readable logs.
    - Fields captured: `similarity_score`, `is_paraphrase`, `response_time_ms`, `endpoint`, and `client_ip`.

2.  **Smart Pipeline (Logstash)**:
    - **Isolation**: A conditional filter ensures Logstash only attempts to parse JSON for the `semantic-backend` container, preventing mapping conflicts with system/ingress logs.
    - **Field Promotion**: Key telemetry fields are promoted to the root level of the Elasticsearch document, enabling instant search and aggregation in Kibana.
    - **Stability**: Automatic template management is disabled to ensure compatibility across different Elasticsearch 8.x minor versions.

3.  **Visualization (Kibana)**:
    - **URL**: `http://localhost:5601` (via port-forward) or NodePort `30601`.
    - **Telemetry**: Monitor real-time inference trends, track 95th percentile latency, and analyze similarity score distributions.

### Troubleshooting & Maintenance
If mapping conflicts occur (e.g., `app.event` type mismatch):
1. Delete the current index: `curl -X DELETE "localhost:9200/semantic-logs-*"`
2. Restart Logstash: `kubectl delete pod -l app=logstash`
3. The pipeline will automatically recreate the index with the correct schema upon the next request.

---

## 🚦 How to Run Locally

### Prerequisites
- Docker & Minikube
- Kubectl

### Step-by-Step Setup
1.  **Run the Startup Script**:
    This script automates the Minikube setup, Ingress enablement, and initial deployment.
    ```bash
    ./startup.sh
    ```
2.  **Enable the Network Bridge**:
    Keep this running in a separate terminal to access the Ingress and Monitoring services:
    ```bash
    minikube tunnel
    ```
3.  **Configure Local DNS**:
    Ensure your `/etc/hosts` file maps the domain:
    ```text
    127.0.0.1 semantic-analysis.test
    ```
4.  **Access the Apps**:
    - **Application**: `http://semantic-analysis.test`
    - **Monitoring (Kibana)**: `http://localhost:30601`

---

## 📁 Key Directories
- `/backend`: FastAPI source code and ML inference logic.
- `/frontend`: React source code and styling.
- `/k8s`: Kubernetes deployment and service manifests.
- `/k8s/monitoring`: Configuration for Filebeat, Logstash, and Kibana.
- `/jenkins`: Jenkins integration files.
