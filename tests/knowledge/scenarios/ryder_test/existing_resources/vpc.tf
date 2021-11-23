resource "aws_vpc" "main" {
  cidr_block       = "10.0.0.0/16"
  instance_tenancy = "default"

  tags = {
    Name        = var.environment
    Environment = var.environment
  }
}

resource "aws_default_security_group" "main" {
  vpc_id = aws_vpc.main.id

  tags = {
    Name        = var.environment
    Environment = var.environment
  }
}
