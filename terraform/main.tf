terraform {
  required_providers {
    google = {
      source = "hashicorp/google"
      version = "6.42.0"
    }
  }
}

provider "google" {
  project = var.project
  region  = var.region
}

resource "google_service_account" "sync_sa" {
  account_id   = "freee-sync-sa"
  display_name = "freee attendance sync SA"
}

resource "google_secret_manager_secret" "freee_secret" {
  secret_id = "freee-oauth-cred"
  replication {
    user_managed {
      replicas {
        location = "us-central1"
      }
    }
  }
}

resource "google_pubsub_topic" "sync_topic" {
  name = "freee-sync"
}

resource "google_storage_bucket" "source_bucket" {
  name          = "${var.project}-freee-sync-source"
  location      = "US" # GCS bucket location must be US or EU for Cloud Functions
  force_destroy = true # For easy cleanup during development
}

resource "google_storage_bucket_object" "source_object" {
  name   = "freee-sync-source.zip"
  bucket = google_storage_bucket.source_bucket.name
  source = "../function_source.zip" # This will be created by CI/CD

  # Add a dependency on the bucket to ensure it's created first
  depends_on = [google_storage_bucket.source_bucket]
}

resource "google_cloudfunctions2_function" "sync_fn" {
  name        = "freee-sync-fn"
  location    = var.region
  build_config {
    runtime     = "python312"
    entry_point = "main"
    source {
      storage_source {
        bucket = google_storage_bucket.source_bucket.name
        object = google_storage_bucket_object.source_object.name
      }
    }
  }
  service_config {
    timeout_seconds = 540
    available_memory = "512M"
    max_instance_count = 2
    service_account_email = google_service_account.sync_sa.email
    environment_variables = {
      FREEE_SECRET_NAME   = google_secret_manager_secret.freee_secret.id
      TARGET_SHEET_ID     = var.sheet_id
    }
  }
  event_trigger {
    trigger_region = var.region
    pubsub_topic   = google_pubsub_topic.sync_topic.id
  }
}

resource "google_cloud_scheduler_job" "daily_job" {
  name = "freee-sync-daily"
  schedule = "0 18 * * *"          # 03:00 JST = 18:00 UTC (サマータイムなし)
  time_zone = "Asia/Tokyo"
  pubsub_target {
    topic_name = google_pubsub_topic.sync_topic.id
    data       = base64encode(jsonencode({mode="daily"}))
  }
}