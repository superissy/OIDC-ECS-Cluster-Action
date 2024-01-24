resource "aws_ecs_cluster" "owasp-juice-shop" {
  name = "owasp-juice-shop"
}


data "aws_vpc" "default" {
  default = true
}

data "aws_subnets" "default" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.default.id]
  }
}


# ECS Task Definition
resource "aws_ecs_task_definition" "owasp_juice_shop_task" {
  family                   = "owasp_juice_shop_task"
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = 1024
  memory                   = 2048
  execution_role_arn       = aws_iam_role.ecs_service_role.arn
  container_definitions = jsonencode([{
    name      = "owasp-container",
    image     = var.image_name,
    cpu       = 1024,
    memory    = 2048,
    essential = true,
    portMappings = [{
      containerPort = 80,
      hostPort      = 80
    }]
  }])
}

# IAM Roles
resource "aws_iam_role" "ecs_service_role" {
  name = "ecsServiceRole"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = "sts:AssumeRole",
        Effect = "Allow",
        Principal = {
          Service = "ecs.amazonaws.com"
        }
      },
    ]
  })
}

resource "aws_iam_role_policy_attachment" "ecs_service_role_policy" {
  role       = aws_iam_role.ecs_service_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonEC2ContainerServiceRole"
}


# ECS Service
resource "aws_ecs_service" "owasp_juice_shop_service" {
  name            = "owasp_juice_shop_service"
  force_new_deployment = true
  cluster         = aws_ecs_cluster.owasp-juice-shop.id
  task_definition = aws_ecs_task_definition.owasp_juice_shop_task.arn
  launch_type     = "FARGATE"

  network_configuration {
    subnets          = data.aws_subnets.default.ids
    assign_public_ip = true
  }

  desired_count = 1
}
