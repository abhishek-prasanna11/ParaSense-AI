# Project Walkthrough: Paraphase Semantic Analysis & CI/CD Deployment

## 🚀 Quick Start (Cross-Platform Deployment)
To easily run this project locally on either **macOS** or **Ubuntu**, simply run the automated deployment script:

```bash
./startup.sh
```

**What this script does automatically:**
1. Starts Minikube and enables the Ingress addon.
2. Prompts for `sudo` to securely add `semantic-analysis.test` to your `/etc/hosts` file (bypassing macOS `.local` DNS issues).
3. Connects to the internal Minikube Docker daemon.
4. Dynamically builds the Docker images (it automatically detects if you are on macOS ARM64 or Ubuntu AMD64 and installs the correct libraries to keep images small and prevent crashes).
5. Deploys the Kubernetes `.yaml` manifests and restarts the pods.

**After the script finishes, you must start the network tunnel:**
```bash
minikube tunnel
```
*(Leave that terminal window open in the background).*

Then simply open your browser and go to: **[http://semantic-analysis.test](http://semantic-analysis.test)**

---

## 1. Project Overview

The **Paraphrase Semantic Analysis** project is a comprehensive Machine Learning application designed to detect paraphrases and assess semantic similarity between text inputs. It leverages a fine-tuned Sentence Transformer (MPNet) optimized for complex language, including negation traps and adversarial word swaps.

### Core Features
- **High-Accuracy Semantic Detection:** Fine-tuned on datasets like QQP, MRPC, STS-B, PAWS, and MNLI to handle conversational, formal, and adversarial sentence pairs.
- **Microservices Architecture:** 
  - **Backend:** A Python/FastAPI service hosting the model inference.
  - **Frontend:** A web interface for users to input sentences and receive similarity scores.
- **Hardware Optimization:** Includes support for Apple Silicon (MPS), CUDA, and standard CPU environments.

---

## 2. Infrastructure & Deployment (What We Did)

To make this project robust and scalable for production environments, we established a complete containerized infrastructure:

### Docker Integration
The project natively supports Docker Compose (`docker-compose.yml`), allowing you to spin up the backend and frontend simultaneously connected via an isolated app network.

### Kubernetes (K8s) Integration
We integrated a full Kubernetes deployment strategy to allow for horizontal scaling and self-healing. All manifests are located in the `k8s/` directory:

1.  **Persistent Volume Claim (`backend-pvc.yaml`):** Secures 1Gi of persistent storage for the fine-tuned machine learning models, ensuring they aren't lost if a pod restarts.
2.  **ConfigMaps (`configmap.yaml`):** Centralizes application configuration (like `VITE_API_URL` and `MODEL_NAME`), allowing for easy environment management without rebuilding images.
3.  **Backend Deployment & Service:**
    *   **Probes:** Includes **Liveness** and **Readiness** probes. Readiness ensures the pod doesn't receive traffic until the ML model is fully loaded; Liveness automatically restarts the container if the API hangs.
    *   **Resource Management:** Implements **CPU/Memory Limits and Requests** (e.g., 2Gi Memory limit) to ensure backend stability and prevent resource starvation.
    *   **Service:** Exposed internally via a `ClusterIP` on port 8000.
4.  **Frontend Deployment & Service:** Includes health checks and resource limits, exposed internally via `ClusterIP`.
5.  **Advanced Ingress (`ingress.yaml`):** Provides a production-grade "Front Door." It uses **Hostname Routing** (`semantic-analysis.local`) to direct `/api` traffic to the backend and `/` traffic to the frontend UI.
6.  **Automated CI/CD:** The updated **`JenkinsFile`** now handles the full deployment lifecycle, automatically applying these manifests to the cluster and performing a `rollout restart` to update running pods with new images.

---

## 3. Getting Started

### Local Setup (Development)
If you want to run the project locally for development or testing:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/dharani070707/CICD_Paraphase_Semantic_Analysis.git
   cd CICD_Paraphase_Semantic_Analysis
   ```
2. **Pull Large Model Files:**
   You must have Git LFS installed to pull the model weights.
   ```bash
   git lfs install
   git lfs pull
   ```
3. **Run via Docker Compose:**
   ```bash
   docker-compose up --build
   ```

### Kubernetes Deployment (Production)
To deploy the application to a Kubernetes cluster (e.g., Minikube, EKS, GKE):

1. **Apply the manifests:**
   ```bash
   kubectl apply -f k8s/
   ```
2. **Verify Pods & Services:**
   ```bash
   kubectl get all -l 'app in (semantic-backend, semantic-frontend)'
   ```
3. **Access the Application:**
   The frontend will be accessible on your Node's IP address at port `30000`. If using Minikube, run:
   ```bash
   minikube service semantic-frontend
   ```

---

## 4. CI/CD & Automation Pipeline

This project employs a robust, fully automated Continuous Integration and Continuous Deployment (CI/CD) pipeline. It ensures that every code change is rigorously tested, containerized, and deployed without manual intervention.

### The Jenkins Pipeline (`Jenkinsfile`)
The Jenkins pipeline is the orchestrator of our CI/CD process. It is written using Jenkins Declarative Pipeline syntax and executes the following stages sequentially:

1.  **Clone Repo:** Fetches the latest source code from the `main` branch of the GitHub repository.
2.  **Start Backend for Testing:** Builds a temporary Docker image (`temp-backend`) for the Python backend and starts it. It includes a health-check loop that waits to ensure the ML model successfully loads into memory before proceeding.
3.  **Run test50 (Automated QA):** Creates an isolated Python virtual environment, installs lightweight dependencies (`requests`), and runs the `test50.py` paraphrase test suite against the live temporary backend. This suite contains 50 rigorous edge-case tests (including negation traps and adversarial swaps).
4.  **Check Pass Percentage:** Parses the test results. A strict quality gate is enforced: the pipeline will instantly fail and halt if the model's accuracy drops below the 60% threshold.
5.  **Build Docker Images:** Once tests pass, it tags the temporary backend image for production and builds the React frontend Docker image.
6.  **Push to DockerHub:** Securely logs into DockerHub using injected credentials and pushes the newly built images (`semantic-backend` and `semantic-frontend`) to the container registry.
7.  **Deploy to Kubernetes:** Applies the Kubernetes manifests (`k8s/`) to the cluster. It then triggers a `kubectl rollout restart` to ensure the pods pull the fresh images without downtime.
8.  **Deploy ELK Monitoring:** Applies the monitoring manifests (`k8s/monitoring/`) to ensure Elasticsearch, Logstash, Filebeat, and Kibana are running to track the newly deployed application.

### Server Configuration Management (`Ansible/`)
While Kubernetes handles our container orchestration, **Ansible** is utilized for foundational server configuration management (often used for staging or alternative environments). The `playbook.yml` performs the following infrastructure-as-code tasks:

1.  **Dependency Verification:** Automatically checks if Docker and the Docker Compose plugin are installed on the target host server.
2.  **Automated Installation:** If Docker is missing, it uses the `apt` package manager to install it and ensures the Docker daemon is enabled and running on boot.
3.  **Clean Slate Deployment:** Navigates to the application directory and runs `docker compose down` to gracefully stop and remove old containers.
4.  **Application Bootstrapping:** Executes `docker compose up -d --build` to safely build and spin up the complete application stack (frontend and backend) via Docker Compose.
5.  **Health Verification:** Implements a polling mechanism that repeatedly pings the backend's `/docs` endpoint. It waits until the API returns a success status, ensuring the application is fully online before Ansible reports a successful deployment.

**Note on Infrastructure:** For this local demonstration, we used Minikube because it's a self-contained environment. However, we have included an Ansible Playbook to show that our project is Production-Ready. If we wanted to move this app to a standard Ubuntu server in the cloud, we would use Ansible to automate the server setup and Docker configuration.

## 5. Viva Voce / Demonstration Guide

During a live demonstration or viva, use the following structured flow to showcase the system:

### 1. Show the Running System
Run this command to show all your running containers (pods):
**`kubectl get pods`**

*Explain the output in two categories:*
*   **The Application Stack:**
    *   **`semantic-frontend-...`**: The React/Web UI where the user interacts.
    *   **`semantic-backend-...`**: The core API engine hosting the Machine Learning model. Multiple replicas demonstrate high availability.
*   **The Monitoring Stack (ELK Stack):**
    *   **`filebeat-...`**: A lightweight agent scraping raw logs from the backend/frontend.
    *   **`logstash-...`**: The data processor receiving logs, parsing out JSON telemetry data (similarity scores, response times), and sending it to the database.
    *   **`elasticsearch-...`**: The database storing all processed logs and metrics.
    *   **`kibana-...`**: The visual dashboard to monitor logs and model health.

### 2. Show the Network Configuration
Run these commands to show how the application is exposed:
**`kubectl get services`** and **`kubectl get ingress`**

*Explanation:* "Services route traffic internally to the correct pods. To expose this, we use a Kubernetes **Ingress Controller** acting as a smart router, directing HTTP requests to the frontend or API backend based on URL paths."

### 3. Start the Application for the Demo
Run in a separate terminal:
**`minikube tunnel`**

*Explanation:* "This tunnel bridges the Kubernetes network to the local machine's network, simulating a real cloud load balancer."

### 4. Show the ELK Dashboard
Run this command to port-forward Kibana:
**`kubectl port-forward svc/kibana 5601:5601`**

*Explanation:* Open `http://localhost:5601` in the browser. "Every time a request is made to the backend, telemetry data (prediction scores, latency) flows through Logstash and is visualized here in real-time, ensuring production observability."

---

## 6. Networking Topology & Data Flow

If asked to explain the networking architecture during the viva, refer to these two decoupled data paths:

### 1. The Application Networking Flow (User Path)
This is how a user’s request travels from their browser to the ML model and back.
1.  **The User:** Types `http://semantic-analysis.test` in the browser.
2.  **Minikube Tunnel:** Routes traffic for `semantic-analysis.test` into the isolated Minikube network.
3.  **The Ingress Controller (Nginx):** The "Front Door" reads the URL path.
    *   Requests for the main website (`/`) are forwarded to the **`semantic-frontend` Service**.
    *   API calls (`/api/analyze`) are forwarded to the **`semantic-backend` Service**.
4.  **The Services (Load Balancing):** 
    *   The **`semantic-frontend` Service** connects the user to the frontend Pods (Nginx/React).
    *   The **`semantic-backend` Service** connects the API to the backend Pods (FastAPI/Python ML model).

### 2. The Monitoring Networking Flow (Telemetry Path)
This is how application logs are collected and visualized without slowing down the user experience.
1.  **Filebeat (DaemonSet):** Runs as a background agent on the node, constantly reading the raw console output of the frontend and backend pods.
2.  **Logstash Service:** Filebeat sends those raw logs over the internal network to Logstash.
3.  **Logstash Pod:** Receives the logs, parses the JSON (extracting the semantic similarity scores and latency), and sends the clean data to Elasticsearch.
4.  **Elasticsearch Service & Pod:** Stores the processed telemetry data permanently.
5.  **Kibana Service & Pod:** Queries Elasticsearch to fetch the logs and renders the visual dashboard when accessed via port-forwarding.

---

## 7. Future Improvement Plan
As outlined in `IMPROVEMENT_PLAN.md`, the next phase involves migrating to a Multi-Task Training approach utilizing Knowledge Distillation to achieve >85% universal accuracy across highly diverse domains.
