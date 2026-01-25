variable "location" {
    description = "Project Location Name"
    default = "AUSTRALIA-SOUTHEAST1"
}

variable "bq_dataset_name" {
    description = "My BigQuery Dataset Name"
    default = "demo_dataset"
}

variable "gcs_bucket_name" {
    description = "My Storage Bucket Name"
    default = "starry-arbor-485309-r2-terra-bucket"
}

variable "gcs_storage_class"{
    description = "Bucket Storage Class"
    default = "STANDARD"
}