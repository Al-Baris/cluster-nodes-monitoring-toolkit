from opensearchpy import OpenSearch
from datetime import datetime

# Function to retrieve detailed node metrics from the OpenSearch cluster.
# Metrics include OS, JVM, filesystem, indices, and thread pool stats.
def get_node_metrics(client):
    return client.nodes.stats(metric='os,jvm,fs,indices,thread_pool')

# Function to process node metrics and structure them into documents for indexing.
# Each document contains detailed information about a specific node.
def collect_nodes_metrics(client):
    # Fetch raw node stats from OpenSearch
    node_stats = get_node_metrics(client)

    # Iterate over each node's stats and construct a structured document
    for node_id, stats in node_stats['nodes'].items():
        document = {
            'timestamp': datetime.now().isoformat(),  # Current timestamp for the metric
            'node_id': node_id,  # Unique identifier for the node
            'node_name': stats['name'],  # Node's display name
            'documents_count': stats['indices']['docs']['count'],  # Total number of documents on the node
            'indexing_time_in_millies': stats['indices']['indexing']['index_time_in_millis'],  # Indexing time in milliseconds
            'search_time_in_millies': stats['indices']['search']['query_time_in_millis'],  # Search query time in milliseconds
            'scroll_time_in_millies': stats['indices']['search']['scroll_time_in_millis'],  # Scroll query time in milliseconds
            'fetch_time_in_millies': stats['indices']['search']['fetch_time_in_millis'],  # Fetch time in milliseconds
            'os_memory_total': stats['os']['mem']['total_in_bytes'],  # Total memory in bytes
            'os_memory_free': stats['os']['mem']['free_in_bytes'],  # Free memory in bytes
            'os_memory_used': stats['os']['mem']['used_in_bytes'],  # Used memory in bytes
            'os_memory_used_percent': stats['os']['mem']['used_percent'],  # Percentage of used memory
            'jvm_memory_used': stats['jvm']['mem']['heap_used_in_bytes'],  # JVM heap memory used in bytes
            'gc_in_millis': stats['jvm']['gc']['collectors']['old']['collection_time_in_millis'] 
                             + stats['jvm']['gc']['collectors']['young']['collection_time_in_millis'],  # Total garbage collection time
            'fs_space_total': stats['fs']['total']['total_in_bytes'],  # Total filesystem space in bytes
            'fs_space_free': stats['fs']['total']['free_in_bytes'],  # Free filesystem space in bytes
            'fs_space_used': stats['fs']['total']['total_in_bytes'] - stats['fs']['total']['free_in_bytes']  # Used filesystem space
        }
        yield document  # Yield each document for further processing

# Main function to initialize the OpenSearch client and index metrics.
def main():
    # Initialize the OpenSearch client with connection details.
    # Replace sensitive information with environment variables or secrets in production.
    client = OpenSearch(
        hosts=['https://example-opensearch-url:9200'],  # OpenSearch endpoint (replace with your URL)
        http_auth=('username', 'password'),  # Authentication credentials (replace with your credentials)
        verify_certs=False,  # Disable certificate verification (set to True in production)
        ssl_assert_hostname=False,  # Disable hostname verification
        ssl_show_warn=False,  # Suppress SSL warnings
        timeout=1000  # Set timeout for requests
    )

    # Collect node metrics and index them into OpenSearch
    documents = collect_nodes_metrics(client)
    for doc in documents:
        # Index each document into the specified OpenSearch index
        response = client.index(index="node-metrics-index", body=doc)  # Replace with your target index
        print("Document indexed:", response)

# Entry point of the script
if __name__ == "__main__":
    main()
