variable "environment" {
  type        = string
  description = "Name of the environment"
  default     = "development"
}

variable "aws_region" {
  type        = string
  description = "AWS region to deploy resources in"
  default     = "us-east-1"
}

variable "cidr_public" {
  type        = string
  description = "CIDR for public subnet"
  default     = "10.0.1.0/24"
}

variable "cidr_private" {
  type        = string
  description = "CIDR for private subnet"
  default     = "10.0.2.0/24"
}
