# 1. Service Account Creation
resource "google_service_account" "kidney_disease" {
  account_id   = "kidney-disease-mlops"
  display_name = "Kidney Disease MLOps Pipeline Service Account"
}

# 2. Proje Seviyesinde Yetkilendirme (Görsellerdeki Seçimler)
resource "google_project_iam_member" "kd_storage_admin" {
  project = "neat-chain-464913-k3" # provider.tf içindeki proje ID'n
  role    = "roles/storage.admin"
  member  = "serviceAccount:${google_service_account.kidney_disease.email}"
}

resource "google_project_iam_member" "kd_storage_viewer" {
  project = "neat-chain-464913-k3"
  role    = "roles/storage.objectViewer"
  member  = "serviceAccount:${google_service_account.kidney_disease.email}"
}

resource "google_project_iam_member" "kd_owner" {
  project = "neat-chain-464913-k3"
  role    = "roles/owner"
  member  = "serviceAccount:${google_service_account.kidney_disease.email}"
}

# 3. JSON Key Oluşturma
resource "google_service_account_key" "kidney_disease_key" {
  service_account_id = google_service_account.kidney_disease.name
}

# JSON key'i projendeki infrastructure dizinine kaydetme
resource "local_file" "kd_key_file" {
  content  = base64decode(google_service_account_key.kidney_disease_key.private_key)
  filename = "${path.module}/kidney-disease-gcp-key.json"
}

# 4. Sadece Oluşturduğumuz Bucket'a Özel Yetki Verme
resource "google_storage_bucket_iam_member" "bucket_object_admin" {
  # main.tf içindeki bucket referans adını kullanıyoruz
  bucket = google_storage_bucket.mlops_artifacts_bucket.name
  role   = "roles/storage.objectAdmin"
  member = "serviceAccount:${google_service_account.kidney_disease.email}"
}

resource "google_storage_bucket_iam_member" "bucket_object_viewer_bucket_level" {
  bucket = google_storage_bucket.mlops_artifacts_bucket.name
  role   = "roles/storage.objectViewer"
  member = "serviceAccount:${google_service_account.kidney_disease.email}"
}

resource "google_storage_bucket_iam_member" "dvc_bucket_object_admin" {
  bucket = google_storage_bucket.dvc_artifacts_bucket.name
  role   = "roles/storage.objectAdmin"
  member = "serviceAccount:${google_service_account.kidney_disease.email}"
}

resource "google_storage_bucket_iam_member" "dvc_bucket_object_viewer" {
  bucket = google_storage_bucket.dvc_artifacts_bucket.name
  role   = "roles/storage.objectViewer"
  member = "serviceAccount:${google_service_account.kidney_disease.email}"
}