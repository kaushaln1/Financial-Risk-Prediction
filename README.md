# Production-Grade MLOps Platform for Financial Risk Prediction

This project demonstrates an end-to-end MLOps platform built with Kubernetes, Feast, MLflow, and FastAPI. It automates the entire lifecycle of a machine learning model, from data ingestion to production inference.

![Architecture Diagram](docs/architecture_diagram.png) 
*(Note: Generate the diagram from `docs/architecture_diagram.mmd`)*

## 🚀 Features

*   **Unified Feature Store**: Consistent feature serving for training and inference using **Feast** (Redis + Parquet).
*   **Experiment Tracking**: Full lineage of code, data, and models using **MLflow**.
*   **Model Registry**: Centralized versioning and lifecycle management.
*   **Scalable Inference**: High-performance **FastAPI** service running on Kubernetes.
*   **Infrastructure as Code**: Fully declarative K8s manifests managed with **Kustomize**.
*   **Self-Healing**: Resilient architecture capable of recovering from pod failures (e.g., database or tracking server crashes).

## 🛠️ Tech Stack

*   **Orchestration**: Kubernetes (Minikube / EKS)
*   **Feature Store**: Feast (Redis Online / Parquet Offline)
*   **Tracking & Registry**: MLflow
*   **Storage**: Minio (S3 Compatible) & Postgres
*   **Model Serving**: FastAPI + Docker
*   **Language**: Python 3.10

## 📂 Project Structure

```bash
mlops-platform/
├── airflow/                # Orchestration DAGs (Future integration)
├── docs/                   # Documentation & Diagrams
├── features/               # Feast feature definitions & data generation
├── inference/              # FastAPI Inference Service (Microservice)
├── infra/                  # Infrastructure configurations
│   ├── k8s/                # Kubernetes Manifests (Base + Overlays)
│   └── terraform/          # Cloud Infrastructure (AWS)
├── monitoring/             # Drift detection & Prometheus configs
├── training/               # Model training scripts
└── requirements.txt        # Python dependencies
```

## ⚡ Quick Start (Local Minikube)

### Prerequisites
*   Docker & Minikube
*   Python 3.10+
*   `kubectl` & `feast` CLI

### 1. Start Infrastructure
```bash
minikube start
kubectl apply -k infra/k8s/overlays/minikube
```

### 2. Setup Feature Store
```bash
cd features
python generate_data.py
feast apply
feast materialize-incremental $(date +%Y-%m-%d)
```

### 3. Train Model
```bash
# Port-forward services first
kubectl port-forward -n mlops svc/mlflow-service 5000:5000 &
kubectl port-forward -n mlops svc/minio-service 9000:9000 &

# Create S3 Bucket & Run Training
export MLFLOW_TRACKING_URI="http://localhost:5000"
export MLFLOW_S3_ENDPOINT_URL="http://localhost:9000"
export AWS_ACCESS_KEY_ID="minioadmin"
export AWS_SECRET_ACCESS_KEY="minioadmin"

python infra/create_bucket.py
python training/train.py --feature_repo features
```

### 4. Deploy Inference Service
```bash
# Build image locally in Minikube
minikube docker-env | Invoke-Expression
docker build -t inference-service:latest inference

# Deploy
kubectl apply -k infra/k8s/base/inference
```

### 5. Test Prediction
```bash
kubectl port-forward -n mlops svc/inference-service 8000:8000 &

curl -X POST "http://localhost:8000/api/v1/predict" \
     -H "Content-Type: application/json" \
     -d '{"user_id": "1001"}'
```

## 📊 Monitoring

*   **MLflow UI**: `http://localhost:5000` (View experiments & artifacts)
*   **Minio Console**: `http://localhost:9001` (User/Pass: `minioadmin`)

## 📝 License
MIT
