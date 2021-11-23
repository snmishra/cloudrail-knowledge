resource "aws_subnet" "public" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = var.cidr_public
  map_public_ip_on_launch = true

  tags = {
    Name        = "${var.environment}-public"
    Environment = var.environment
    Public      = true
  }
}

resource "aws_subnet" "private" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = var.cidr_private
  map_public_ip_on_launch = false

  tags = {
    Name        = "${var.environment}-private"
    Environment = var.environment
    Public      = false
  }
}
