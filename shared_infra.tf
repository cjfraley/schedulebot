# Deployment Service Account
# Build Trigger
provider "google" {
  project = "task-bot-63b37"
  region  = "us-central1"
}

locals {
  env = "dev"
}

resource "google_storage_bucket" "function_archives" {
  name     = "task_scheduler_code_cf"
  location = "us-central1"
}

resource "google_secret_manager_secret" "todoist_key" {
  secret_id = "todoist_key"
  replication {
    user_managed {
      replicas {
        location = "us-central1"
      }
    }
  }
}

resource "google_secret_manager_secret_version" "secret-version-basic" {
  secret = google_secret_manager_secret.todoist_key.id

  secret_data = file("/home/trooper310/taskbot_scratch/token.secret")
}

resource "google_service_account" "account" {
  account_id = "todoist-utility-sa"
  display_name = "Todoist Function Service Account"
}

resource "google_pubsub_topic" "taskbot_schedule" {
  name = "taskbot-topic"
}

module "scheduler" {
  source      = "./task_schedule_tool"
  env         = local.env
  code_bucket = google_storage_bucket.function_archives.name
  pubsub = google_pubsub_topic.taskbot_schedule.id
}
