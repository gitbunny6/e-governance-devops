import os
import time
from flask import Flask, jsonify, request, Response
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

REQUEST_COUNT = Counter(
    "egov_http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "status"]
)
REQUEST_LATENCY = Histogram(
    "egov_http_request_duration_seconds",
    "HTTP request duration in seconds",
    ["method", "endpoint"]
)

SERVICES = [
    {"id": 1, "name": "Birth Certificate", "category": "Certificates"},
    {"id": 2, "name": "Income Certificate", "category": "Certificates"},
    {"id": 3, "name": "Property Tax Payment", "category": "Taxation"},
    {"id": 4, "name": "Water Connection", "category": "Utilities"},
]
APPLICATIONS = []
NEXT_ID = 1


@app.before_request
def start_timer():
    request.start_time = time.perf_counter()


@app.after_request
def record_metrics(response):
    endpoint = request.endpoint or "unknown"
    duration = time.perf_counter() - getattr(
        request, "start_time", time.perf_counter()
    )
    if endpoint != "metrics":
        REQUEST_COUNT.labels(
            request.method, endpoint, str(response.status_code)
        ).inc()
        REQUEST_LATENCY.labels(request.method, endpoint).observe(duration)
    return response


@app.get("/")
def home():
    return jsonify({
        "application": "E-Governance Citizen Services Portal",
        "version": "1.0.0",
        "status": "running"
    })


@app.get("/health")
def health():
    return jsonify({"status": "healthy"}), 200


@app.get("/api/services")
def get_services():
    return jsonify({"services": SERVICES}), 200


@app.post("/api/applications")
def create_application():
    global NEXT_ID
    data = request.get_json(silent=True) or {}
    name = data.get("citizen_name")
    service_id = data.get("service_id")

    if not isinstance(name, str) or not name.strip():
        return jsonify({"error": "citizen_name is required"}), 400

    try:
        service_id = int(service_id)
    except (TypeError, ValueError):
        return jsonify({"error": "service_id must be a valid integer"}), 400

    service = next((s for s in SERVICES if s["id"] == service_id), None)
    if service is None:
        return jsonify({"error": "Service not found"}), 404

    application = {
        "id": NEXT_ID,
        "citizen_name": name.strip(),
        "service_id": service_id,
        "service_name": service["name"],
        "status": "Submitted"
    }
    APPLICATIONS.append(application)
    NEXT_ID += 1
    return jsonify({"application": application}), 201


@app.get("/api/applications")
def get_applications():
    return jsonify({"applications": APPLICATIONS}), 200


@app.get("/metrics")
def metrics():
    return Response(generate_latest(), content_type=CONTENT_TYPE_LATEST)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "5000")))
