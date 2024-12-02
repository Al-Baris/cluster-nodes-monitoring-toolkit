# Node and Cluster Monitoring Toolkit

This project provides a Python-based monitoring system designed to collect, process, and index performance metrics for OpenSearch clusters and nodes. It enables real-time and historical insights through efficient data aggregation and visualization using OpenSearch Dashboards.

---

## Features

- **Cluster Monitoring**: Tracks key metrics such as node count, indices, shards, memory usage, and JVM performance.
- **Node Monitoring**: Collects detailed statistics on document counts, indexing/search times, memory, and disk utilization for individual nodes.
- **Automated Data Collection**: Uses Python scripts (`main.py`, `cluster.py`, `nodes.py`) to automate metric collection and indexing into OpenSearch.
- **Visualization**: Leverages OpenSearch Dashboards for real-time and trend-based data visualization.

---

## Benefits

This monitoring toolkit provides a scalable and efficient solution for maintaining system stability, identifying bottlenecks, and optimizing OpenSearch performance.

---

## Prerequisites

Before using the toolkit, ensure you have the following:

- **Python**: Version 3.8 or later.
- **OpenSearch**: A running OpenSearch cluster (tested with version 2.11).
- **Dependencies**: Install required Python libraries using `pip install -r requirements.txt`.

---

## Setup Instructions

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-repository/node-cluster-monitoring.git
   cd node-cluster-monitoring

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   
3. **Set Environment Variables: Create a .env file or export the required environment variables**:
   ```bash
   export CXS_CORE_URL="https://your-opensearch-url:9200"
   export CXS_CORE_USERNAME="your_username"
   export CXS_CORE_PASSWORD="your_password"
   export CXS_MONITORING_CLUSTER_INDEX="cluster-monitoring"
   export CXS_MONITORING_NODES_INDEX="node-monitoring"

4. **Run the Scripts**:
- To monitor cluster metrics:
   ```bash
   python cluster.py
   
- To monitor node metrics:
   ```bash
   python main.py

## Code Overview
main.py
- Purpose: Collects and indexes cluster- and node-level metrics into OpenSearch.
- Key Features:
  - Fetches detailed node statistics including memory, disk, and query times.
  - Indexes metrics into the node-monitoring index (customizable).
    
