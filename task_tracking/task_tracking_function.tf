variable "env" {
  type    = string
  default = "dev"
}
variable "bucket_name" {
  type    = string
  default = "schedulebot-dev"
}

resource "google_storage_bucket_object" "todo_to_bq_source" {
  name   = "${env}/task_tracking/todo_to_bq.zip"
  bucket = var.bucket_name
  source = "${path.module}/todo_to_bq_func"
}

resource "google_cloudfunctions_function" "todo_to_bq" {
  name                  = "todoist-to-bigquery-${env}"
  description           = "Transfers todoist events to bigquery"
  bucket                = var.bucket_name
  runtime               = "python39"
  source_archive_bucket = var.bucket_name
  source_archive_object = google_storage_bucket_object.todo_to_bq_source.name
  entry_point           = "todo_to_bq"
}

resource "google_cloudfunctions_function_iam_member" "invoker" {
  project        = google_cloudfunctions_function.function.project
  region         = google_cloudfunctions_function.function.region
  cloud_function = google_cloudfunctions_function.function.name

  role   = "roles/cloudfunctions.invoker"
  member = google_service_account.todo_to_bq_invoker.email
}

resource "google_service_account" "todo_to_bq_invoker" {

}

resource "google_cloud_scheduler_job" "daily_to-bq" {

}