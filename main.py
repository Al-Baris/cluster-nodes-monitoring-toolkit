import os
from opensearchpy import OpenSearch, RequestsHttpConnection
import logging
from enum import Enum
from cxs_monitoring_nodes import collect_nodes_metrics
from cxs_monitoring_cluster import collect_cluster_metrics

# Configure logging for the script to display information and debug messages.
logging.basicConfig(level=logging.INFO)

# Enum class to define the scope of metrics collection: either Cluster or Nodes.
class Scope(Enum):
    CLUSTER = "cluster"
    NODES = "nodes"

# Function to collect metrics based on the provided scope (Cluster or Nodes).
def collect_metrics(client, scope):
    if scope == Scope.CLUSTER:
        # Collect cluster-level metrics.
        return collect_cluster_metrics(client)
    elif scope == Scope.NODES:
        # Collect node-level metrics.
        return collect_nodes_metrics(client)
    else:
        # Return an empty list for unsupported scopes.
        return []

# Function to collect and index metrics into OpenSearch.
def collect_and_index_metrics(client, index_name, scope):
    # Iterate through the collected metrics and index each document into OpenSearch.
    for doc in collect_metrics(client, scope):
        client.index(index=index_name, body=doc)

if __name__ == '__main__':
    # Start of the monitoring script execution.
    logging.info("Starting the monitoring script.")

    # Initialize the OpenSearch client with environment variables for configuration.
    client = OpenSearch(
        os.getenv('CXS_CORE_URL', 'https://example-opensearch-url:9200'),  # Replace with your OpenSearch URL.
        http_auth=(
            os.getenv('CXS_CORE_USERNAME', 'your_username'),  # Replace with your username.
            os.getenv('CXS_CORE_PASSWORD', 'your_password')   # Replace with your password.
        ),
        verify_certs=False,  # Disable certificate verification for simplicity (not recommended for production).
        ssl_assert_hostname=False,
        ssl_show_warn=False,
        timeout=1000,  # Set timeout to handle long-running operations.
        connection_class=RequestsHttpConnection  # Use HTTP connection for OpenSearch client.
    )

    # Retrieve the indices for cluster and node metrics from environment variables or use default values.
    cxs_monitoring_cluster = os.getenv("CXS_MONITORING_CLUSTER_INDEX", "default-cluster-index")
    cxs_monitoring_nodes = os.getenv("CXS_MONITORING_NODES_INDEX", "default-nodes-index")

    # Collect and index cluster metrics into the specified OpenSearch index.
    collect_and_index_metrics(client, cxs_monitoring_cluster, Scope.CLUSTER)

    # Collect and index node metrics into the specified OpenSearch index.
    collect_and_index_metrics(client, cxs_monitoring_nodes, Scope.NODES)

    # Log the completion of the metrics collection and indexing process.
    logging.info("Metrics collection and indexing complete.")
