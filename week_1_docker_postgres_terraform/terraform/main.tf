terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "7.16.0"
    }
  }
}

provider "google" {
  credentials = file("./keys/my_cred.json")
  project     = "starry-arbor-485309-r2"
  region      = "australia-southeast1"
}

resource "google_storage_bucket" "demo-bucket" {
  name          = "starry-arbor-485309-r2-terra-bucket"
  location      = "AUSTRALIA-SOUTHEAST1"
  force_destroy = true
  
  uniform_bucket_level_access = true  # Changed from block to argument

  lifecycle_rule {
    condition {
      age = 1
    }
    action {
      type = "AbortIncompleteMultipartUpload"
    }
  }
}