from opensearchpy import OpenSearch, helpers
from datetime import datetime

# Function to retrieve cluster metrics from the OpenSearch cluster
def get_cluster_metrics(client):
    # Fetch cluster stats using the OpenSearch client
    cluster_stats = client.cluster.stats()
    return cluster_stats

# Function to collect and structure cluster metrics for indexing
def collect_cluster_metrics(client):
    # Retrieve raw cluster metrics
    cluster_metrics = get_cluster_metrics(client)

    # Get the current timestamp for the metrics
    timestamp = datetime.now().isoformat()

    # Structure the metrics into a document for indexing
    document = {
        'timestamp': timestamp,
        'nodes_count': cluster_metrics['nodes']['count']['total'],  # Total number of nodes in the cluster
        'indices_count': cluster_metrics['indices']['count'],  # Number of indices in the cluster
        'shards_count': cluster_metrics['indices']['shards']['total'],  # Total number of shards
        'documents_count': cluster_metrics['indices']['docs']['count'],  # Total number of documents
        'os_memory_total': cluster_metrics['nodes']['os']['mem']['total_in_bytes'],  # Total memory in bytes
        'os_memory_free': cluster_metrics['nodes']['os']['mem']['free_in_bytes'],  # Free memory in bytes
        'os_memory_used': cluster_metrics['nodes']['os']['mem']['used_in_bytes'],  # Used memory in bytes
        'os_memory_used_percent': cluster_metrics['nodes']['os']['mem']['used_percent'],  # Percentage of used memory
        'jvm_memory_used': cluster_metrics['nodes']['jvm']['mem']['heap_used_in_bytes'],  # Used JVM heap memory in bytes
        'fs_space_total': cluster_metrics['nodes']['fs']['total_in_bytes'],  # Total file system space in bytes
        'fs_space_free': cluster_metrics['nodes']['fs']['free_in_bytes'],  # Free file system space in bytes
        'fs_space_used': cluster_metrics['nodes']['fs']['total_in_bytes'] - cluster_metrics['nodes']['fs']['free_in_bytes']  # Used file system space in bytes
    }
    yield document  # Yield the document for further processing or indexing


# Main function to initialize the OpenSearch client and index the metrics
def main():
    # OpenSearch host URL (replace with your OpenSearch server URL)
    host = 'https://your-opensearch-host:9200'

    # Initialize the OpenSearch client
    client = OpenSearch(
        hosts=[host],
        http_auth=('your-username', 'your-password'),  # Replace with valid credentials
        verify_certs=False,  # Disable certificate verification (use cautiously in production)
        ssl_assert_hostname=False,  # Disable SSL hostname verification
        ssl_show_warn=False,  # Suppress SSL warnings
        timeout=1000  # Set the timeout for OpenSearch requests
    )

    # Collect cluster metrics
    metrics = collect_cluster_metrics(client)

    # Index the collected metrics into an OpenSearch index
    response = client.index(index="cluster-monitoring", body=next(metrics))
    print("Document indexed:", response)


# Entry point of the script
if __name__ == "__main__":
    main()
