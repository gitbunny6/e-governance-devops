# E-Governance DevOps Mini Project

## 1. Project Overview

The E-Governance DevOps project demonstrates how DevOps tools and practices can be used to deploy, test, monitor, and maintain a web-based application.

The project uses a Flask REST API to provide basic e-governance services and application submission functionality. Docker is used for containerization, Kubernetes manages application replicas and self-healing, and Prometheus and Grafana provide monitoring and visualization.

## 2. Objectives

- Develop a REST API for e-governance services.
- Containerize the application using Docker.
- Deploy the application using Kubernetes.
- Test API endpoints using Postman and Python unit tests.
- Collect application metrics using Prometheus.
- Visualize request rate and response time using Grafana.
- Demonstrate Kubernetes self-healing after a pod failure.
- Configure GitLab CI/CD for automated testing and Docker image building.

## 3. Technologies Used

- Python and Flask
- Docker
- Kubernetes
- GitLab and GitLab CI/CD
- Postman
- Prometheus
- Grafana

## 4. Application Features

- Application health endpoint
- List of available e-governance services
- Application submission and retrieval endpoints
- Prometheus metrics endpoint
- HTTP request counters and request-duration metrics

## 5. Architecture

1. Users send HTTP requests to the Flask REST API.
2. Docker packages the application and its dependencies.
3. Kubernetes deploys and maintains two application replicas.
4. Prometheus collects metrics from the application's `/metrics` endpoint.
5. Grafana queries Prometheus and visualizes application performance.
6. GitLab stores the project source code and contains the CI/CD pipeline configuration.
flowchart TD
    A[Developer] --> B[GitLab Repository]
    B --> C[GitLab CI/CD Pipeline]
    C --> D[Unit Tests]
    D --> E[Docker Image Build]
    E --> F[Kubernetes Deployment]
    F --> G[Flask Application]
    G --> H[Prometheus]
    H --> I[Grafana Dashboard]
## 6. Running the Application

Build the Docker image:

```bash
docker build -t egov-app:1.0 .
```

Run the application locally:

```bash
docker run -d --name egov-app -p 5001:5000 egov-app:1.0
```

Check the health endpoint:

```bash
curl http://localhost:5001/health
```

## 7. Kubernetes Deployment

Apply the deployment configuration:

```bash
kubectl apply -f k8s/deployment.yaml
```

Check the pods and service:

```bash
kubectl get pods
kubectl get services
```

Access the application health endpoint:

```bash
curl http://localhost:30080/health
```

## 8. Testing

Python unit tests are located in the `tests` directory.

Run them using:

```bash
python -m unittest discover -s tests -v
```

The three implemented unit tests check the health endpoint, services endpoint, and validation of an application submission with a missing citizen name.

API requests can also be tested using the Postman collection in the `postman` directory.

## 9. Monitoring

Prometheus collects metrics exposed by the application's `/metrics` endpoint.

The metrics include:
- Total HTTP requests
- Request duration and latency histogram
- Python process and runtime metrics

Grafana connects to Prometheus to visualize API request rate and average response time.

## 10. Self-Healing Demonstration

The Kubernetes deployment maintains two application replicas.

During testing, one application pod was deleted manually. Kubernetes automatically created a replacement pod, and both replicas returned to the Running state.

The health endpoint was checked after the replacement to verify application availability.

## 11. CI/CD

The `.gitlab-ci.yml` configuration defines:
- A unit-test stage
- A Docker image build stage

The pipeline is intended to run automatically when code is pushed to GitLab. Successful execution of both CI jobs must be verified separately.

## 12. Conclusion

This project demonstrates core DevOps concepts, including containerization, orchestration, automated testing, monitoring, and Kubernetes self-healing. It provides a local implementation of a basic E-Governance application supported by DevOps tools.
