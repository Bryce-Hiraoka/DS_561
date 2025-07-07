📁 Project Summaries
📄 File 1 – Cloud Console, gcloud, and gsutil Operations
This project explores fundamental GCP resource management operations:

Creating and managing GCS buckets and directories

Managing VM instances (create, pause, delete)

Creating/deleting service accounts and assigning storage access

Full cleanup of cloud resources

Tools: GCP Console, gcloud, gsutil

📄 File 2 – Link Graph Analysis and PageRank
Generates a dataset of 10,000 files representing a web graph with links:

Uploads the graph files to a GCS bucket

Analyzes link statistics: avg, median, min, max, quintiles

Constructs a directed graph and computes PageRank using an iterative algorithm

Reports cloud resource usage and costs

Tools: Python, GCS, GCP billing

📄 File 3 – Cloud Function Web Service
Implements a cloud function that serves GCS files over HTTP:

Handles GET requests (200 OK) and logs invalid requests (404/501) to Cloud Logging

Demonstrates app behavior with browser, curl, and client script

Second app tracks banned-country requests and logs permission-denied (400) errors locally

Tools: Cloud Functions, Cloud Logging, GCS, Python, Web client

📄 File 4 – VM-Based HTTP Server
Builds a full HTTP server hosted on a GCP VM:

Serves GCS files over HTTP

Automatically starts on VM boot using a static IP

Handles and logs various HTTP methods (GET, 404, 501)

Supports multi-VM architecture with stress testing and error rate analysis

Includes permission checks using the second app

Tools: Compute Engine, Python HTTP server, curl, multi-client load testing

📄 File 5 – Request Logging to Cloud SQL
Enhances the VM web server to:

Store structured request data in Cloud SQL (normalized to 2NF)

Separately logs failed requests

Supports concurrent clients issuing 50,000 requests each

Performs analytics on request metadata (success rates, demographics, top countries)

Tools: Cloud SQL, Python (MySQL/PostgreSQL client), VM instance, Data normalization

📄 File 6 – Machine Learning on Request Data
Trains and evaluates two ML models using Cloud SQL data:

Predicts country from client IP (99%+ accuracy expected)

Predicts income from user metadata (gender, age, country, etc.)

Runs on a separate GCP VM

Tools: scikit-learn / TensorFlow, SQL, Python, GCP VM

📄 File 7 – Apache Beam + Dataflow Pipeline
Performs large-scale data processing on the link graph:

Computes top 5 files with the most incoming and outgoing links

Runs both locally and via Google Cloud Dataflow

Compares performance and runtime costs

Tools: Apache Beam, Dataflow, Python, GCS

📄 File 8 – Load Balanced Multi-Zone Deployment
Deploys two web server VMs in different zones behind a Load Balancer:

Implements zone-based response headers

Dynamically detects VM health and reroutes traffic

Measures failover and recovery latency

Verifies client response behavior during failover events

Tools: GCP Load Balancer, Health Checks, Compute Engine, curl, browser, client

📄 File 9 – Kubernetes (GKE) Containerized Server
Ports the HTTP server to a Docker container running on GKE:

Handles and logs 200/404/501 responses

Communicates with second app for banned-country tracking

Client run on separate VM to simulate usage and errors

Tools: GKE, Docker, Kubernetes, GCS, Cloud Logging, VM

📄 File 10 – Infrastructure as Code with Deployment Manager
Uses Google Deployment Manager to provision:

Cloud SQL, GCS, VMs, service accounts, Pub/Sub, and permissions

Automatically creates schema if it doesn’t exist

Demonstrates end-to-end deployment, functionality, and teardown

Tools: Google Deployment Manager, YAML/Config files, Python (schema setup), Pub/Sub, curl
