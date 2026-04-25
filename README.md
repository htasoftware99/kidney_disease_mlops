# Chronic Kidney Disease Prediction MLOps Project

An end-to-end MLOps pipeline for classifying Chronic Kidney Disease (CKD) using clinical data. This project demonstrates the integration of machine learning development with production-ready DevOps practices, including infrastructure as code, containerization, and automated CI/CD.

## 🏗️ System Architecture

<p align="center">
  <img src="structure.png" width="700"/>
</p>

## 🚀 Project Overview

The goal of this project is to provide a robust system for predicting the likelihood of chronic kidney disease based on patient clinical parameters. It covers the entire lifecycle from data ingestion to cloud deployment.

### Key Features
- **Data & Model Versioning**: Managed via **DVC (Data Version Control)** with Google Cloud Storage (GCS) as remote storage.
- **Experiment Tracking**: Integrated with **Comet ML** to log metrics, hyperparameters, and model performance.
- **Infrastructure as Code (IaC)**: **Terraform** used to provision Google Kubernetes Engine (GKE) and IAM roles on GCP.
- **CI/CD Pipeline**: Automated testing, building, security scanning with **Trivy**, and deployment using **Jenkins** and **GitHub Actions**.
- **Security Scanning**: Integrated **Trivy** to scan Docker images for vulnerabilities (High/Critical) before pushing to the container registry.
- **Deployment**: Scalable deployment using **Docker** and **Kubernetes (GKE)**.
- **Web Interface**: A **Flask**-based dashboard for real-time patient diagnosis.

---

## 🛠 Tech Stack

- **Language**: Python 3.10+
- **ML Frameworks**: Scikit-Learn, XGBoost, Pandas, Numpy
- **Web Framework**: Flask
- **DevOps/MLOps**:
    - **DVC**: Data and model versioning.
    - **Docker**: Containerization.
    - **Kubernetes (GKE)**: Orchestration.
    - **Terraform**: Cloud infrastructure provisioning.
    - **Jenkins**: Continuous integration.
    - **Trivy**: Vulnerability scanning for containers.
    - **Comet ML**: Experiment tracking.
- **Cloud Platform**: Google Cloud Platform (GCP)

---

## ⚙️ Installation & Setup

### 1. Clone the repository
```bash
git clone https://github.com/your-username/kidney_disease_mlops.git
cd kidney_disease_mlops
```

### 2. Create a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## 🧪 Usage

### Data & Training Pipeline
To run the end-to-end training pipeline (Data Processing -> Model Training):
```bash
python pipeline/training_pipeline.py
```

### Running the Web Application
To start the Flask app locally:
```bash
python app.py
```
Visit `http://localhost:5000` in your browser.

---

## ☁️ Cloud Infrastructure & Deployment

### Infrastructure Provisioning
The project uses Terraform to set up the GKE cluster.
```bash
cd infrastructure
terraform init
terraform plan
terraform apply
```

---

## 📊 Experiment Tracking
Model performance and metadata are logged to **Comet ML**. Ensure you have your `COMET_API_KEY`, `COMET_PROJECT_NAME`, `COMET_WORKSPACE` configured in your environment to track new runs.
