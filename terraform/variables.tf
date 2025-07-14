variable "project" {
  description = "The GCP project ID."
  type        = string
}

variable "region" {
  description = "The GCP region for resources."
  type        = string
  default     = "asia-northeast1"
}

variable "sheet_id" {
  description = "The Google Sheet ID for attendance data."
  type        = string
}