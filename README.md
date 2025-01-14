# Node and Cluster Monitoring Toolkit

This project provides a Python-based monitoring system designed to collect, process, and index performance metrics for OpenSearch clusters and nodes. It enables real-time and historical insights through efficient data aggregation and visualization using OpenSearch Dashboards.

---

## Features

- **Cluster Monitoring**: Tracks key metrics such as node count, indices, shards, memory usage, and JVM performance.
- **Node Monitoring**: Collects detailed statistics on document counts, indexing/search times, memory, and disk utilization for individual nodes.
- **Automated Data Collection**: Uses Python scripts (`main.py`, `cluster.py`, `nodes.py`) to automate metric collection and indexing into OpenSearch.
- **Visualization**: Leverages OpenSearch Dashboards for real-time and trend-based data visualization.
- **Docker Integration**: Provides a Docker image for simplified deployment and scalability.
- **Scheduled Execution**: Utilizes a CronJob for periodic execution of monitoring tasks.

---

## Benefits

This monitoring toolkit provides a scalable and efficient solution for maintaining system stability, identifying bottlenecks, and optimizing OpenSearch performance.

---

## Prerequisites

Before using the toolkit, ensure you have the following:

- **Python**: Version 3.8 or later.
- **OpenSearch**: A running OpenSearch cluster (tested with version 2.11).
- **Dependencies**: Install required Python libraries using `pip install -r requirements.txt`.
- **Docker**: Ensure Docker is installed and running for containerized deployment.
- **Kubernetes**: Required if deploying the CronJob.

---

## Setup Instructions

### Local Deployment

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-repository/node-cluster-monitoring.git
   cd node-cluster-monitoring
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Environment Variables**:
   Create a `.env` file or export the required environment variables:
   ```bash
   export CXS_CORE_URL="https://your-opensearch-url:9200"
   export CXS_CORE_USERNAME="your_username"
   export CXS_CORE_PASSWORD="your_password"
   export CXS_MONITORING_CLUSTER_INDEX="cluster-monitoring"
   export CXS_MONITORING_NODES_INDEX="node-monitoring"
   ```

4. **Run the Scripts**:
   - To monitor cluster metrics:
     ```bash
     python cluster.py
     ```
   - To monitor node metrics:
     ```bash
     python main.py
     ```

### Docker Deployment

1. **Build the Docker Image**:
   ```bash
   docker build -t docker.example.com/sweet/monitoring/cxs-core-monitoring:latest .
   ```

2. **Run the Docker Container**:
   ```bash
   docker run -d \
     -e CXS_CORE_URL="https://your-opensearch-url:9200" \
     -e CXS_CORE_USERNAME="your_username" \
     -e CXS_CORE_PASSWORD="your_password" \
     docker.example.com/sweet/monitoring/cxs-core-monitoring:latest
   ```

3. **Push the Docker Image** (if required):
   ```bash
   docker push docker.example.com/sweet/monitoring/cxs-core-monitoring:latest
   ```

### Kubernetes CronJob Deployment

1. **Apply the CronJob Manifest**:
   Create a file `cronjob.yaml` with the following content and apply it:
   ```yaml
   kind: CronJob
   apiVersion: batch/v1
   metadata:
     name: cxs-core-monitoring-cron-job
     namespace: sweet
   spec:
     schedule: '4/15 * * * *'
     concurrencyPolicy: Forbid
     suspend: true
     startingDeadlineSeconds: 180
     jobTemplate:
       spec:
         backoffLimit: 0
         template:
           spec:
             restartPolicy: OnFailure
             containers:
               - name: cxs-core-monitor
                 image: docker.example.com/sweet/monitoring/cxs-core-monitoring:latest
                 command: [ "python", "main.py" ]
                 env:
                   - name: CXS_CORE_URL
                     value: https://your-opensearch-url:9200
                   - name: CXS_CORE_USERNAME
                     valueFrom:
                       secretKeyRef:
                         name: cxs-core-access
                         key: username
                   - name: CXS_CORE_PASSWORD
                     valueFrom:
                       secretKeyRef:
                         name: cxs-core-access
                         key: password
                   - name: SSL_CERT_ALLOW_SELF_SIGNED
                     value: "true"
                 imagePullPolicy: IfNotPresent
             imagePullSecrets:
               - name: docker-example-com-credentials
     successfulJobsHistoryLimit: 1
     failedJobsHistoryLimit: 3
   ```

2. **Deploy the CronJob**:
   ```bash
   kubectl apply -f cronjob.yaml
   ```

---

## Code Overview

### `main.py`
- **Purpose**: Collects and indexes cluster- and node-level metrics into OpenSearch.
- **Key Features**:
  - Fetches detailed node statistics including memory, disk, and query times.
  - Indexes metrics into the `node-monitoring` index (customizable).

### Dockerfile
- **Purpose**: Builds a containerized version of the monitoring toolkit.
- **Key Features**:
  - Includes dependencies and environment variable configuration.
  - Sets the entry point to `main.py`.

### `cronjob.yaml`
- **Purpose**: Automates periodic execution of the monitoring scripts in Kubernetes.
- **Key Features**:
  - Configurable schedule.
  - Ensures non-concurrent executions with `concurrencyPolicy: Forbid`.

---

## Contact
For questions or contributions, feel free to open an issue or submit a pull request on GitHub.

