output "function_name" {
  description = "The name of the Cloud Function."
  value       = google_cloudfunctions2_function.sync_fn.name
}

output "service_account_email" {
  description = "The email of the service account used by the Cloud Function."
  value       = google_service_account.sync_sa.email
}

output "pubsub_topic_name" {
  description = "The name of the Pub/Sub topic."
  value       = google_pubsub_topic.sync_topic.name
}