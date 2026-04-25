# 1. GKE Cluster Tanımı
resource "google_container_cluster" "primary" {
  name     = "ml-app-cluster"
  location = "us-central1" # Görseldeki Region seçimi

  # Görseldeki varsayılan network ayarları
  network    = "default"
  subnetwork = "default"

  # Sektörel En İyi Pratik (Best Practice): 
  # Varsayılan node pool'u silip, aşağıda kendi özel node pool'umuzu tanımlıyoruz.
  remove_default_node_pool = true
  initial_node_count       = 1

  # Görseldeki "Advanced networking options" -> "Cluster default Pod address range" ayarı
  ip_allocation_policy {
    cluster_ipv4_cidr_block = "/17"
  }

  # Yanlışlıkla silinmelere karşı koruma (Geliştirme aşamasında false yapılabilir)
  deletion_protection = false
}

# 2. Özel Node Pool Tanımı
resource "google_container_node_pool" "primary_nodes" {
  name       = "ml-app-node-pool"
  location   = "us-central1"
  cluster    = google_container_cluster.primary.name
  
  # us-central1 bölgesindeki her bir zone için oluşturulacak node sayısı 
  # (Bölgesel cluster olduğu için genelde 3 zone x 1 = 3 makine oluşur)
  node_count = 1 

  node_config {
    preemptible  = false       # Production için false kalmalı.
    machine_type = "e2-medium" # MLOps iş yüküne göre ileride "e2-standard-4" vb. olarak güncelleyebilirsin.

    # DİKKAT: iam.tf dosyasında oluşturduğun Service Account'u Node'lara veriyoruz!
    # Bu sayede Kubernetes içindeki Pod'lar senin Storage Bucket'larına doğrudan erişebilir.
    service_account = google_service_account.kidney_disease.email
    
    oauth_scopes = [
      "https://www.googleapis.com/auth/cloud-platform"
    ]
  }
}