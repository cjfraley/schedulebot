variable "env" {
  type = string
  default = "dev"
}
data "google_cloudfunctions_function" "task_transfer" {
  name = "todoist-to-bigquery-${env}"
}