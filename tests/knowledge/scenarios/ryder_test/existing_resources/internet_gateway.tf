resource "aws_internet_gateway" "public" {
  // Allow instances within the public subnet
  // to have internet access
  vpc_id = aws_vpc.main.id

  tags = {
    Name        = "${var.environment}-internet-gateway"
    Environment = var.environment
  }
}
