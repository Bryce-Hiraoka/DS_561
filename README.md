☁️ Cloud Computing Projects
This repository showcases a sequence of 10 hands-on cloud computing projects using Google Cloud Platform (GCP). Projects cover resource management, data analysis, web services, machine learning, distributed processing, and infrastructure automation.

📂 Project Overview
1. Basic GCP Operations
Create and manage GCS buckets, VMs, and service accounts
Use gcloud, gsutil, and the GCP Console
Automate cleanup of all resources

2. Web Graph + PageRank
Generate a dataset of 10,000 linked files
Upload to GCS, analyze link stats, and implement PageRank
Make bucket world-readable and report cloud costs

3. Cloud Function Web Server
Handle HTTP GET requests for GCS files via Cloud Functions
Return 200, 404, and 501 status codes with logging
Second app handles blocked countries (e.g. North Korea, Iran)

4. VM-Based HTTP Server
Deploy a web server on a GCP VM with a static IP
Log errors and serve GCS files
Stress test with concurrent clients, report limits and costs

5. Store Requests in Cloud SQL
Log request metadata (country, IP, gender, etc.) into a normalized SQL schema
Separate logs for failed requests
Analyze usage patterns (top countries, gender, age, success rate)

6. Machine Learning Models
Model 1: Predict country from IP (≥99% accuracy)
Model 2: Predict income from request metadata (target ≥80%)

7. Apache Beam + Dataflow
Find top 5 files by incoming/outgoing links
Run pipeline locally and in Dataflow
Compare runtimes

8. Load Balanced Deployment
Deploy 2 VM servers in different zones behind a load balancer
Include response header for zone tracking
Test failover and recovery speed

9. GKE + Containers
Containerize web server and deploy on Google Kubernetes Engine
Log 404 and 501 requests
Use second app to handle blocked countries

10. Deployment Manager Automation
Deploy VM, SQL DB, GCS, Pub/Sub, and permissions with GDM
Web server auto-creates schema if missing
Demo with HTTP client and curl
Tear down all resources when done

🧰 Tech Stack
Languages: Python, YAML
GCP Services: Compute Engine, Cloud Functions, GCS, Cloud SQL, GKE, Pub/Sub, Dataflow, Deployment Manager
Tools: Apache Beam, curl, scikit-learn

