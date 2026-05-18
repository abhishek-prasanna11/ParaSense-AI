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

Then simply open your browser and go to the application: **[http://semantic-analysis.test](http://semantic-analysis.test)**

**To view the Kibana Monitoring Dashboard (Logs):**
Open a new terminal and run:
```bash
kubectl port-forward svc/kibana 5601:5601
```
Then open your browser to: **[http://localhost:5601](http://localhost:5601)**
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

## 8. Production Logging Pipeline — Full Trace (stdout → ELK)

### 1. Your FastAPI App Runs Inside a Container

When Kubernetes starts your backend:

```plaintext
Pod
 └── Docker/Container Runtime
      └── FastAPI App
```

Your Python process is running INSIDE the container.

### 2. What Is stdout Here?

Inside Linux, every process automatically has:

| Stream | Purpose       |
| ------ | ------------- |
| stdin  | input         |
| stdout | normal output |
| stderr | errors        |

When Python does:

```python
print("hello")
```

or:

```python
logger.info(...)
```

it writes to:

```plaintext
stdout
```

### 3. Is a Terminal Actually Open?

Not like your laptop terminal.

There is NO visible terminal window.

Instead:

```plaintext
The container runtime creates stdout/stderr streams internally.
```

Think of it like invisible pipes.

Internally It Looks Like:

```plaintext
FastAPI Process
     │
 writes to stdout
     │
Container Runtime captures it
```

So when your logger writes:

```python
logger.info("request completed")
```

the JSON log goes into the container's stdout stream.

### 4. Docker Automatically Captures stdout

Docker automatically captures:

* stdout
* stderr

from containers.

That's why:

```bash
docker logs <container-id>
```

works.

Docker has already been collecting stdout the whole time.

Example — suppose container prints:

```json
{
  "message": "request_completed"
}
```

Docker stores it internally. You can see it via:

```bash
docker logs semantic-backend
```

### 5. In Kubernetes

Kubernetes also captures container stdout automatically.

You can view logs using:

```bash
kubectl logs <pod-name>
```

because Kubernetes reads the container stdout stream.

**Important Production Rule:** In containers, applications should log to stdout/stderr, NOT to local files. Why?

* containers are temporary
* files may disappear
* orchestration systems already collect stdout

### 6. Where Are Logs Physically Stored?

Depends on runtime. Usually:

```plaintext
/var/log/containers/
```

or:

```plaintext
/var/lib/docker/containers/
```

Kubernetes/container runtime stores stdout logs there.

### 7. How Does ELK Get Them?

This is where Filebeat, Fluentd, and Logstash come in.

**Typical Kubernetes Logging Architecture:**

```plaintext
FastAPI App
    ↓
stdout
    ↓
Container runtime
    ↓
Kubernetes node log files
    ↓
Filebeat/Fluent Bit DaemonSet
    ↓
Logstash
    ↓
Elasticsearch
    ↓
Kibana
```

### 8. What Is Filebeat Doing?

Filebeat runs on every Kubernetes node, usually as a DaemonSet. Meaning:

```plaintext
One Filebeat pod per node
```

Filebeat continuously watches log files:

```plaintext
/var/log/containers/*.log
```

It continuously tails logs like:

```bash
tail -f logfile
```

So Filebeat reads your JSON logs. Example container log:

```json
{
  "timestamp": "...",
  "message": "inference_completed"
}
```

Filebeat reads it and forwards it.

### 9. Why JSON Helps

Because Filebeat/Logstash can directly parse fields.

Instead of ugly text parsing:

```plaintext
INFO inference completed in 42ms
```

you already have structured data:

```json
{
  "inference_time_ms": 42
}
```

Much easier for Elasticsearch indexing.

### 10. Logstash (Optional Processing Layer)

Logstash may:

* enrich logs
* transform fields
* filter logs
* add metadata

Example:

```plaintext
Add Kubernetes pod name
Add namespace
Add node info
```

Then forwards to Elasticsearch.

### 11. Elasticsearch Stores Logs

Elasticsearch indexes logs as searchable JSON documents.

Now queries become possible:

```plaintext
Find all ERROR logs
```

or:

```plaintext
Average inference latency
```

### 12. Kibana Visualizes Everything

Kibana connects to Elasticsearch.

You can build:

* dashboards
* graphs
* alerts
* filters

Example:

```plaintext
Inference latency over time
```

### Full Real Example

**Your Backend:**

```python
logger.info(
    "inference_completed",
    extra={
        "inference_time_ms": 42,
        "similarity_score": 0.91
    }
)
```

**Printed to stdout:**

```json
{
  "message": "inference_completed",
  "inference_time_ms": 42,
  "similarity_score": 0.91
}
```

**Docker/K8s Captures It** — Stored internally in container log files.

**Filebeat Reads It:**

```plaintext
tail -f /var/log/containers/backend.log
```

**Filebeat Sends to Elasticsearch** — Over HTTP usually.

**Elasticsearch Stores Document:**

```json
{
  "service": "semantic-backend",
  "inference_time_ms": 42
}
```

**Kibana Dashboard Shows:**

```plaintext
Average inference latency: 38ms
```

### Simplest Mental Model

```plaintext
Your app prints logs to invisible console streams.
Docker/Kubernetes capture those streams automatically.
Filebeat reads them.
Elasticsearch stores them.
Kibana visualizes them.
```

That's the full production logging pipeline.

---

## 9. Horizontal Pod Autoscaler (HPA)

To handle variable traffic loads, we implemented a **Horizontal Pod Autoscaler** for the backend deployment. The HPA automatically adjusts the number of running pods based on real-time CPU utilization.

### How It Works

```plaintext
User traffic increases
    ↓
Backend pods CPU usage rises
    ↓
Metrics Server reports CPU > 50%
    ↓
HPA creates more pods (up to 4)
    ↓
Traffic is load-balanced across all pods
    ↓
Traffic decreases → HPA scales back down to 1 pod
```

### Configuration (`k8s/hpa.yaml`)

| Parameter | Value | Explanation |
|---|---|---|
| `minReplicas` | 1 | Minimum number of pods running at all times |
| `maxReplicas` | 4 | Maximum pods Kubernetes will scale up to |
| `averageUtilization` | 50% | The CPU threshold that triggers scaling |
| `scaleTargetRef` | `semantic-backend` | The deployment being autoscaled |

### Prerequisites

The HPA requires the **Metrics Server** to be running in the cluster. In Minikube, this is enabled with:

```bash
minikube addons enable metrics-server
```

### Useful Commands for Viva

```bash
# Check HPA status and current CPU usage
kubectl get hpa

# Watch HPA in real-time (updates every 2 seconds)
kubectl get hpa -w

# See detailed HPA events and conditions
kubectl describe hpa semantic-backend-hpa
```

### Why HPA Matters (Viva Talking Point)

> *"Our system uses a Horizontal Pod Autoscaler to ensure **elastic scalability**. During normal traffic, we run a single backend pod to save resources. When traffic spikes (e.g., multiple users submitting sentences simultaneously), the HPA detects the increased CPU load via the Metrics Server and automatically spins up additional pods — up to 4 replicas. When traffic drops, it scales back down. This ensures both **cost efficiency** and **high availability** without any manual intervention."*

---

## 10. Kubernetes Resource Inventory & Key Concepts

This section provides a complete inventory of every resource running in the cluster and explains the Kubernetes concepts behind them.

### Application Endpoints & Routes

Our application cluster exposes traffic externally through the Ingress controller and internally for specific services. Here are the available endpoints you can interact with:

| Service | External Route / URL | Internal Path | Purpose |
|---|---|---|---|
| **Frontend UI** | `http://semantic-analysis.test/` | `/` | The main React user interface served by Nginx. |
| **Backend Health** | `http://semantic-analysis.test/api/` | `GET /` | Returns `{"status": "Backend running"}`. Used by Kubernetes Liveness and Readiness probes to verify the pod is alive. |
| **Backend API** | `http://semantic-analysis.test/api/analyze` | `POST /analyze` | **Core ML Endpoint** — Accepts two sentences (`text1`, `text2`), runs them through the Sentence Transformer model, and returns a similarity score and paraphrase boolean. |
| **Backend Docs** | `http://semantic-analysis.test/api/docs` | `GET /docs` | Auto-generated interactive Swagger UI API documentation provided by FastAPI. |
| **Kibana UI** | `http://<minikube-ip>:30601` | - | The ELK stack visual dashboard (exposed via NodePort) for monitoring logs. |

### Pods (6 Total)

A **Pod** is the smallest deployable unit in Kubernetes. It is a wrapper around one or more containers. In our project, each pod runs exactly one container.

| Pod | Container Inside | What It Does |
|---|---|---|
| `semantic-backend-...` | Python FastAPI + ML Model | Serves the `/analyze` API. Loads the Sentence Transformer model into memory on startup. |
| `semantic-frontend-...` | Nginx serving React static files | Serves the web UI to the user's browser. |
| `elasticsearch-...` | Elasticsearch 7.x | Stores all processed logs as searchable JSON documents. |
| `logstash-...` | Logstash 7.x | Receives raw logs from Filebeat, parses JSON fields (similarity scores, latency), and forwards clean data to Elasticsearch. |
| `kibana-...` | Kibana 7.x | Provides the visual dashboard UI that queries Elasticsearch. |
| `filebeat-...` | Filebeat 7.x | Runs as a DaemonSet. Tails log files from all containers on the node and forwards them to Logstash. |

### Containers (6 Total)

A **Container** is a lightweight, isolated process running inside a pod. Each of our 6 pods has exactly 1 container, so we have **6 containers** in total. The containers are built from Docker images:

| Container | Docker Image | Base |
|---|---|---|
| semantic-backend | `abhishekprasanna1109/semantic-backend:latest` | `python:3.10-slim` |
| semantic-frontend | `abhishekprasanna1109/semantic-frontend:latest` | `nginx:alpine` (multi-stage build) |
| elasticsearch | `docker.elastic.co/elasticsearch/elasticsearch` | Official Elastic image |
| logstash | `docker.elastic.co/logstash/logstash` | Official Elastic image |
| kibana | `docker.elastic.co/kibana/kibana` | Official Elastic image |
| filebeat | `docker.elastic.co/beats/filebeat` | Official Elastic image |

### Services (5 Application + 1 System)

A **Service** provides a stable, unchanging IP address for a group of pods. Pods can die and restart with new IPs, but the Service IP never changes. Other pods use the Service name as a DNS hostname to communicate.

| Service Name | Type | Port(s) | Connects To |
|---|---|---|---|
| `semantic-backend` | ClusterIP | 8000 | Backend pod(s) — the FastAPI ML server |
| `semantic-frontend` | ClusterIP | 80 | Frontend pod(s) — the Nginx web server |
| `elasticsearch` | ClusterIP | 9200, 9300 | Elasticsearch pod — log storage database |
| `logstash` | ClusterIP | 5044, 9600 | Logstash pod — log processing pipeline |
| `kibana` | NodePort | 5601 (→30601) | Kibana pod — monitoring dashboard |
| `kubernetes` | ClusterIP | 443 | System service — the K8s API server itself |

**ClusterIP** = Only accessible from inside the cluster (other pods can reach it).
**NodePort** = Accessible from outside the cluster on a specific port (e.g., Kibana on port 30601).

### Ingress Resources (2 Total)

An **Ingress** is the "Smart Front Door" of the cluster. It reads the incoming HTTP URL and routes it to the correct Service. We have 2 Ingress resources, both listening on `semantic-analysis.test`:

| Ingress Name | URL Path | Routes To |
|---|---|---|
| `semantic-frontend-ingress` | `/` (everything) | `semantic-frontend` Service (port 80) |
| `semantic-api-ingress` | `/api/*` | `semantic-backend` Service (port 8000) |

The API ingress uses **regex rewriting** (`nginx.ingress.kubernetes.io/rewrite-target`) so that `/api/analyze` is rewritten to `/analyze` before hitting the backend.

### Deployments (5 Total)

A **Deployment** tells Kubernetes: "I want X replicas of this pod running at all times." If a pod crashes, the Deployment automatically creates a new one.

| Deployment | Replicas | Managed Pod |
|---|---|---|
| `semantic-backend` | 1 (autoscaled by HPA up to 4) | Backend ML server |
| `semantic-frontend` | 1 | Frontend web UI |
| `elasticsearch` | 1 | Log storage |
| `logstash` | 1 | Log processor |
| `kibana` | 1 | Dashboard UI |

### DaemonSet (1 Total) — What Is a DaemonSet?

A **DaemonSet** is different from a Deployment. Instead of saying "run X copies," a DaemonSet says: **"Run exactly ONE copy of this pod on EVERY node in the cluster."**

```plaintext
Deployment:  "I want 3 pods running somewhere in the cluster"
DaemonSet:   "I want 1 pod running on EVERY node in the cluster"
```

**Why Filebeat uses a DaemonSet:**
Filebeat needs to read log files from the node's filesystem (`/var/log/containers/`). If Filebeat only ran on Node A, it would miss logs from pods running on Node B. By using a DaemonSet, we guarantee that every single node has a Filebeat agent collecting logs.

| DaemonSet | Pod Per Node | Purpose |
|---|---|---|
| `filebeat` | 1 per node | Tails container log files and forwards them to Logstash |

In our Minikube setup (single node), this means 1 Filebeat pod. In a production cluster with 10 nodes, there would automatically be 10 Filebeat pods.

### ConfigMap (1 Total)

A **ConfigMap** stores configuration data as key-value pairs. It allows you to change application settings without rebuilding Docker images.

| ConfigMap | Keys | Used By |
|---|---|---|
| `semantic-config` | `VITE_API_URL`, `MODEL_NAME` | Backend and Frontend pods via `envFrom` |

### Complete Resource Summary

| Resource Type | Count | Names |
|---|---|---|
| Pods | 6 | backend, frontend, elasticsearch, logstash, kibana, filebeat |
| Containers | 6 | One per pod |
| Services | 5+1 | backend, frontend, elasticsearch, logstash, kibana + kubernetes (system) |
| Ingress | 2 | frontend-ingress (`/`), api-ingress (`/api/*`) |
| Deployments | 5 | backend, frontend, elasticsearch, logstash, kibana |
| DaemonSets | 1 | filebeat |
| ConfigMaps | 1 | semantic-config |
| HPA | 1 | semantic-backend-hpa |
| API Endpoints | 2 | `GET /` (health), `POST /analyze` (ML inference) |

### Networking Concepts: NodePort vs Port-Forward

During development and monitoring, we use two different ways to access our services. Here is how the network traffic flows for each:

**NodePort** (Used for Kibana in our setup)
```plaintext
Browser
  ↓
Real network connection
  ↓
Minikube IP:NodePort
  ↓
Service
  ↓
Pod
```

**Port-Forward** (Used for direct debugging)
```plaintext
Browser
  ↓
localhost
  ↓
kubectl tunnel
  ↓
Kubernetes API
  ↓
Pod
```
### End-to-End User Request Flow (Browser to Backend)

Here is the exact step-by-step chronological flow of what happens from the moment a user opens their browser to the moment they get a result.

#### Step 1: The User Opens the Website
1.  **The Action:** The user types `http://semantic-analysis.test` in their browser and hits Enter.
2.  **The Ingress:** The request hits the Kubernetes Ingress. The Ingress looks at the path, which is just `/`.
3.  **The Route:** According to `ingress.yaml`, anything on `/` goes to the `semantic-frontend` service.
4.  **The Result:** The Nginx container inside the frontend pod sends the React HTML/JavaScript files back to the user's browser. The beautiful UI is now displayed on their screen.

#### Step 2: The User Interacts with the Page
1.  **The Action:** The user types two sentences into the text boxes.
2.  **The Result:** The React code (`App.tsx`) saves these sentences into its internal memory (React state). No network request is made yet.

#### Step 3: The User Clicks "Analyze"
1.  **The Action:** The user clicks the Analyze button.
2.  **The Frontend Code:** React triggers an `axios.post` command in `Result.tsx`.
3.  **The Network Request:** The browser automatically constructs a new HTTP request and sends it to: `http://semantic-analysis.test/api/analyze`.

#### Step 4: The Ingress Intercepts the API Call
1.  **The Ingress:** This new request hits the Kubernetes Ingress again. 
2.  **The Route:** The Ingress looks at the path: `/api/analyze`. 
3.  **The Match:** It sees that this matches the specific rule in `ingress.yaml`: "Anything starting with `/api` goes to the backend."
4.  **The Rewrite (Crucial Step):** Before sending it to the backend, the Ingress looks at the annotation (`rewrite-target: /$2`). It magically strips the `/api` part off the URL.

#### Step 5: The Backend Processes the Request
1.  **The Hand-off:** The Ingress forwards the modified request (`/analyze`) to the `semantic-backend` service.
2.  **The Python Code:** Inside `main.py`, FastAPI sees a request for `/analyze` and matches it to the `@app.post("/analyze")` function.
3.  **The ML Engine:** The Python code runs the sentences through the Sentence Transformer model, generates a similarity score, and sends a JSON response (e.g., `{"similarity": 0.85, "paraphrase": true}`) back through the Kubernetes network, out through the Ingress, and back to the user's browser.
4.  **The Final Display:** React receives the JSON response and updates the screen to show the 85% score.

**Summary of the Flow:**
> **Browser → Ingress (`/`) → Frontend Service → Browser → Browser clicks Analyze → Browser sends request → Ingress (`/api/analyze`) → Rewrite to `/analyze` → Backend Service → Python ML Model → JSON Response back to Browser.**

---

## 11. Kubernetes Manifests Deep Dive

The `k8s/` directory contains all the blueprints used to build our cluster infrastructure. Here is a detailed explanation of each file and its role in the architecture.

### 1. `frontend-deployment.yaml`
This creates the **Frontend Pods**.
*   **The Container:** It pulls `abhishekprasanna1109/semantic-frontend:latest` from DockerHub. Because we used a Multi-Stage Docker build, this container does NOT contain Node.js; it only contains an **Nginx** web server and our compiled static React files (HTML/JS/CSS).
*   **Port:** It opens port `80` (the default port for Nginx).
*   **Probes:** We defined `livenessProbe` and `readinessProbe` to ping `/` on port 80. Kubernetes uses this to verify the Nginx server is actively serving the React app before it routes user traffic to it.
*   **Resources:** It requests minimal resources (`128Mi` RAM) because serving static HTML is very lightweight.

### 2. `frontend-service.yaml`
This creates a stable internal IP address for the Frontend Pods.
*   **The Glue:** It uses a `selector` looking for `app: semantic-frontend`. It finds our Nginx pod and creates a stable connection to it.
*   **Routing:** It listens on port `80` and forwards traffic to `targetPort: 80` (the Nginx container port). The Ingress uses this Service name to send user traffic to the frontend.

### 3. `backend-deployment.yaml`
This creates the **Backend ML Pods** (the "heavy lifters").
*   **The Container:** It pulls `abhishekprasanna1109/semantic-backend:latest`. This container runs a full Python 3.10 environment with **FastAPI**. 
*   **The ML Model:** When FastAPI starts, it loads the heavy `all-mpnet-base-v2` Sentence Transformer model directly into the container's RAM.
*   **Resources:** Because ML models are heavy, this deployment specifically requests up to `3Gi` of RAM and `1000m` (1 full CPU core) to prevent Out-Of-Memory (OOM) crashes.
*   **Port:** It opens port `8000`, the default port we configured for FastAPI/Uvicorn.

### 4. `backend-service.yaml`
This creates a stable internal IP address for the Backend ML Pods.
*   **The Glue:** It uses a `selector` looking for `app: semantic-backend`. 
*   **Routing:** It listens on port `8000` and forwards traffic to the FastAPI pod on `8000`. The Ingress (and the HPA) use this service to communicate with the ML engine.

### 5. `ingress.yaml`
This is the "Smart Router" or API Gateway. It exposes our internal services to the outside world.
*   **Rule 1 (Frontend):** It says any traffic hitting `semantic-analysis.test` on the root path `/` should be routed to the `semantic-frontend` Service on port 80.
*   **Rule 2 (Backend):** It says any traffic starting with `/api` should be routed to the `semantic-backend` Service on port 8000.
*   **The Rewrite Magic:** We use the annotation `nginx.ingress.kubernetes.io/rewrite-target: /$2`. This automatically strips the `/api` prefix from the URL before it hits the backend. This means our Python code only has to listen for `/analyze`, not `/api/analyze`.

### 6. `configmap.yaml`
This stores configuration variables centrally.
*   It defines environment variables like `MODEL_NAME` (`all-mpnet-base-v2`). 
*   Both the frontend and backend deployments use `envFrom: configMapRef` to pull these variables inside the containers at runtime. This allows us to change settings without rebuilding our Docker images.

### 7. `hpa.yaml`
The Horizontal Pod Autoscaler.
*   It constantly monitors the CPU usage of the `semantic-backend` Deployment (via the Metrics Server).
*   If average CPU usage crosses **50%** (e.g., during a spike in ML inference requests), it automatically spins up new backend pods (up to a max of 4).
*   When traffic dies down, it terminates the extra pods, scaling back down to a minimum of 1 to save resources.

---

## 12. Future Improvement Plan
As outlined in `IMPROVEMENT_PLAN.md`, the next phase involves migrating to a Multi-Task Training approach utilizing Knowledge Distillation to achieve >85% universal accuracy across highly diverse domains.

---

## 💬 13. Viva Voce Q&A (Infrastructure Design Decisions)

### Q1: Why did we use Jenkins Credentials Manager instead of Ansible Vault?
* **Pipeline-First Orchestration**: The CI/CD process is managed and driven by Jenkins. Jenkins must authenticateto GitHub, build and push to Docker Hub, and securely authenticate with the Kubernetes cluster *before* Ansible is triggered. Managing credentials centrally in Jenkins makes architectural sense.
* **Console Log Masking**: Jenkins Credentials Manager has a built-in protection mechanism that automatically masks secret strings (replacing them with `****`) in build console logs. Ansible Vault does not automatically mask outputted secrets.
* **Risk of Disk Exposure**: Ansible Vault requires storing a decryption password/file on the Jenkins runner's disk or passing it via command line parameters, which increases the security vulnerability surface. Jenkins Credentials Manager injects secrets directly into environment memory only for the duration of the execution block (`withCredentials`) without writing decrypted keys to disk.

### Q2: Why did we not use Ansible Roles?
* **Avoidance of Over-Engineering**: Ansible Roles are designed for complex, modular, and highly reusable configuration setups across large environments (e.g., maintaining full web, database, and caching servers across multi-region VMs). 
* **Simple Automations**: Our Ansible playbooks perform extremely targeted, lightweight deployment and provisioning tasks. Using Roles would require generating a complex directory hierarchy (`tasks/`, `handlers/`, `templates/`, `vars/`, `defaults/`, `meta/`) for basic commands, introducing unnecessary cognitive overhead and cluttering the workspace.
* **Declarative Kubernetes Paradigm**: Since Kubernetes natively handles the heavy lifting of state reconciliation, service mesh, scaling, and container configuration declaratively via YAML manifests, Ansible's role is relegated strictly to automation orchestration. A single flat playbook is simpler, cleaner, and highly maintainable for this architecture.

### Q3: Why is `kubectl rollout restart` necessary after `kubectl apply` in our pipeline?
* **The `:latest` Image Tag Rollout Problem**: `kubectl apply -f k8s/` updates Kubernetes resources only if the Deployment specification changes. Since your Deployment always uses the same image tag (`semantic-backend:latest`), pushing a new image to Docker Hub does not change the YAML. Kubernetes therefore sees no change and keeps the existing pod running with the old image. `kubectl rollout restart deployment semantic-backend` forces Kubernetes to recreate the pod even though the YAML is unchanged. The new pod then starts again and pulls the updated latest image.
