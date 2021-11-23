resource "aws_route" "public_internet_route" {
  // Provide public subnet instances with
  // a route to the internet
  route_table_id         = aws_route_table.public.id
  destination_cidr_block = "0.0.0.0/0"
  gateway_id             = aws_internet_gateway.public.id
  depends_on = [
    aws_route_table.public,
    aws_internet_gateway.public,
  ]
}

resource "aws_route" "private_internet_route" {
  // Provide private subnet instances with
  // a route to the internet
  route_table_id         = aws_route_table.private.id
  destination_cidr_block = "0.0.0.0/0"
  nat_gateway_id         = aws_nat_gateway.private.id
  depends_on = [
    aws_route_table.private,
    aws_nat_gateway.private,
  ]
}
