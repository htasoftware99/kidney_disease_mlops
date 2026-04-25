# 1. GKE Cluster Tanımı
resource "google_container_cluster" "primary" {
  name     = "ml-app-cluster"
  location = "us-central1-a" # DEĞİŞİKLİK: Sadece 'a' zone'unu seçerek 3 yerine 1 makine açılmasını sağlıyoruz

  network    = "default"
  subnetwork = "default"

  remove_default_node_pool = true
  initial_node_count       = 1

  ip_allocation_policy {
    cluster_ipv4_cidr_block = "/17"
  }

  deletion_protection = false
}

# 2. Özel Node Pool Tanımı
resource "google_container_node_pool" "primary_nodes" {
  name       = "ml-app-node-pool"
  location   = "us-central1-a" # DEĞİŞİKLİK: Burası da cluster ile aynı zone olmalı
  cluster    = google_container_cluster.primary.name
  
  node_count = 1 

  node_config {
    preemptible  = false
    machine_type = "e2-medium"
    
    # KOTA ÇÖZÜMÜ: Disk tipini standart yapıp boyutunu 50 GB'a düşürdük
    disk_size_gb = 50
    disk_type    = "pd-standard" 

    service_account = google_service_account.kidney_disease.email
    
    oauth_scopes = [
      "https://www.googleapis.com/auth/cloud-platform"
    ]
  }
}