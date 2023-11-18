provider "google" {
  project = "task-bot-63b37"
  region  = "us-central1"
}

resource "google_cloudfunctions_function" "schedule_bot" {
    name = "schedule-bot-${var.env}"
    description = "Automatic categorization and delay of todoist tasks"
    runtime = "python311"

    source_archive_bucket = google_storage_bucket.bucket.name
    source_archive_object = google_storage_bucket_object.archive.name
}