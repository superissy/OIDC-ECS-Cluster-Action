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
  family                   = "test"
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = 1024
  memory                   = 2048
  execution_role_arn       = data.aws_iam_role.ecs-service-role.arn
  container_definitions    = <<TASK_DEFINITION
[
  {
    "name": "iis",
    "image": ${var.image_name},
    "cpu": 1024,
    "memory": 2048,
    "essential": true
    "portMappings": [
      {
        "containerPort": 80,
        "hostPort": 80
      }
    ]
  }
]
TASK_DEFINITION
}

# IAM Roles
data "aws_iam_role" "ecs-service-role" {
  name = "ecsServiceRole"
}


# ECS Service
resource "aws_ecs_service" "owasp_juice_shop_service" {
  name            = "owasp_juice_shop_service"
  cluster         = aws_ecs_cluster.owasp-juice-shop.id
  task_definition = aws_ecs_task_definition.owasp_juice_shop_task.arn
  launch_type     = "FARGATE"

  network_configuration {
    subnets          = data.aws_subnets.default.ids
    assign_public_ip = true
  }

  desired_count = 1
}
