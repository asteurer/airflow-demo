terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.region
}

/*
=================================================================================
S3
=================================================================================
*/

resource "aws_s3_bucket" "s3_bucket" {
  bucket = var.bucket_name
  force_destroy = true
}