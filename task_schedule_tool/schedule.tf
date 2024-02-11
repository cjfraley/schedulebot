provider "google" {
  project = "task-bot-63b37"
  region  = "us-central1"
}

data "archive_file" "function_code" {
  type        = "zip"
  source_dir  = "${path.module}/sched_source"
  output_path = "${path.module}/archive.zip"
}

resource "google_storage_bucket_object" "function_code" {
  name   = "${var.env}/schedulebot.zip"
  bucket = var.code_bucket
  source = "${path.module}/archive.zip"
}

# resource "google_cloud_run_service" "schedule_bot" {
#   name = "schedule-bot-dev"
#   location = "us-central1"
#   template {
#     spec 
#   }
# }
resource "google_cloudfunctions2_function" "schedule_bot" {
  name        = "schedule-bot-${var.env}"
  description = "Automatic categorization and delay of todoist tasks"
  location = "us-central1"

  build_config {
    entry_point = "schedule"
    runtime     = "python311"
    source {
      storage_source {
        bucket = var.code_bucket
        object = google_storage_bucket_object.function_code.name
      }
    }
  }

  event_trigger {
      trigger_region = "us-central1" #TODO better handle for this 
      event_type = "google.cloud.pubsub.topic.v1.messagePublished"
      pubsub_topic = var.pubsub
      retry_policy = "RETRY_POLICY_DO_NOT_RETRY"
  }
}
