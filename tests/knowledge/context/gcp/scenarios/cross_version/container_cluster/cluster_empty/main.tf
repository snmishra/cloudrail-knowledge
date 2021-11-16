resource "google_container_cluster" "cluster" {
    name = "kuber-2"
    location = "us-central1-a"
}
resource "google_container_node_pool" "add_cluster" {
    name = "node-cluster-2"
    location = "us-central1"
    cluster = google_container_cluster.cluster.id
    node_count = 2

    node_config {
        preemptible = true
        machine_type = "e2-medium"
        disk_size_gb = "30"
    }
}