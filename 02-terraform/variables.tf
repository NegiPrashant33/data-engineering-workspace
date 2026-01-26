variable "credentials" {
  description = "my credentials"
  default     = "./keys/my-cred.json"
}

variable "project" {
  description = "project name"
  default     = "terraform-workspace-485405"
}

variable "location" {
  description = "project location"
  default     = "US"
}

variable "region" {
  description = "project region"
  default     = "us-central1"
}

variable "bq_dataset_name" {
  description = "my bigquery dataset name"
  default     = "demo_dataset"
}

variable "gcs_bucket_name" {
  description = "storage bucket name"
  default     = "terraform-workspace-485405-terra-bucket"
}

variable "gcs_storage_class" {
  description = "bucket storage class"
  default     = "STANDARD"
}