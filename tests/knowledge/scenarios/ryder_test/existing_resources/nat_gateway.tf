resource "aws_nat_gateway" "private" {
  // Allows instances in the private subnet
  // to establish outbound connections to the internet
  subnet_id            = aws_subnet.private.id
  allocation_id        = aws_eip.nat_gateway.id
  connectivity_type    = "public"
  depends_on = [
    aws_internet_gateway.public,
  ]
  tags = {
    Name        = "${var.environment}-nat-gateway-private"
    Environment = var.environment
  }
}

resource "aws_eip" "nat_gateway" {
  vpc = true
  tags = {
    Name        = "${var.environment}-private-nat-gateway-elastic-ip"
    Environment = var.environment
  }
}
