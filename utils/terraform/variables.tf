variable "instance_name" {
  description = "Value of the Name Tag for the EC2 instance"
  type        = string
  default     = "wesm-terraform"
}

variable "key_name" {
  description = "Key Pair to Use"
  type        = string
  default     = "wesm-pair"
}